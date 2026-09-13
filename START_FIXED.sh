#!/bin/bash

# Code Review Bot - One-Click Starter (Linux/macOS) - FIXED VERSION

set -e

echo "================================"
echo "🚀 Code Review Bot - Starting..."
echo "================================"
echo ""

# Get the directory this script is in
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Script directory: $SCRIPT_DIR"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    wait $BACKEND_PID 2>/dev/null || true
    wait $FRONTEND_PID 2>/dev/null || true
    echo -e "${GREEN}✓ Stopped${NC}"
}

trap cleanup EXIT

# Check Python
echo -e "${BLUE}Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found${NC}"

# Check Node
echo -e "${BLUE}Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found. Please install Node.js 16+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found${NC}"

# Setup Backend
echo ""
echo -e "${BLUE}Setting up backend...${NC}"
cd "$SCRIPT_DIR/backend"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

if ! python -c "import flask" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ ERROR: Could not install Python dependencies${NC}"
        echo "Check that requirements.txt exists in: $SCRIPT_DIR/backend"
        exit 1
    fi
fi
echo -e "${GREEN}✓ Backend ready${NC}"

# Setup Frontend
echo -e "${BLUE}Setting up frontend...${NC}"
cd "$SCRIPT_DIR/frontend"

if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ ERROR: Could not install npm packages${NC}"
        echo "Check that package.json exists in: $SCRIPT_DIR/frontend"
        exit 1
    fi
fi
echo -e "${GREEN}✓ Frontend ready${NC}"

# Start Backend
echo ""
echo -e "${BLUE}Starting backend on port 5000...${NC}"
cd "$SCRIPT_DIR/backend"
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
python app.py > /tmp/codebot_backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is ready${NC}"
        break
    fi
    sleep 1
done

# Start Frontend
echo -e "${BLUE}Starting frontend on port 3000...${NC}"
cd "$SCRIPT_DIR/frontend"
npm run dev > /tmp/codebot_frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"

# Wait for frontend to be ready
echo "Waiting for frontend to be ready..."
sleep 5

# Open browser
echo ""
echo -e "${BLUE}Opening browser...${NC}"
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000 2>/dev/null || true
elif command -v open &> /dev/null; then
    open http://localhost:3000 2>/dev/null || true
fi

# Show status
echo ""
echo "================================"
echo -e "${GREEN}✓ Application Started!${NC}"
echo "================================"
echo ""
echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
echo -e "${GREEN}Backend:${NC}  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Keep running
wait $BACKEND_PID 2>/dev/null || true

