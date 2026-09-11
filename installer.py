"""Движок установки через winget (фоновый поток)."""

import re
import shutil
import subprocess
import threading
from enum import Enum


class Status(Enum):
    QUEUED = "queued"
    INSTALLING = "installing"
    DONE = "done"
    ERROR = "error"
    SKIPPED = "skipped"


_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def _clean(s: str) -> str:
    """Убирает ANSI-коды, служебные символы и пустые строки."""
    s = _ANSI_RE.sub("", s)
    s = s.replace("\r", " ").replace("\x08", "").strip()
    return s


def winget_available() -> bool:
    return shutil.which("winget") is not None


def get_winget_version() -> str | None:
    try:
        out = subprocess.run(
            ["winget", "--version"],
            capture_output=True, text=True, timeout=15,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return out.stdout.strip() if out.returncode == 0 else None
    except Exception:
        return None


def build_args(app_id: str, per_user: bool) -> list[str]:
    args = [
        "winget", "install", "--id", app_id,
        "--exact",
        "--silent",
        "--accept-package-agreements",
        "--accept-source-agreements",
        "--disable-interactivity",
    ]
    if per_user:
        args += ["--scope", "user"]
    return args


class Installer(threading.Thread):
    """Последовательно ставит пакеты через winget.

    Колбэки вызываются из фонового потока:
      on_event(app_id, Status, detail)
      on_log(app_id, line)
      on_finish(summary_dict)
    """

    def __init__(self, app_ids, per_user=False, on_event=None, on_log=None, on_finish=None):
        super().__init__(daemon=True)
        self.app_ids = list(app_ids)
        self.per_user = per_user
        self.on_event = on_event or (lambda *a: None)
        self.on_log = on_log or (lambda *a: None)
        self.on_finish = on_finish or (lambda s: None)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def run(self):
        done = 0
        errors = 0
        skipped = 0
        for app_id in self.app_ids:
            if self._stop.is_set():
                self.on_event(app_id, Status.SKIPPED, "Отменено")
                skipped += 1
                continue
            self.on_event(app_id, Status.INSTALLING, "Установка…")
            rc = self._install(app_id)
            if rc == 0:
                self.on_event(app_id, Status.DONE, "Установлено")
                done += 1
            else:
                self.on_event(app_id, Status.ERROR, f"Ошибка (код {rc})")
                errors += 1
        self.on_finish({"done": done, "errors": errors, "skipped": skipped, "total": len(self.app_ids)})

    def _install(self, app_id: str) -> int:
        args = build_args(app_id, self.per_user)
        try:
            proc = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except Exception as e:
            self.on_log(app_id, f"Не удалось запустить winget: {e}")
            return -1

        assert proc.stdout is not None
        for raw in proc.stdout:
            if self._stop.is_set():
                proc.terminate()
                break
            line = _clean(raw)
            if line:
                self.on_log(app_id, line)
        proc.wait()
        return proc.returncode
