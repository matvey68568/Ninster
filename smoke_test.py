"""Дымовой тест GUI: создаёт окно, проверяет построение, затем закрывает.

Запуск:  python smoke_test.py
Возвращает 0 при успехе.
"""

import sys

import main as m
from catalog import CATALOG


def run():
    app = m.NinsterApp()
    app.update()  # обработать построение

    assert len(app.rows) == len(CATALOG), f"строк {len(app.rows)} != каталога {len(CATALOG)}"

    # Имитация выбора первой программы
    first = CATALOG[0].id
    app.vars[first].set(True)
    app._on_toggle(first)
    app.update()
    assert app.selected_count == 1, f"selected_count={app.selected_count}"

    # Фильтр по несуществующей строке — всё скрыто
    app.search_var.set("zzz_не_существует_zzz")
    app.update()
    assert len(app._visible_ids()) == 0

    # Сброс фильтра
    app.search_var.set("")
    app.update()
    assert len(app._visible_ids()) == len(CATALOG)

    # Прогресс-бар и статус доступны
    app.progress.set(0.5)
    app.update()

    app.destroy()
    print("Smoke test OK")
    return 0


if __name__ == "__main__":
    sys.exit(run())
