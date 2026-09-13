@echo off
title Code Review Bot
color 0A
mode con: cols=80 lines=30

echo.
echo ========================================
echo   CODE REVIEW BOT - LAUNCHING
echo ========================================
echo.

setlocal enabledelayedexpansion

for /f "tokens=*" %%A in ("%~dp0.") do set "SCRIPT_DIR=%%~fA"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ERROR: Python not installed!
    echo.
    echo Please install Python 3.8+ from: https://python.org
    echo Make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Check Node
node --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ERROR: Node.js not installed!
    echo.
    echo Please install Node.js 16+ LTS from: https://nodejs.org
    echo.
    pause
    exit /b 1
)

REM Setup and start backend
cd /d "%SCRIPT_DIR%\backend"

if not exist "venv" (
    echo Creating Python environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Python packages...
    pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt >nul 2>&1
)

echo Starting backend...
start /b python app.py >nul 2>&1

timeout /t 3 /nobreak >nul 2>&1

REM Setup and start frontend
cd /d "%SCRIPT_DIR%\frontend"

if not exist "node_modules" (
    echo Installing npm packages...
    call npm install >nul 2>&1
)

echo Starting frontend...
start "Code Review Bot Frontend" cmd /k npm run dev

REM Wait and open
timeout /t 5 /nobreak >nul 2>&1

echo.
echo ========================================
echo   OPENING APPLICATION...
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:5000
echo.
echo Press Ctrl+C to stop
echo.

start http://localhost:3000
timeout /t 2 /nobreak >nul 2>&1

exit /b 0
