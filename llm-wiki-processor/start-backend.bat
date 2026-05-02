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

echo Searching for Python...
set PYTHON_PATH=

for /f "delims=" %%p in ('where python') do (
    echo Found Python: %%p
    echo Checking if %%p has required packages...
    "%%p" -c "import requests" >nul 2>&1
    if !errorlevel! equ 0 (
        set PYTHON_PATH=%%p
        echo Using this Python: !PYTHON_PATH!
        goto :found_good_python
    ) else (
        echo This Python doesn't have required packages, skipping...
    )
)

:found_good_python
if "%PYTHON_PATH%"=="" (
    echo ERROR: No valid Python found with required packages
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

cd src
"%PYTHON_PATH%" app.py

pause
