"""Ninster — установка программ в один клик (аналог Ninite на winget).

Запуск:  python main.py
"""

import ctypes
import queue
import sys
import tkinter as tk

import customtkinter as ctk

from catalog import CATALOG, CATEGORIES
from installer import Installer, Status, winget_available, get_winget_version

APP_NAME = "Ninster"
APP_TAGLINE = "Все нужные программы — в один клик"
VERSION = "1.0.1"


def is_admin() -> bool:
    """True, если процесс запущен с правами администратора."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def elevate():
    """Перезапускает процесс с правами администратора (UAC один раз при старте)."""
    if sys.platform != "win32" or getattr(sys, "frozen", False) is False:
        return
    params = " ".join(sys.argv[1:])
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1)
    except Exception:
        pass


# ---------- Автоподнятие прав администратора ----------
# UAC запрашивается ОДИН раз при запуске, а не при установке каждой программы.
# Выполняется только при прямом запуске (не при импорте, напр. в smoke_test).

def _ensure_admin():
    if not is_admin():
        elevate()
        sys.exit(0)


# ---------- DPI / тема ----------
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

STATUS_META = {
    Status.QUEUED:     ("#8b8b8b", "Ожидание"),
    Status.INSTALLING: ("#d99a1b", "Установка…"),
    Status.DONE:       ("#2e9e5b", "Готово"),
    Status.ERROR:      ("#d64545", "Ошибка"),
    Status.SKIPPED:    ("#6b6b6b", "Пропущено"),
}

FONT_H1 = ("Segoe UI Semibold", 24)
FONT_SUB = ("Segoe UI", 12)
FONT_APP = ("Segoe UI Semibold", 14)
FONT_DESC = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 11)


class NinsterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} {VERSION}")
        self.geometry("920x720")
        self.minsize(720, 560)

        self.selected_count = 0
        self.installing = False
        self.total = 0
        self.finished = 0
        self.log_queue = queue.Queue()
        self.rows = {}          # app_id -> {frame, var, status_lbl, ...}
        self.vars = {}          # app_id -> tk.BooleanVar

        self._build_ui()
        self._apply_filter()
        self._check_winget()
        self.after(150, self._drain_log)

    # ---------- UI ----------
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Заголовок
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 8))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text=APP_NAME, font=FONT_H1).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header, text=APP_TAGLINE, font=FONT_SUB, text_color="gray60").grid(
            row=1, column=0, sticky="w")

        # Панель инструментов
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 6))
        toolbar.grid_columnconfigure(0, weight=1)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._apply_filter())
        self.search_entry = ctk.CTkEntry(
            toolbar, placeholder_text="Поиск программ…", textvariable=self.search_var, height=34)
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.cat_var = tk.StringVar(value="Все категории")
        cat_values = ["Все категории"] + list(CATEGORIES.values())
        self.cat_menu = ctk.CTkOptionMenu(
            toolbar, values=cat_values, variable=self.cat_var,
            command=lambda _: self._apply_filter(), width=200, height=34)
        self.cat_menu.grid(row=0, column=1, padx=(0, 8))

        self.select_all_btn = ctk.CTkButton(
            toolbar, text="Выбрать всё", width=120, height=34,
            command=lambda: self._select_visible(True))
        self.select_all_btn.grid(row=0, column=2, padx=(0, 8))

        self.clear_btn = ctk.CTkButton(
            toolbar, text="Снять всё", width=110, height=34, fg_color="#3a3a3a",
            hover_color="#4a4a4a", command=lambda: self._select_visible(False))
        self.clear_btn.grid(row=0, column=3)

        # Список программ
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 6))
        self.list_frame.grid_columnconfigure(0, weight=1)
        self._build_rows()

        # Низ: прогресс + статус + лог + кнопка установки
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 14))
        bottom.grid_columnconfigure(0, weight=1)

        self.progress = ctk.CTkProgressBar(bottom, height=10)
        self.progress.set(0)
        self.progress.grid(row=0, column=0, sticky="ew", columnspan=2, pady=(0, 8))

        self.status_lbl = ctk.CTkLabel(bottom, text="", font=FONT_SMALL, text_color="gray70")
        self.status_lbl.grid(row=1, column=0, sticky="w")

        self.log_btn = ctk.CTkButton(
            bottom, text="Журнал ▾", width=110, height=30, fg_color="#3a3a3a",
            hover_color="#4a4a4a", command=self._toggle_log)
        self.log_btn.grid(row=1, column=1, sticky="e", padx=(8, 8))

        self.scope_var = tk.BooleanVar(value=False)

        self.install_btn = ctk.CTkButton(
            bottom, text="Установить", height=44, font=("Segoe UI Semibold", 15),
            command=self._start_install)
        self.install_btn.grid(row=2, column=1, sticky="e", padx=(8, 0))

        # Журнал (скрыт по умолчанию)
        self.log_text = ctk.CTkTextbox(bottom, height=130, font=("Consolas", 10))
        self.log_text.configure(state="disabled")
        self.log_visible = False

        self.grid_rowconfigure(2, weight=1)

    def _build_rows(self):
        for app in CATALOG:
            row = ctk.CTkFrame(self.list_frame, fg_color="#1f1f1f", corner_radius=8)
            row.grid_columnconfigure(0, weight=1)
            row.grid_columnconfigure(2, weight=1)

            var = tk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(
                row, text=app.name, variable=var, font=FONT_APP,
                command=lambda a=app.id: self._on_toggle(a))
            cat = ctk.CTkLabel(
                row, text=CATEGORIES.get(app.category, app.category),
                font=FONT_SMALL, text_color="#7aa2c4")
            status_lbl = ctk.CTkLabel(
                row, text="", font=FONT_SMALL, width=120, anchor="e", text_color="gray50")
            desc = ctk.CTkLabel(
                row, text=app.description, font=FONT_DESC, text_color="gray55", anchor="w")

            cb.grid(row=0, column=0, sticky="w", padx=(16, 10), pady=(8, 0))
            cat.grid(row=0, column=1, sticky="e", padx=10)
            status_lbl.grid(row=0, column=2, sticky="e", padx=(10, 16))
            desc.grid(row=1, column=0, columnspan=3, sticky="w", padx=(16, 16), pady=(0, 8))

            self.rows[app.id] = {
                "frame": row, "var": var, "status_lbl": status_lbl, "app": app,
            }
            self.vars[app.id] = var

    # ---------- Фильтрация ----------
    def _matches(self, app, term: str, cat: str) -> bool:
        if cat != "Все категории" and CATEGORIES.get(app.category) != cat:
            return False
        if term:
            hay = f"{app.name} {app.description} {app.id}".lower()
            if term not in hay:
                return False
        return True

    def _apply_filter(self):
        term = self.search_var.get().strip().lower()
        cat = self.cat_var.get()
        r = 0
        for app in CATALOG:
            row = self.rows[app.id]["frame"]
            if self._matches(app, term, cat):
                row.grid(row=r, column=0, sticky="ew", padx=2, pady=3)
                r += 1
            else:
                row.grid_remove()

    def _visible_ids(self):
        term = self.search_var.get().strip().lower()
        cat = self.cat_var.get()
        return [a.id for a in CATALOG if self._matches(a, term, cat)]

    def _select_visible(self, value: bool):
        for aid in self._visible_ids():
            self.vars[aid].set(value)
        self._refresh_count()

    def _on_toggle(self, _app_id=None):
        self._refresh_count()

    def _refresh_count(self):
        self.selected_count = sum(1 for v in self.vars.values() if v.get())
        if not self.installing:
            n = self.selected_count
            self.install_btn.configure(
                text=f"Установить ({n})" if n else "Установить",
                state="normal" if n else "disabled")
            self.status_lbl.configure(
                text=f"Выбрано: {n} из {len(CATALOG)}" if n else "Выберите программы из списка")

    # ---------- Winget ----------
    def _check_winget(self):
        if winget_available():
            ver = get_winget_version() or "?"
            self.status_lbl.configure(text=f"winget v{ver} — готов к работе")
        else:
            self.status_lbl.configure(text="winget не найден", text_color="#d64545")
            self.install_btn.configure(state="disabled")
            self._append_log(
                "winget не найден. Установите App Installer из Microsoft Store "
                "или выполните: winget — и перезапустите Ninster.\n")

    # ---------- Установка ----------
    def _start_install(self):
        if self.installing:
            return
        selected = [a.id for a in CATALOG if self.vars[a.id].get()]
        if not selected:
            return
        self.installing = True
        self.total = len(selected)
        self.finished = 0
        self.progress.set(0)
        self._show_log(True)

        for aid in selected:
            self._set_status(aid, Status.QUEUED)
        self._set_controls(False)
        self.status_lbl.configure(text=f"Установка 0 из {self.total}…", text_color="gray70")
        self._append_log(f"=== Запуск установки {self.total} программ ===\n")

        self.installer = Installer(
            selected,
            per_user=False,
            on_event=self._on_event,
            on_log=self._on_log,
            on_finish=self._on_finish,
        )
        self.installer.start()

    def _on_event(self, app_id, status, detail):
        self.after(0, lambda: self._apply_event(app_id, status, detail))

    def _apply_event(self, app_id, status, detail):
        name = self.rows[app_id]["app"].name
        color, _ = STATUS_META[status]
        self._set_status(app_id, status)
        if status in (Status.DONE, Status.ERROR, Status.SKIPPED):
            self.finished += 1
            self.progress.set(self.finished / self.total)
            self.status_lbl.configure(
                text=f"Установка {self.finished} из {self.total}…", text_color="gray70")
        self._append_log(f"[{name}] {detail}\n")

    def _on_log(self, app_id, line):
        self.log_queue.put((app_id, line))

    def _on_finish(self, summary):
        self.after(0, lambda: self._apply_finish(summary))

    def _apply_finish(self, s):
        self.installing = False
        self._set_controls(True)
        self.progress.set(1)
        ok = s["done"]
        err = s["errors"]
        skipped = s["skipped"]
        self.status_lbl.configure(
            text=f"Готово: {ok} успешно, {err} с ошибками" + (f", {skipped} пропущено" if skipped else ""),
            text_color="#2e9e5b" if err == 0 else "#d99a1b")
        self._append_log(f"=== Завершено: {ok} успешно, {err} с ошибками ===\n")
        self._refresh_count()
        self._show_summary(ok, err, skipped)

    def _show_summary(self, ok, err, skipped):
        dlg = ctk.CTkToplevel(self)
        dlg.title("Установка завершена")
        dlg.geometry("360x180")
        dlg.transient(self)
        dlg.grab_set()
        dlg.grid_columnconfigure(0, weight=1)
        head = "Всё установлено успешно ✓" if err == 0 else "Установка завершена с ошибками"
        ctk.CTkLabel(dlg, text=head, font=("Segoe UI Semibold", 16)).grid(
            row=0, column=0, padx=20, pady=(20, 8))
        body = f"Успешно: {ok}\nС ошибками: {err}"
        if skipped:
            body += f"\nПропущено: {skipped}"
        ctk.CTkLabel(dlg, text=body, font=FONT_SUB, text_color="gray70").grid(
            row=1, column=0, padx=20, pady=(0, 12))
        ctk.CTkButton(dlg, text="ОК", width=120, command=dlg.destroy).grid(
            row=2, column=0, padx=20, pady=(0, 20))

    def _set_status(self, app_id, status):
        color, text = STATUS_META[status]
        lbl = self.rows[app_id]["status_lbl"]
        lbl.configure(text=text, text_color=color)

    def _set_controls(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.install_btn.configure(
            state="normal" if (enabled and self.selected_count) else "disabled")
        self.select_all_btn.configure(state=state)
        self.clear_btn.configure(state=state)
        self.search_entry.configure(state=state)
        self.cat_menu.configure(state=state)

    # ---------- Журнал ----------
    def _toggle_log(self):
        self._show_log(not self.log_visible)

    def _show_log(self, visible: bool):
        if visible and not self.log_visible:
            self.log_text.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(6, 4))
            self.log_btn.configure(text="Журнал ▴")
            self.log_visible = True
        elif not visible and self.log_visible:
            self.log_text.grid_remove()
            self.log_btn.configure(text="Журнал ▾")
            self.log_visible = False

    def _append_log(self, text: str):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text)
        # Ограничиваем объём журнала
        if int(self.log_text.index("end-1c").split(".")[0]) > 3000:
            self.log_text.delete("1.0", "1000.0")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _drain_log(self):
        drained = 0
        while drained < 500:
            try:
                app_id, line = self.log_queue.get_nowait()
            except queue.Empty:
                break
            name = self.rows.get(app_id, {}).get("app").name if app_id in self.rows else app_id
            # Пропускаем строки-прогресс-бары winget (спиннеры/проценты)
            if not (len(line) < 60 and line.replace(".", "").replace(" ", "").isdigit()):
                self._append_log(f"  {name}: {line}\n")
            drained += 1
        self.after(150, self._drain_log)


def main():
    _ensure_admin()
    app = NinsterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
