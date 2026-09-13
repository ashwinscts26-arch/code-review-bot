@echo off
REM Code Review Bot - One-Click Starter (Windows)

setlocal enabledelayedexpansion

echo ================================
echo 🚀 Code Review Bot - Starting...
echo ================================
echo.

REM Get script directory
set SCRIPT_DIR=%~dp0

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo ✓ Python found

REM Check Node
echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js 16+
    pause
    exit /b 1
)
echo ✓ Node.js found

REM Setup Backend
echo.
echo Setting up backend...
cd /d "%SCRIPT_DIR%backend"

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -q -r requirements.txt
)
echo ✓ Backend ready

REM Setup Frontend
echo Setting up frontend...
cd /d "%SCRIPT_DIR%frontend"

if not exist "node_modules" (
    echo Installing npm packages...
    npm install
)
echo ✓ Frontend ready

REM Start Backend
echo.
echo Starting backend on port 5000...
cd /d "%SCRIPT_DIR%backend"
call venv\Scripts\activate.bat
start /b "Code Review Bot - Backend" python app.py
echo ✓ Backend started

REM Wait for backend
echo Waiting for backend to be ready...
timeout /t 3 /nobreak

REM Start Frontend
echo Starting frontend on port 3000...
cd /d "%SCRIPT_DIR%frontend"
start "Code Review Bot - Frontend" cmd /k npm run dev
echo ✓ Frontend started

REM Wait for frontend
timeout /t 5 /nobreak

REM Open browser
echo Opening browser...
start http://localhost:3000

echo.
echo ================================
echo ✓ Application Started!
echo ================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:5000
echo.
echo Close these windows to stop the application.
echo.
pause

