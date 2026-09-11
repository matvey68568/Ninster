"""Вшивает манифест requireAdministrator в готовый .exe через pefile.

Запускается из build.py ПОСЛЕ PyInstaller. Заменяет стандартный манифест
загрузчика (asInvoker) на наш, требующий права администратора.

Запуск:  python patch_manifest.py dist/Ninster.exe
"""

import sys
from pathlib import Path

import pefile

MANIFEST_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity version="1.0.0.0" processorArchitecture="*" name="Ninster" type="win32"/>
  <description>Ninster — установка программ в один клик</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application><supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/></application>
  </compatibility>
</assembly>
"""

RT_MANIFEST = 24


def patch(exe_path: Path) -> bool:
    pe = pefile.PE(str(exe_path))
    try:
        manifest_bytes = MANIFEST_XML.encode("utf-8")
        found = False
        for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
            if entry.id == RT_MANIFEST:
                for e2 in entry.directory.entries:
                    for e3 in e2.directory.entries:
                        data_rva = e3.data.struct.OffsetToData
                        size = e3.data.struct.Size
                        raw = pe.get_memory_mapped_image()[data_rva:data_rva + size]
                        if raw.startswith(b"\xff\xfe"):
                            new = MANIFEST_XML.encode("utf-16-le") + b"\x00\x00"
                        else:
                            new = manifest_bytes
                        if len(new) > size:
                            print(f"  Предупреждение: новый манифест ({len(new)} б) "
                                  f"больше старого ({size} б), пропуск", file=sys.stderr)
                            continue
                        pe.set_bytes_at_rva(data_rva, new + b"\x00" * (size - len(new)))
                        print("  Манифест обновлён → requireAdministrator")
                        found = True
        return found
    finally:
        pe.write(str(exe_path))
        pe.close()


def main():
    if len(sys.argv) < 2:
        print("Использование: python patch_manifest.py <путь к exe>", file=sys.stderr)
        sys.exit(2)
    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Файл не найден: {target}", file=sys.stderr)
        sys.exit(1)
    print(f"Патч манифеста: {target}")
    if patch(target):
        print("Готово: exe требует права администратора ✓")
    else:
        print("Манифест не найден в ресурсах exe", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
