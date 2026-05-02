@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Starting Full Application
echo ========================================
echo.

echo Checking port 3001...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3001 ^| findstr LISTENING') do (
    echo Port 3001 is occupied by process %%a, terminating...
    taskkill /F /PID %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
)

echo Checking port 3000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    echo Port 3000 is occupied by process %%a, terminating...
    taskkill /F /PID %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
)

echo.
echo Starting backend server...
start "Backend Server - Port 3001" cmd /k "%~dp0start-backend.bat"

timeout /t 3 /nobreak >nul

echo Starting frontend server...
start "Frontend Server - Port 3000" cmd /k "%~dp0start-frontend.bat"

echo.
echo ========================================
echo   All services started!
echo ========================================
echo.
echo Backend:  http://localhost:3001
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window (services will keep running)
pause >nul
