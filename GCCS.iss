; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "GCCS"
#define MyAppVersion "1.0"
#define MyAppPublisher "MotionSync Technologies"
#define MyAppExeName "Integrated.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{658C9D01-DAE7-443B-9D8A-9C036F571FE0}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=D:\Learning Plan\Gesture Control CS\license.txt
InfoBeforeFile=D:\Learning Plan\Gesture Control CS\preinstall.rtf
InfoAfterFile=D:\Learning Plan\Gesture Control CS\postinstall.rtf
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=D:\Learning Plan\Gesture Control CS
OutputBaseFilename=GCCS_WINDOWS_1.0_setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "installPython"; Description: "InstallPython"; GroupDescription: "Additional Installations"; Flags: unchecked
[Files]
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\aircanvasright\*"; DestDir: "{app}/aircanvasright"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\aircanvastop\*"; DestDir: "{app}/aircanvastop"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\icons\*"; DestDir: "{app}/icons"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\lib\*"; DestDir: "{app}/lib"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\modules\*"; DestDir: "{app}/modules"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\PyQt5.uic.widget-plugins\*"; DestDir: "{app}/PyQt5.uic.widget-plugins"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\splash\*"; DestDir: "{app}/splash"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\DOWNLOADS\python-3.12.1.exe"; DestDir: "{app}/python"; Flags: ignoreversion
Source: "D:\DOWNLOADS\python-3.12.1-amd64.exe"; DestDir: "{app}/python"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\msvcp140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\msvcp140_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\msvcp140_2.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\msvcp140_atomic_wait.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\msvcp140_codecvt_ids.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\python3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\python310.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\ucrtbase.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\vcamp140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\vccorlib140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\vcomp140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\vcruntime140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\vcruntime140_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-console-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-datetime-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-debug-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-errorhandling-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-file-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-file-l1-2-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-file-l2-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-handle-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-heap-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-interlocked-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-libraryloader-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-localization-l1-2-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-memory-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-namedpipe-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-processenvironment-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-processthreads-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-processthreads-l1-1-1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-profile-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-rtlsupport-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-string-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-synch-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-synch-l1-2-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-sysinfo-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-timezone-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-core-util-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-conio-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-convert-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-environment-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-filesystem-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-heap-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-locale-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-math-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-multibyte-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-private-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-process-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-runtime-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-stdio-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-string-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-time-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\api-ms-win-crt-utility-l1-1-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\concrt140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Learning Plan\Gesture Control CS\build\exe.win-amd64-3.10\d3dcompiler_47.dll"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
;Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent; Tasks: installPython


[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  PythonInstallerPath: String;
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Specify the path to the copied Python installer in the temp directory
    // Check if the third task is checked
    if WizardForm.TasksList.Checked[3] then
      begin
      // Check if the system is 64-bit
        if IsWin64 then
          PythonInstallerPath := ExpandConstant('{app}\python\python-3.12.1-amd64.exe')
        else
          PythonInstallerPath := ExpandConstant('{app}\python\python-3.12.1.exe');
        // Execute the Python installer with visible UI
        if not Exec(PythonInstallerPath, '/other_install_options', '', SW_SHOW, ewWaitUntilTerminated, ResultCode) then
          begin
          // Handle installation failure
            MsgBox('Failed to install Python. Error Code: ' + IntToStr(ResultCode), mbError, MB_OK);
            WizardForm.Close;
          end;
      end;
  end;
end;