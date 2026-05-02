@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Starting Backend Server (Port 3001)
echo ========================================
echo.

cd /d "%~dp0backend"

echo Checking port 3001...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3001 ^| findstr LISTENING') do (
    echo Port 3001 is occupied by process %%a, terminating...
    taskkill /F /PID %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
    echo Process terminated
)

if exist "venv\Scripts\python.exe" (
    echo Using virtual environment...
    call venv\Scripts\activate.bat
    cd src
    python app.py
) else (
    echo Using system Python...
    cd src
    python app.py
)

pause
