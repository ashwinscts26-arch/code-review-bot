#!/bin/bash

# Code Review Bot - Single Click Start Script (macOS/Linux)

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "================================"
echo "Code Review Bot - Starting..."
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if virtual environment exists, create if not
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo -e "${BLUE}Creating Python virtual environment...${NC}"
    cd "$BACKEND_DIR"
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
    cd "$PROJECT_DIR"
fi

# Check if node_modules exists, create if not
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo -e "${BLUE}Installing Node packages...${NC}"
    cd "$FRONTEND_DIR"
    npm install -q
    cd "$PROJECT_DIR"
fi

echo -e "${GREEN}✓ All dependencies ready${NC}"
echo ""
echo "Starting Code Review Bot..."
echo ""

# Start backend in background
cd "$BACKEND_DIR"
source venv/bin/activate
echo -e "${BLUE}Starting Backend (Port 5000)...${NC}"
python app.py > /tmp/crb-backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 2

# Start frontend in background
cd "$FRONTEND_DIR"
echo -e "${BLUE}Starting Frontend (Port 3000)...${NC}"
npm run dev > /tmp/crb-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait for frontend to start
sleep 3

# Open browser
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✓ Application started!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Opening browser to http://localhost:3000..."
echo ""

# Try to open browser (works on macOS, Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://localhost:3000
else
    echo "Please open http://localhost:3000 in your browser"
fi

echo ""
echo "Application is running!"
echo ""
echo "Backend logs: tail -f /tmp/crb-backend.log"
echo "Frontend logs: tail -f /tmp/crb-frontend.log"
echo ""
echo "To stop the application, press Ctrl+C"
echo ""

# Keep script running
wait

