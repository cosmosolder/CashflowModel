#!/bin/bash

# Financial Planning Model - Full Stack Startup Script
# This script starts both the Flask backend and React frontend

echo "🏦 Financial Planning Model - Full Stack UI"
echo "============================================="

# Check if required dependencies are available
command -v python3 >/dev/null 2>&1 || { echo "❌ python3 is required but not installed." >&2; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed." >&2; exit 1; }

echo "✅ Dependencies check passed"

# Install Python backend dependencies
echo "📦 Installing Python backend dependencies..."
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi
cd ..

# Install React frontend dependencies
echo "📦 Installing React frontend dependencies..."
cd financial-planning-ui
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install React dependencies"
    exit 1
fi
cd ..

echo "✅ All dependencies installed successfully"

# Function to start backend
start_backend() {
    echo "🚀 Starting Flask backend server on port 5000..."
    cd backend
    python3 app.py &
    BACKEND_PID=$!
    cd ..
    echo "Backend PID: $BACKEND_PID"
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting React frontend server on port 3000..."
    cd financial-planning-ui
    npm start &
    FRONTEND_PID=$!
    cd ..
    echo "Frontend PID: $FRONTEND_PID"
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "Backend server stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "Frontend server stopped"
    fi
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start both servers
start_backend
sleep 3  # Give backend time to start
start_frontend

echo ""
echo "🌐 Servers starting up..."
echo "📊 Backend API: http://localhost:5001"
echo "🎨 Frontend UI: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "=================================="

# Wait for user interrupt
wait