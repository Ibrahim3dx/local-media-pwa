@echo off
setlocal

REM ====== Configuration ======
REM Change this to your media root folder (full Windows path)
if "%MEDIA_ROOT%"=="" set "MEDIA_ROOT=%USERPROFILE%\Videos"

REM Use Python embedded venv in .venv
set "VENV_DIR=.venv"

REM ====== Ensure venv ======
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [*] Creating virtual environment...
    py -3.12 -m venv "%VENV_DIR%"
)

REM ====== Install/Update deps ======
echo [*] Installing requirements (this may take a minute)...
"%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip >nul
"%VENV_DIR%\Scripts\python.exe" -m pip install -r requirements.txt

REM ====== Pick a free port via PowerShell ======
for /f "usebackq delims=" %%p in (`powershell -NoProfile -Command "$l=New-Object System.Net.Sockets.TcpListener([Net.IPAddress]::Loopback,0);$l.Start();$p=$l.LocalEndpoint.Port;$l.Stop();Write-Output $p"`) do set "PORT=%%p"

if "%PORT%"=="" set "PORT=8789"

REM ====== Start server ======
set "APP_DIR=%~dp0app"
set "PYTHONPATH=%~dp0"
set "HOST=0.0.0.0"

echo [*] Starting Local Media PWA on http://%COMPUTERNAME%:%PORT%  (bind %HOST%:%PORT%)
echo [*] Media root: %MEDIA_ROOT%

REM Write server URL for convenience
echo http://%HOST%:%PORT% > server-url.txt


"%~dp0%VENV_DIR%\Scripts\python.exe" -m uvicorn app.main:app --host %HOST% --port %PORT% --log-level info

endlocal
