"""Сборка Ninster в один .exe через PyInstaller.

Запуск:  python build.py
Результат:  dist/Ninster.exe
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
ICON = ROOT / "assets" / "icon.ico"

NAME = "Ninster"


def main():
    if not ICON.exists():
        print("Иконка не найдена, генерирую…")
        subprocess.run([sys.executable, str(ROOT / "make_icon.py")], check=True)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name", NAME,
        "--icon", str(ICON),
        "--collect-all", "customtkinter",
        "--collect-data", "customtkinter",
        str(ROOT / "main.py"),
    ]
    print("Запуск PyInstaller…")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)

    exe = ROOT / "dist" / f"{NAME}.exe"
    if exe.exists():
        size_mb = exe.stat().st_size / 1024 / 1024
        print(f"\nГотово: {exe} ({size_mb:.1f} МБ)")
    else:
        print("\nОшибка: exe не собран", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
