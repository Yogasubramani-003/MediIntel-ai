#!/bin/bash
# MediIntel AI - Local Development Setup (No Docker Required)

echo "==================================="
echo "MediIntel AI - Local Setup"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python found"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "Installing dependencies (this may take a few minutes)..."
python -m pip install --upgrade pip
pip install -r requirements-local.txt

echo ""
echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm

echo ""
echo "Creating uploads directory..."
mkdir -p uploads

echo ""
echo "==================================="
echo "Starting MediIntel AI Server..."
echo "==================================="
echo ""
echo "Server will start at: http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
