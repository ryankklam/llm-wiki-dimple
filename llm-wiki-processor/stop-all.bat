@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Stopping All Services
echo ========================================
echo.

echo Stopping backend server...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3001 ^| findstr LISTENING') do (
    echo Terminating process %%a (port 3001)
    taskkill /F /PID %%a >nul 2>&1
)

echo Stopping frontend server...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    echo Terminating process %%a (port 3000)
    taskkill /F /PID %%a >nul 2>&1
)

echo.
set /p stop_python="Stop all Python processes? (y/N): "
if /i "!stop_python!"=="y" (
    echo Stopping all Python processes...
    taskkill /F /IM python.exe >nul 2>&1
)

set /p stop_node="Stop all Node processes? (y/N): "
if /i "!stop_node!"=="y" (
    echo Stopping all Node processes...
    taskkill /F /IM node.exe >nul 2>&1
)

echo.
echo All services stopped
pause
