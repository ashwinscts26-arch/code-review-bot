#!/bin/bash
cd "$(dirname "$0")"

echo ""
echo "========================================"
echo "   CODE REVIEW BOT - LAUNCHING"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not installed!"
    echo ""
    echo "Install from: https://python.org"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js not installed!"
    echo ""
    echo "Install from: https://nodejs.org"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

# Setup backend
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python environment..."
    python3 -m venv venv
fi

source venv/bin/activate

if ! python -c "import flask" 2>/dev/null; then
    echo "Installing Python packages..."
    pip install --upgrade pip >/dev/null 2>&1
    pip install -r requirements.txt >/dev/null 2>&1
fi

echo "Starting backend..."
python app.py >/dev/null 2>&1 &
BACKEND_PID=$!

sleep 3

# Setup frontend
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install >/dev/null 2>&1
fi

echo "Starting frontend..."
npm run dev >/dev/null 2>&1 &

sleep 5

echo ""
echo "========================================"
echo "   OPENING APPLICATION..."
echo "========================================"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:5000"
echo ""
echo "Close this window to stop"
echo ""

open http://localhost:3000

# Keep running
wait

