[Setup]
AppName=NotionPresence
AppVersion=1.0.1
AppPublisher=CrypterENC
AppPublisherURL=https://github.com/CrypterENC/Notion-Rich-Presence
AppSupportURL=https://github.com/CrypterENC/Notion-Rich-Presence/issues
DefaultDirName={localappdata}\NotionPresence
DefaultGroupName=NotionPresence
PrivilegesRequired=lowest
OutputDir=userdocs:Inno Setup Output
OutputBaseFilename=NotionPresence_Installer
Compression=lzma
SolidCompression=yes
SetupIconFile=Assets\Notion.ico
UninstallDisplayIcon={app}\NotionPresence.exe
WizardStyle=modern


[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"
Name: "startup"; Description: "Run NotionPresence on system startup"; GroupDescription: "Startup options:"; Flags: unchecked

[Files]
Source: "dist\NotionPresence\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\NotionPresence"; Filename: "{app}\NotionPresence.exe"; IconFilename: "{app}\NotionPresence.exe"; IconIndex: 0
Name: "{commondesktop}\NotionPresence"; Filename: "{app}\NotionPresence.exe"; IconFilename: "{app}\NotionPresence.exe"; IconIndex: 0; Tasks: desktopicon
Name: "{userstartup}\NotionPresence"; Filename: "{app}\NotionPresence.exe"; IconFilename: "{app}\NotionPresence.exe"; IconIndex: 0; Tasks: startup

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "NotionPresence"; ValueData: "{app}\NotionPresence.exe"; Tasks: startup
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\NotionPresence"; ValueType: string; ValueName: "DisplayName"; ValueData: "Notion Discord Auto RPC"
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\NotionPresence"; ValueType: string; ValueName: "DisplayVersion"; ValueData: "1.0.0"
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\NotionPresence"; ValueType: string; ValueName: "Publisher"; ValueData: "CrypterENC"
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\NotionPresence"; ValueType: string; ValueName: "UninstallString"; ValueData: "{uninstallexe}"

[Run]
Filename: "{app}\NotionPresence.exe"; Description: "Launch NotionPresence"; Flags: nowait postinstall skipifsilent

[CustomMessages]
WelcomeLabel1=Welcome to NotionPresence Setup
WelcomeLabel2=Notion Discord Auto RPC - Display your Notion page as Discord Rich Presence%n%nAuthor: CrypterENC%nVersion: 1.0.0%nRepository: https://github.com/CrypterENC/Notion-Rich-Presence%n%nThis application allows you to display your current Notion page as your Discord Rich Presence status.%n%nClick Next to continue with the installation.
