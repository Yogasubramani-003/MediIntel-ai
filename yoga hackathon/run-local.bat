@echo off
REM MediIntel AI - Local Development Setup (No Docker Required)

echo ===================================
echo MediIntel AI - Local Setup
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if virtual environment exists
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)

echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Installing dependencies (this may take a few minutes)...
python -m pip install --upgrade pip
pip install -r requirements-local.txt

echo.
echo Downloading spaCy model...
python -m spacy download en_core_web_sm

echo.
echo Creating uploads directory...
if not exist "uploads\" mkdir uploads

echo.
echo ===================================
echo Starting MediIntel AI Server...
echo ===================================
echo.
echo Server will start at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
