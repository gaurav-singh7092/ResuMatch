#!/bin/bash

# ResuMatch Development Helper Script
# This script helps with common development tasks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv .venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source .venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Download spaCy model
    print_status "Downloading spaCy model..."
    python -m spacy download en_core_web_sm
    
    print_status "Backend setup complete!"
    cd ..
}

# Function to setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    if ! command_exists node; then
        print_error "Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    print_status "Frontend setup complete!"
    cd ..
}

# Function to run backend
run_backend() {
    print_status "Starting backend server..."
    cd backend
    source .venv/bin/activate
    python main.py
}

# Function to run frontend
run_frontend() {
    print_status "Starting frontend development server..."
    cd frontend
    npm run dev
}

# Function to run both backend and frontend
run_dev() {
    print_status "Starting both backend and frontend..."
    
    # Start backend in background
    cd backend
    source .venv/bin/activate
    python main.py &
    BACKEND_PID=$!
    cd ..
    
    # Start frontend in background
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    print_status "Backend running on http://localhost:8000 (PID: $BACKEND_PID)"
    print_status "Frontend running on http://localhost:3000 (PID: $FRONTEND_PID)"
    print_warning "Press Ctrl+C to stop both servers"
    
    # Wait for interrupt
    trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
    wait
}

# Function to clean up
clean() {
    print_status "Cleaning up..."
    
    # Clean backend
    if [ -d "backend/__pycache__" ]; then
        rm -rf backend/__pycache__
    fi
    
    if [ -d "backend/.venv" ]; then
        rm -rf backend/.venv
    fi
    
    # Clean frontend
    if [ -d "frontend/node_modules" ]; then
        rm -rf frontend/node_modules
    fi
    
    if [ -d "frontend/.next" ]; then
        rm -rf frontend/.next
    fi
    
    print_status "Cleanup complete!"
}

# Function to show help
show_help() {
    echo "ResuMatch Development Helper"
    echo ""
    echo "Usage: ./dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  setup-backend    Setup Python backend environment"
    echo "  setup-frontend   Setup Node.js frontend environment"
    echo "  setup-all        Setup both backend and frontend"
    echo "  run-backend      Start backend server"
    echo "  run-frontend     Start frontend development server"
    echo "  run-dev          Start both backend and frontend"
    echo "  clean            Clean up generated files"
    echo "  help             Show this help message"
    echo ""
}

# Main script logic
case "${1:-help}" in
    "setup-backend")
        setup_backend
        ;;
    "setup-frontend")
        setup_frontend
        ;;
    "setup-all")
        setup_backend
        setup_frontend
        ;;
    "run-backend")
        run_backend
        ;;
    "run-frontend")
        run_frontend
        ;;
    "run-dev")
        run_dev
        ;;
    "clean")
        clean
        ;;
    "help"|*)
        show_help
        ;;
esac
