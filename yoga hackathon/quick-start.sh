#!/bin/bash
# MediIntel AI - Quick Start Script

echo "==================================="
echo "MediIntel AI - Quick Start"
echo "==================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✅ Docker found"

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker Compose found"
echo ""

# Stop any existing containers
echo "Stopping any existing containers..."
docker compose down 2>/dev/null

# Build and start services
echo ""
echo "Building and starting MediIntel AI..."
echo "This may take a few minutes on first run..."
echo ""

docker compose up --build -d

# Wait for services to be ready
echo ""
echo "Waiting for services to start..."
sleep 10

# Check if services are running
if docker compose ps | grep -q "Up"; then
    echo ""
    echo "==================================="
    echo "✅ MediIntel AI is running!"
    echo "==================================="
    echo ""
    echo "🌐 Open your browser and go to:"
    echo "   http://localhost:8000"
    echo ""
    echo "📊 View logs:"
    echo "   docker compose logs -f"
    echo ""
    echo "🛑 Stop the application:"
    echo "   docker compose down"
    echo ""
else
    echo ""
    echo "❌ Services failed to start. Check logs:"
    echo "   docker compose logs"
fi
