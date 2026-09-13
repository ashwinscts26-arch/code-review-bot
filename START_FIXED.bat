@echo off
REM Code Review Bot - One-Click Starter (Windows) - FIXED VERSION
setlocal enabledelayedexpansion

echo ================================
echo 🚀 Code Review Bot - Starting...
echo ================================
echo.

REM Get script directory
for /f "tokens=*" %%A in ("%~dp0.") do set "SCRIPT_DIR=%%~fA"

echo Script directory: %SCRIPT_DIR%
echo.

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
cd /d "%SCRIPT_DIR%\backend"

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Python dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ ERROR: Could not install Python dependencies
        echo Check that requirements.txt exists in: %SCRIPT_DIR%\backend
        pause
        exit /b 1
    )
)
echo ✓ Backend ready

REM Setup Frontend
echo.
echo Setting up frontend...
cd /d "%SCRIPT_DIR%\frontend"

if not exist "node_modules" (
    echo Installing npm packages...
    call npm install
    if errorlevel 1 (
        echo ❌ ERROR: Could not install npm packages
        echo Check that package.json exists in: %SCRIPT_DIR%\frontend
        pause
        exit /b 1
    )
)
echo ✓ Frontend ready

REM Start Backend
echo.
echo Starting backend on port 5000...
cd /d "%SCRIPT_DIR%\backend"
call venv\Scripts\activate.bat
start /b "Code Review Bot - Backend" python app.py
timeout /t 3 /nobreak
echo ✓ Backend started

REM Start Frontend
echo.
echo Starting frontend on port 3000...
cd /d "%SCRIPT_DIR%\frontend"
start "Code Review Bot - Frontend" cmd /k npm run dev
echo ✓ Frontend started

REM Wait and open browser
timeout /t 5 /nobreak
start http://localhost:3000

echo.
echo ================================
echo ✓ Application Started!
echo ================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:5000
echo.
echo Close the terminal to stop the application.
echo.

