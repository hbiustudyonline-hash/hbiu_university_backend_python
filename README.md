# HBIU University Backend (Python FastAPI with AI)

AI-powered educational backend built with FastAPI, featuring comprehensive learning management system capabilities and OpenAI integration.

## Features

### 🎓 Educational Features
- **AI Study Assistant** - Intelligent tutoring system
- **Content Generation** - AI-powered lesson and assignment creation
- **Quiz Generator** - Automated quiz and assessment creation
- **Concept Explanation** - Detailed topic explanations

### 🔐 Authentication & Authorization
- JWT-based authentication
- Role-based access control (Admin, Lecturer, Student)
- Secure password hashing with bcrypt

### 🤖 AI Integration
- OpenAI GPT integration for educational content
- Contextual learning assistance
- Automated content generation
- Intelligent quiz creation

## Quick Start

### Local Development

1. **Clone and setup**
   ```bash
   cd backend-py
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the server**
   ```bash
   python3 main.py
   ```

   Server will start on `http://localhost:8000`

### Railway Deployment

1. **Connect to Railway**
   - Push code to GitHub repository
   - Connect repository to Railway project
   - Railway will auto-detect Python and deploy

2. **Environment Variables** (Set in Railway dashboard)
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SECRET_KEY=your_jwt_secret_key
   DATABASE_URL=your_postgresql_url (if using database)
   ```

3. **Custom Start Command** (Optional)
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

## API Documentation

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user info

### AI Endpoints
- `GET /api/ai/capabilities` - Get available AI features
- `POST /api/ai/study-assistant` - AI tutoring assistance
- `POST /api/ai/generate-content` - Generate educational content
- `POST /api/ai/generate-quiz` - Generate quiz questions
- `POST /api/ai/explain-concept` - Explain concepts

### Core Endpoints
- `GET /` - Health check
- `GET /api/courses` - List courses
- `GET /api/users` - List users (admin only)

## User Roles & Permissions

### 👨‍🎓 Student
- Access study assistant
- View assigned courses
- Get concept explanations

### 👨‍🏫 Lecturer
- All student permissions
- Generate educational content
- Create quizzes and assignments
- View student progress

### 👨‍💼 Admin
- All lecturer permissions
- User management
- System analytics
- Advanced AI features

## Test Credentials

```
Admin:     username=admin,     password=admin123
Lecturer:  username=lecturer1, password=lecturer123
Student:   username=student1,  password=student123
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | JWT secret key | Yes |
| `OPENAI_API_KEY` | OpenAI API key for AI features | Optional* |
| `DATABASE_URL` | PostgreSQL connection string | Optional |
| `PORT` | Server port (default: 8000) | No |
| `RAILWAY_ENVIRONMENT` | Railway environment | No |

*AI features will be disabled without OpenAI API key

## Technology Stack

- **Framework**: FastAPI
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt
- **AI Integration**: OpenAI GPT API
- **Server**: Uvicorn ASGI server
- **Database**: SQLAlchemy + PostgreSQL
- **Deployment**: Railway

## Development

### Project Structure
```
backend-py/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env                # Environment variables
├── Procfile            # Railway deployment
├── railway.json        # Railway configuration
├── nixpacks.toml       # Build configuration
└── test_ai.py          # AI functionality tests
```

### Adding New AI Features

1. Create AI utility function in `main.py`
2. Add corresponding API endpoint
3. Update role permissions in `get_ai_capabilities`
4. Test with appropriate user roles

### Running Tests
```bash
# Test AI functionality
python3 test_ai.py

# Manual API testing
curl http://localhost:8000/api/ai/capabilities
```

## Production Deployment

### Railway Configuration
- Automatically detects Python project
- Uses `requirements.txt` for dependencies
- Respects `Procfile` for start command
- Supports environment variables via dashboard

### Health Checks
- Endpoint: `GET /`
- Returns: `{"message": "HBIU University Backend API", "status": "running"}`

## Support

For issues and questions:
1. Check API documentation at `http://localhost:8000/docs` (Swagger UI)
2. Review server logs for error details
3. Ensure all environment variables are properly set
4. Verify OpenAI API key if using AI features

---

Built for HBIU University Learning Management System