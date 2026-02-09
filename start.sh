#!/bin/bash
# Startup script with better error handling for Railway

echo "🚀 Starting HBIU Python Backend..."
echo "📍 Working directory: $(pwd)"
echo "🔍 Files present: $(ls -la)"

# Check environment variables
echo "🔧 Environment Check:"
echo "   PORT: ${PORT:-Not set (will use 8000)}"
echo "   SECRET_KEY: ${SECRET_KEY:+Set ✓}" 
echo "   OPENAI_API_KEY: ${OPENAI_API_KEY:+Set ✓}"

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ ERROR: main.py not found!"
    exit 1
fi

# Check Python version
echo "🐍 Python version: $(python --version)"

# Install any missing dependencies (safety check)
echo "📦 Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# Start the application
echo "🚀 Starting FastAPI application..."
echo "   Host: 0.0.0.0"
echo "   Port: ${PORT:-8000}"

exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info