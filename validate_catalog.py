"""Проверяет, что все winget ID из catalog.py существуют в репозитории winget.

Запуск:  python validate_catalog.py
Печатает список ID, которые winget не находит.
"""

import subprocess
import sys

from catalog import CATALOG


def exists(app_id: str) -> bool:
    try:
        proc = subprocess.run(
            ["winget", "show", "--id", app_id, "--exact",
             "--accept-source-agreements"],
            capture_output=True, text=True, timeout=60,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return proc.returncode == 0
    except Exception:
        return False


def main():
    missing = []
    total = len(CATALOG)
    for i, app in enumerate(CATALOG, 1):
        ok = exists(app.id)
        mark = "ok" if ok else "MISSING"
        print(f"[{i}/{total}] {app.id:40s} {mark}")
        if not ok:
            missing.append(app)
    print("\n" + "=" * 60)
    if missing:
        print(f"Не найдено {len(missing)} ID:")
        for app in missing:
            print(f"  {app.id}  ({app.name})")
    else:
        print("Все ID найдены ✓")


if __name__ == "__main__":
    main()
