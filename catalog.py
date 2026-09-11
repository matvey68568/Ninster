"""Каталог программ: имя, winget ID, категория, краткое описание."""

from dataclasses import dataclass


@dataclass(frozen=True)
class App:
    id: str            # winget package identifier
    name: str          # отображаемое имя
    category: str      # ключ категории из CATEGORIES
    description: str = ""


CATEGORIES = {
    "browsers":   "Браузеры",
    "messaging":  "Мессенджеры и связь",
    "office":     "Офис и документы",
    "media":      "Медиа и стриминг",
    "graphics":   "Графика и дизайн",
    "dev":        "Разработка",
    "utils":      "Утилиты",
    "security":   "Безопасность и VPN",
    "archivers":  "Архиваторы",
    "cloud":      "Облако и хранение",
    "games":      "Игры и игровые платформы",
}

# Каждая запись: App("<winget id>", "Название", "категория", "описание")
CATALOG = [
    # ---------- Браузеры ----------
    App("Google.Chrome", "Google Chrome", "browsers", "Самый популярный браузер"),
    App("Mozilla.Firefox", "Mozilla Firefox", "browsers", "Браузер с упором на приватность"),
    App("Microsoft.Edge", "Microsoft Edge", "browsers", "Браузер на движке Chromium от Microsoft"),
    App("Brave.Brave", "Brave", "browsers", "Браузер с блокировкой рекламы и трекеров"),
    App("Opera.Opera", "Opera", "browsers", "Браузер со встроенным VPN"),
    App("Opera.OperaGX", "Opera GX", "browsers", "Браузер для геймеров"),
    App("Vivaldi.Vivaldi", "Vivaldi", "browsers", "Гибкий браузер для опытных пользователей"),
    App("DuckDuckGo.DesktopBrowser", "DuckDuckGo", "browsers", "Приватный браузер от DuckDuckGo"),
    App("LibreWolf.LibreWolf", "LibreWolf", "browsers", "Firefox с усиленной приватностью"),
    App("Waterfox.Waterfox", "Waterfox", "browsers", "Независимый форк Firefox"),

    # ---------- Мессенджеры ----------
    App("Discord.Discord", "Discord", "messaging", "Голос, чат и сообщества"),
    App("Telegram.TelegramDesktop", "Telegram", "messaging", "Популярный мессенджер"),
    App("9NKSQGP7F2NH", "WhatsApp", "messaging", "Мессенджер от Meta (Microsoft Store)"),
    App("OpenWhisperSystems.Signal", "Signal", "messaging", "Максимально защищённый мессенджер"),
    App("SlackTechnologies.Slack", "Slack", "messaging", "Корпоративный мессенджер"),
    App("Microsoft.Teams", "Microsoft Teams", "messaging", "Командная связь и видеозвонки"),
    App("Zoom.Zoom", "Zoom", "messaging", "Видеоконференции"),
    App("Rakuten.Viber", "Viber", "messaging", "Мессенджер и звонки"),
    App("Element.Element", "Element", "messaging", "Клиент Matrix с шифрованием"),
    App("Session.Session", "Session", "messaging", "Анонимный мессенджер без номера телефона"),
    App("TeamSpeakSystems.TeamSpeakClient", "TeamSpeak", "messaging", "Голосовой чат для команд"),

    # ---------- Офис ----------
    App("TheDocumentFoundation.LibreOffice", "LibreOffice", "office", "Бесплатный офисный пакет"),
    App("ONLYOFFICE.DesktopEditors", "ONLYOFFICE", "office", "Офисный пакет, совместимый с MS Office"),
    App("Apache.OpenOffice", "Apache OpenOffice", "office", "Классический офисный пакет"),
    App("Notion.Notion", "Notion", "office", "Заметки, базы и wiki"),
    App("Obsidian.Obsidian", "Obsidian", "office", "Заметки на локальных markdown-файлах"),
    App("Joplin.Joplin", "Joplin", "office", "Заметки с синхронизацией"),
    App("Kingsoft.WPSOffice", "WPS Office", "office", "Лёгкий офисный пакет"),
    App("SoftMaker.Office.2024", "SoftMaker Office 2024", "office", "Офисный пакет SoftMaker"),
    App("Xmind.Xmind", "Xmind", "office", "Интеллект-карты"),
    App("Adobe.Acrobat.Reader.64-bit", "Adobe Acrobat Reader", "office", "Просмотр PDF от Adobe"),
    App("Foxit.FoxitReader", "Foxit PDF Reader", "office", "Быстрый просмотр PDF"),
    App("SumatraPDF.SumatraPDF", "SumatraPDF", "office", "Минималистичный просмотрщик PDF"),

    # ---------- Медиа ----------
    App("VideoLAN.VLC", "VLC Media Player", "media", "Универсальный видеоплеер"),
    App("clsid2.mpc-hc", "MPC-HC", "media", "Лёгкий видеоплеер"),
    App("Daum.PotPlayer", "PotPlayer", "media", "Мощный видеоплеер"),
    App("Spotify.Spotify", "Spotify", "media", "Музыкальный стриминг"),
    App("Audacity.Audacity", "Audacity", "media", "Редактор аудио"),
    App("OBSProject.OBSStudio", "OBS Studio", "media", "Запись экрана и стриминг"),
    App("Gyan.FFmpeg", "FFmpeg", "media", "Набор инструментов для аудио/видео"),
    App("XBMCFoundation.Kodi", "Kodi", "media", "Медиацентр"),
    App("Plex.Plex", "Plex", "media", "Медиасервер и плеер"),
    App("Apple.iTunes", "iTunes", "media", "Медиатека и синхронизация Apple"),
    App("Musescore.Musescore", "MuseScore", "media", "Нотный редактор"),
    App("HandBrake.HandBrake", "HandBrake", "media", "Конвертация видео"),
    App("PeterPawlowski.foobar2000", "foobar2000", "media", "Продвинутый аудиоплеер"),
    App("AIMP.AIMP", "AIMP", "media", "Аудиоплеер с эквалайзером"),
    App("Winamp.Winamp", "Winamp", "media", "Легендарный аудиоплеер"),
    App("Stremio.Stremio", "Stremio", "media", "Агрегатор фильмов и сериалов"),

    # ---------- Графика ----------
    App("GIMP.GIMP", "GIMP", "graphics", "Бесплатный растровый редактор"),
    App("Inkscape.Inkscape", "Inkscape", "graphics", "Векторная графика"),
    App("BlenderFoundation.Blender", "Blender", "graphics", "3D-моделирование и анимация"),
    App("KDE.Krita", "Krita", "graphics", "Рисование и цифровая живопись"),
    App("dotPDN.PaintDotNet", "paint.net", "graphics", "Лёгкий растровый редактор"),
    App("ShareX.ShareX", "ShareX", "graphics", "Скриншоты и запись экрана"),
    App("IrfanSkiljan.IrfanView", "IrfanView", "graphics", "Быстрый просмотр изображений"),
    App("XnSoft.XnViewMP", "XnView MP", "graphics", "Просмотр и конвертация изображений"),
    App("Figma.Figma", "Figma", "graphics", "Дизайн интерфейсов"),
    App("darktable.darktable", "darktable", "graphics", "Обработка RAW-фото"),
    App("RawTherapee.RawTherapee", "RawTherapee", "graphics", "Обработка RAW-фото"),
    App("LibreCAD.LibreCAD", "LibreCAD", "graphics", "2D-САПР"),
    App("FreeCAD.FreeCAD", "FreeCAD", "graphics", "Параметрическое 3D-моделирование"),
    App("Greenshot.Greenshot", "Greenshot", "graphics", "Скриншоты с аннотациями"),
    App("NickeManarin.ScreenToGif", "ScreenToGif", "graphics", "Запись экрана в GIF"),

    # ---------- Разработка ----------
    App("Microsoft.VisualStudioCode", "Visual Studio Code", "dev", "Популярный редактор кода"),
    App("Notepad++.Notepad++", "Notepad++", "dev", "Текстовый редактор"),
    App("vim.vim", "Vim", "dev", "Классический редактор из терминала"),
    App("Git.Git", "Git", "dev", "Система контроля версий"),
    App("GitHub.GitHubDesktop", "GitHub Desktop", "dev", "GUI-клиент для GitHub"),
    App("GitHub.cli", "GitHub CLI", "dev", "GitHub из терминала"),
    App("Python.Python.3.12", "Python 3.12", "dev", "Язык программирования Python"),
    App("OpenJS.NodeJS.LTS", "Node.js LTS", "dev", "Среда выполнения JavaScript"),
    App("EclipseAdoptium.Temurin.21.JDK", "Temurin JDK 21", "dev", "OpenJDK от Eclipse Adoptium"),
    App("JetBrains.PyCharm.Community", "PyCharm Community", "dev", "IDE для Python"),
    App("JetBrains.IntelliJIDEA.Community", "IntelliJ IDEA Community", "dev", "IDE для Java/Kotlin"),
    App("JetBrains.Toolbox", "JetBrains Toolbox", "dev", "Управление IDE от JetBrains"),
    App("SublimeHQ.SublimeText.4", "Sublime Text 4", "dev", "Лёгкий редактор кода"),
    App("Docker.DockerDesktop", "Docker Desktop", "dev", "Контейнеризация"),
    App("Postman.Postman", "Postman", "dev", "Тестирование API"),
    App("Insomnia.Insomnia", "Insomnia", "dev", "REST-клиент"),
    App("PuTTY.PuTTY", "PuTTY", "dev", "SSH/терминал клиент"),
    App("WinSCP.WinSCP", "WinSCP", "dev", "Передача файлов по SFTP/SCP"),
    App("DBeaver.DBeaver.Community", "DBeaver", "dev", "Универсальный SQL-клиент"),
    App("Microsoft.WindowsTerminal", "Windows Terminal", "dev", "Современный терминал"),
    App("Microsoft.VisualStudio.2022.Community", "Visual Studio 2022", "dev", "Полноценная IDE от Microsoft"),
    App("Kitware.CMake", "CMake", "dev", "Система сборки"),
    App("GoLang.Go", "Go", "dev", "Язык программирования Go"),
    App("Rustlang.Rustup", "Rust", "dev", "Язык программирования Rust"),
    App("Oracle.VirtualBox", "VirtualBox", "dev", "Виртуальные машины"),

    # ---------- Утилиты ----------
    App("Microsoft.PowerToys", "PowerToys", "utils", "Набор утилит для Windows"),
    App("voidtools.Everything", "Everything", "utils", "Мгновенный поиск файлов"),
    App("Rufus.Rufus", "Rufus", "utils", "Создание загрузочных флешек"),
    App("CPUID.CPU-Z", "CPU-Z", "utils", "Информация о процессоре"),
    App("TechPowerUp.GPU-Z", "GPU-Z", "utils", "Информация о видеокарте"),
    App("REALiX.HWiNFO", "HWiNFO", "utils", "Мониторинг системы"),
    App("CrystalDewWorld.CrystalDiskInfo", "CrystalDiskInfo", "utils", "Здоровье дисков"),
    App("CrystalDewWorld.CrystalDiskMark", "CrystalDiskMark", "utils", "Скорость дисков"),
    App("qBittorrent.qBittorrent", "qBittorrent", "utils", "Торрент-клиент"),
    App("Ventoy.Ventoy", "Ventoy", "utils", "Мультизагрузочная флешка"),
    App("Balena.Etcher", "balenaEtcher", "utils", "Запись образов на флешки"),
    App("Microsoft.Sysinternals.ProcessExplorer", "Process Explorer", "utils", "Продвинутый диспетчер задач"),
    App("Microsoft.Sysinternals.Autoruns", "Autoruns", "utils", "Управление автозагрузкой"),
    App("JAMSoftware.TreeSize.Free", "TreeSize Free", "utils", "Анализ занятого места"),
    App("Piriform.CCleaner", "CCleaner", "utils", "Очистка системы"),
    App("File-New-Project.EarTrumpet", "EarTrumpet", "utils", "Управление громкостью по приложениям"),
    App("9PM860492SZD", "Microsoft PC Manager", "utils", "Оптимизация Windows (Microsoft Store)"),
    App("TeamViewer.TeamViewer", "TeamViewer", "utils", "Удалённый доступ"),
    App("AnyDesk.AnyDesk", "AnyDesk", "utils", "Удалённый доступ"),

    # ---------- Безопасность ----------
    App("Bitwarden.Bitwarden", "Bitwarden", "security", "Менеджер паролей"),
    App("KeePassXCTeam.KeePassXC", "KeePassXC", "security", "Офлайн-менеджер паролей"),
    App("WireGuard.WireGuard", "WireGuard", "security", "Современный VPN-туннель"),
    App("OpenVPNTechnologies.OpenVPN", "OpenVPN", "security", "VPN-клиент"),
    App("Proton.ProtonVPN", "Proton VPN", "security", "VPN с фокусом на приватность"),
    App("Proton.ProtonMail", "Proton Mail", "security", "Защищённая почта"),
    App("Malwarebytes.Malwarebytes", "Malwarebytes", "security", "Антивирус и антишпион"),
    App("Tailscale.Tailscale", "Tailscale", "security", "Приватная mesh-сеть"),

    # ---------- Архиваторы ----------
    App("7zip.7zip", "7-Zip", "archivers", "Свободный архиватор"),
    App("RARLab.WinRAR", "WinRAR", "archivers", "Популярный архиватор"),
    App("M2Team.NanaZip", "NanaZip", "archivers", "Архиватор в стиле Windows 11"),
    App("Giorgiotani.Peazip", "PeaZip", "archivers", "Архиватор с широкой поддержкой форматов"),

    # ---------- Облако ----------
    App("Google.GoogleDrive", "Google Drive", "cloud", "Облачное хранилище Google"),
    App("Dropbox.Dropbox", "Dropbox", "cloud", "Облачное хранилище"),
    App("Microsoft.OneDrive", "OneDrive", "cloud", "Облако от Microsoft"),
    App("Mega.MEGASync", "MEGA", "cloud", "Облако со сквозным шифрованием"),
    App("Nextcloud.NextcloudDesktop", "Nextcloud", "cloud", "Собственное облако"),
    App("pCloudAG.pCloudDrive", "pCloud", "cloud", "Облачное хранилище"),

    # ---------- Игры ----------
    App("Valve.Steam", "Steam", "games", "Крупнейший игровой магазин"),
    App("EpicGames.EpicGamesLauncher", "Epic Games Launcher", "games", "Магазин Epic Games"),
    App("GOG.Galaxy", "GOG Galaxy", "games", "Магазин без DRM"),
    App("Ubisoft.Connect", "Ubisoft Connect", "games", "Лаунчер Ubisoft"),
    App("ElectronicArts.EADesktop", "EA app", "games", "Лаунчер Electronic Arts"),
    App("Parsec.Parsec", "Parsec", "games", "Облачный гейминг"),
    App("PrismLauncher.PrismLauncher", "Prism Launcher", "games", "Лаунчер Minecraft"),
    App("HeroicGamesLauncher.HeroicGamesLauncher", "Heroic Games Launcher", "games", "Открытый лаунчер Epic/GOG"),

    # ---------- Системные библиотеки ----------
    App("Microsoft.VCRedist.2015+.x64", "VC++ Redistributable", "utils", "Библиотеки для многих программ"),
    App("Microsoft.DotNet.DesktopRuntime.8", ".NET Desktop Runtime 8", "utils", "Среда выполнения .NET"),
]

# Сортировка внутри категорий по имени для аккуратного списка
CATALOG.sort(key=lambda a: (list(CATEGORIES).index(a.category), a.name.lower()))
