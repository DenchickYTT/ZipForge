; Скрипт установщика для ZipForge v1.2.0
#define MyAppName "ZipForge"
#define MyAppVersion "1.2.0"
#define MyAppPublisher "DenchickYTT"
#define MyAppURL "https://github.com/DenchickYTT/ZipForge"
#define MyAppExeName "ZipForge.exe"

[Setup]
AppId={{B7A6F3D2-9C4E-4A1B-8F5D-2E7C9A3B6F1D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer_output
OutputBaseFilename=ZipForge_Setup_v{#MyAppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
SetupIconFile=resources\icon.ico

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\ZipForge.exe"; DestDir: "{app}"; Flags: ignoreversion
; Если хочешь добавить иконки в установку (не обязательно):
; Source: "resources\icon.ico"; DestDir: "{app}\resources"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
; --- АССОЦИАЦИЯ ДЛЯ ZIP ---
Root: HKCU; Subkey: "Software\Classes\ZipForge.zip"; ValueType: string; ValueName: ""; ValueData: "ZipForge Archive"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\ZipForge.zip\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\ZipForge.exe,0"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\ZipForge.zip\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\ZipForge.exe"" ""%1"""; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\.zip"; ValueType: string; ValueName: ""; ValueData: "ZipForge.zip"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\.zip\OpenWithProgids"; ValueType: string; ValueName: "ZipForge.zip"; ValueData: ""; Flags: uninsdeletevalue

; --- ДРУЖЕСТВЕННОЕ ИМЯ (чтобы не было "python") ---
Root: HKCU; Subkey: "Software\Classes\Applications\ZipForge.exe"; ValueType: string; ValueName: "FriendlyAppName"; ValueData: "ZipForge"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\Applications\ZipForge.exe\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\ZipForge.exe"" ""%1"""; Flags: uninsdeletekey