#!/bin/bash

# HBIU Python Backend - Local Development Script
# This script helps you run and test the backend locally

echo "🏫 HBIU Python Backend - Development Helper"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "backend_env" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv backend_env
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source backend_env/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating template..."
    cat > .env << EOL
# JWT Secret Key (generate a secure random string)
SECRET_KEY=your-super-secret-jwt-key-here-please-change-this

# OpenAI API Key (required for AI features)
# Get your key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here

# Database Configuration (Railway PostgreSQL)
DATABASE_URL=postgresql://postgres:uYQBmbMxABSBFFEXuKmagaqmxFhbGKzF@tramway.proxy.rlwy.net:16123/railway

# Environment
ENVIRONMENT=development
EOL
    echo "📝 Created .env template. Please update with your actual values!"
    echo "   - Add your OpenAI API key for AI features"
    echo "   - Change the SECRET_KEY to something secure"
fi

# Function to run the server
run_server() {
    echo "🚀 Starting HBIU Python Backend..."
    echo "   API Documentation: http://localhost:8000/docs"
    echo "   Health Check: http://localhost:8000/"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
}

# Function to run tests
run_tests() {
    echo "🧪 Running deployment tests..."
    python3 test_deployment.py
}

# Main menu
echo ""
echo "What would you like to do?"
echo "1) Start the backend server"
echo "2) Run deployment tests"
echo "3) Install dependencies only"
echo "4) Show API documentation URL"
echo "5) Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        run_server
        ;;
    2)
        run_tests
        ;;
    3)
        echo "✅ Dependencies installed!"
        ;;
    4)
        echo "📚 API Documentation URLs:"
        echo "   Local: http://localhost:8000/docs"
        echo "   Railway: https://hbiuuniversitybackendpython-production.up.railway.app/docs"
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac