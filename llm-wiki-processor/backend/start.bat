@echo off

REM 进入脚本所在目录
cd /d "%~dp0"

REM 安装依赖
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

REM 进入 src 目录
cd src

REM 启动应用
echo Starting application...
echo Server will be available at http://localhost:3001
echo API documentation: http://localhost:3001/docs
echo Press Ctrl+C to stop the server
echo.

python app.py
