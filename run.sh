#!/bin/bash

echo "================================"
echo "  LearnVaultX - Starting Server"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from python.org"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo ""
echo "Starting LearnVaultX application..."
echo ""
echo "Access the app at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py

