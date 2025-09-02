#!/bin/bash

# EduConnect Startup Script

echo "🚀 Starting EduConnect Platform..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration (especially OPENAI_API_KEY for AI features)"
fi

# Build and start all services
echo "🏗️  Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ EduConnect is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000/api"
echo "👨‍💼 Admin Panel: http://localhost:8000/admin"
echo "🔑 Admin Login: admin@educonnect.com / admin123"
echo ""
echo "📖 API Documentation: http://localhost:8000/api/ (when DRF browsable API is enabled)"
echo ""
echo "To stop the platform: docker-compose down"
echo "To view logs: docker-compose logs -f [service_name]"
echo ""
echo "🎉 Happy learning with EduConnect!"