[Setup]
AppId=lucasseib.Cateno
AppName=Cateno
AppVersion=2.0.0
AppPublisher=Lucas Seib
AppPublisherURL=https://github.com/lucasseib/cateno

DefaultDirName={localappdata}\Programs\Cateno
PrivilegesRequired=lowest
DisableDirPage=yes
DisableProgramGroupPage=yes

OutputDir=dist\instalador
OutputBaseFilename=Cateno-Setup-2.0.0
SetupIconFile=cateno.ico
UninstallDisplayIcon={app}\Cateno.exe

Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "dist\v2\Cateno\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Criar um atalho na Área de Trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked

[Icons]
Name: "{userprograms}\Cateno"; Filename: "{app}\Cateno.exe"; WorkingDir: "{app}"
Name: "{userdesktop}\Cateno"; Filename: "{app}\Cateno.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\Cateno.exe"; Description: "Abrir o Cateno"; Flags: nowait postinstall skipifsilent