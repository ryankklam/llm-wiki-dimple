@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Starting Frontend Server (Port 3000)
echo ========================================
echo.

cd /d "%~dp0frontend"

echo Checking port 3000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    echo Port 3000 is occupied by process %%a, terminating...
    taskkill /F /PID %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
    echo Process terminated
)

if not exist "node_modules" (
    echo First run, installing dependencies...
    npm install
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Starting frontend development server...
npm run dev

pause
