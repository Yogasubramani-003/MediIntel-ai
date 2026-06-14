@echo off
REM MediIntel AI - Quick Start Script for Windows

echo ===================================
echo MediIntel AI - Quick Start
echo ===================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Docker is not installed. Please install Docker Desktop first.
    echo Visit: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [OK] Docker found
echo.

REM Stop any existing containers
echo Stopping any existing containers...
docker compose down 2>nul

REM Build and start services
echo.
echo Building and starting MediIntel AI...
echo This may take a few minutes on first run...
echo.

docker compose up --build -d

REM Wait for services to be ready
echo.
echo Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are running
docker compose ps | findstr "Up" >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo ===================================
    echo [OK] MediIntel AI is running!
    echo ===================================
    echo.
    echo Open your browser and go to:
    echo    http://localhost:8000
    echo.
    echo View logs:
    echo    docker compose logs -f
    echo.
    echo Stop the application:
    echo    docker compose down
    echo.
) else (
    echo.
    echo [X] Services failed to start. Check logs:
    echo    docker compose logs
)

pause
