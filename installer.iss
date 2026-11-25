; Скрипт установщика для ZipForge
#define MyAppName "ZipForge"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "ZipForge"
#define MyAppURL "https://github.com/DenchickYTT/ZipForge"
#define MyAppExeName "ZipForge.exe"

[Setup]
; Уникальный ID приложения (не меняй его после первой установки!)
AppId={{B7A6F3D2-9C4E-4A1B-8F5D-2E7C9A3B6F1D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
; Куда ставить по умолчанию (Program Files)
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Лицензия (файл LICENSE должен лежать в корне проекта)
LicenseFile=LICENSE
; Куда сохранять готовый установщик
OutputDir=installer_output
OutputBaseFilename=ZipForge_Setup_v{#MyAppVersion}
; Сжатие
Compression=lzma2
SolidCompression=yes
; Стиль мастера установки
WizardStyle=modern
; Требовать права администратора (для записи в Program Files)
PrivilegesRequired=admin
; Иконка для самого установщика
SetupIconFile=resources\icon.ico

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
; Задача: создать ярлык на рабочем столе
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Копируем наш собранный EXE из папки dist в папку установки
Source: "dist\ZipForge.exe"; DestDir: "{app}"; Flags: ignoreversion
; Если у тебя есть другие файлы (например, лицензия), их тоже можно добавить:
; Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Ярлык в меню Пуск
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Ярлык на рабочем столе (если выбрана задача)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Предложить запустить программу после установки
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
; --- АВТОМАТИЧЕСКАЯ РЕГИСТРАЦИЯ В WINDOWS ---
; Добавляем ZipForge в список "Открыть с помощью" для ZIP
Root: HKCU; Subkey: "Software\Classes\.zip\OpenWithProgids"; ValueType: string; ValueName: "ZipForge.zip"; ValueData: ""; Flags: uninsdeletevalue
; Создаём ProgID для ZipForge
Root: HKCU; Subkey: "Software\Classes\ZipForge.zip"; ValueType: string; ValueName: ""; ValueData: "ZipForge Archive"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\ZipForge.zip\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\ZipForge.exe,0"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\ZipForge.zip\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\ZipForge.exe"" ""%1"""; Flags: uninsdeletekey
; Дружественное имя для "Открыть с помощью"
Root: HKCU; Subkey: "Software\Classes\Applications\ZipForge.exe"; ValueType: string; ValueName: "FriendlyAppName"; ValueData: "ZipForge"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\Applications\ZipForge.exe\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\ZipForge.exe"" ""%1"""; Flags: uninsdeletekey