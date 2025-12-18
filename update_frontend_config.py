#!/usr/bin/env python3
"""
Frontend Configuration Updater
Updates the React frontend to use the production Python backend URL
"""

import json
import os

def update_frontend_config():
    """Update frontend configuration files with production backend URL"""
    
    production_url = "https://hbiuuniversitybackendpython-production.up.railway.app"
    local_url = "http://localhost:8000"
    
    print("🔧 Frontend Configuration Updater")
    print("=" * 50)
    
    frontend_dir = "/Users/gregorygrant/Desktop/hbiu lms/hbiu-online-studies/Frontend"
    
    # Check if frontend directory exists
    if not os.path.exists(frontend_dir):
        print("❌ Frontend directory not found!")
        return False
    
    # Look for API configuration files
    api_config_files = [
        "src/api/base44Client.js",
        "src/config/api.js", 
        "src/utils/api.js",
        "vite.config.js"
    ]
    
    print(f"📁 Frontend directory: {frontend_dir}")
    print(f"🌐 Production URL: {production_url}")
    print(f"🏠 Local URL: {local_url}")
    print()
    
    found_files = []
    
    for config_file in api_config_files:
        file_path = os.path.join(frontend_dir, config_file)
        if os.path.exists(file_path):
            found_files.append(file_path)
            print(f"✅ Found: {config_file}")
        else:
            print(f"❌ Not found: {config_file}")
    
    if not found_files:
        print("\n⚠️  No API configuration files found!")
        print("💡 You may need to manually update your frontend API URLs")
    else:
        print(f"\n📋 Configuration Update Instructions:")
        print(f"   Replace any instances of:")
        print(f"   • http://localhost:8000  →  {production_url}")
        print(f"   • http://localhost:8001  →  {production_url}")
        print(f"   • Backend API URLs       →  {production_url}")
    
    # Create environment file suggestion
    env_content = f"""# Production Environment Variables for Frontend
VITE_API_BASE_URL={production_url}
VITE_BACKEND_URL={production_url}
VITE_PYTHON_API_URL={production_url}
VITE_NODE_API_URL=https://your-node-backend-url.railway.app
"""
    
    env_file = os.path.join(frontend_dir, ".env.production")
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"\n✅ Created: {env_file}")
        print("💡 Add this to your frontend build process")
    except Exception as e:
        print(f"\n❌ Could not create {env_file}: {e}")
    
    print(f"\n🔗 Production API Endpoints:")
    print(f"   📚 Documentation: {production_url}/docs")
    print(f"   🔍 Health Check: {production_url}/")
    print(f"   🔐 Login: {production_url}/api/auth/login")
    print(f"   🤖 AI Features: {production_url}/api/ai/")
    
    return True

if __name__ == "__main__":
    try:
        update_frontend_config()
    except Exception as e:
        print(f"💥 Error: {e}")