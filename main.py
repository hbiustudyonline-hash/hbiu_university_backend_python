from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
from datetime import datetime, timedelta, timezone
import jwt
import bcrypt
import hashlib
from dotenv import load_dotenv
from openai import OpenAI
import json
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Initialize OpenAI client
try:
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None
except Exception as e:
    print(f"Warning: OpenAI client initialization failed: {e}")
    openai_client = None

# FastAPI app instance
app = FastAPI(title="HBIU University Backend", version="1.0.0")

# Security
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CORS Configuration
origins = [
    "http://localhost:5173",  # Vite dev server (Base44 Frontend)
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://hbiuuniversityfrontend-production.up.railway.app",
    "https://*.railway.app",
    "https://*.up.railway.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "student"

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class Course(BaseModel):
    id: int
    title: str
    description: str
    instructor: str
    created_at: datetime

class Discussion(BaseModel):
    id: int
    courseId: int
    moduleId: Optional[int] = None
    authorId: int
    title: str
    content: str
    isPinned: bool = False
    isResolved: bool = False
    replies: List[Dict[str, Any]] = []
    tags: List[str] = []
    created_at: datetime

class Attendance(BaseModel):
    id: int
    courseId: int
    studentId: int
    moduleId: Optional[int] = None
    date: str
    status: str  # 'present', 'absent', 'late', 'excused'
    notes: Optional[str] = None
    recordedBy: Optional[int] = None
    created_at: datetime

class Page(BaseModel):
    id: int
    courseId: int
    moduleId: Optional[int] = None
    title: str
    content: str
    slug: Optional[str] = None
    isPublished: bool = False
    order: int = 0
    createdBy: int
    created_at: datetime

class FinalExam(BaseModel):
    id: int
    courseId: int
    title: str
    description: Optional[str] = None
    questions: List[Dict[str, Any]] = []
    totalPoints: int = 100
    duration: int  # minutes
    startDate: datetime
    endDate: datetime
    isPublished: bool = False
    passingScore: int = 60
    createdBy: int
    created_at: datetime

class FinalExamSubmission(BaseModel):
    id: int
    examId: int
    studentId: int
    answers: Dict[str, Any] = {}
    score: Optional[float] = None
    feedback: Optional[str] = None
    status: str = "in_progress"  # 'in_progress', 'submitted', 'graded'
    startedAt: datetime
    submittedAt: Optional[datetime] = None
    gradedAt: Optional[datetime] = None
    gradedBy: Optional[int] = None
    created_at: datetime

class Transcript(BaseModel):
    id: int
    studentId: int
    courseId: int
    grade: Optional[str] = None
    gradePoints: Optional[float] = None
    credits: int = 3
    semester: Optional[str] = None
    year: Optional[int] = None
    status: str = "in_progress"  # 'in_progress', 'completed', 'withdrawn', 'failed'
    completedAt: Optional[datetime] = None
    created_at: datetime

class CollegeStaff(BaseModel):
    id: int
    collegeId: int
    userId: int
    position: str
    department: Optional[str] = None
    officeLocation: Optional[str] = None
    phone: Optional[str] = None
    officeHours: Optional[Dict[str, Any]] = None
    bio: Optional[str] = None
    permissions: List[str] = []
    isActive: bool = True
    hireDate: Optional[datetime] = None
    created_at: datetime

class Degree(BaseModel):
    id: int
    collegeId: int
    name: str
    type: str  # 'certificate', 'associate', 'bachelor', 'master', 'doctorate'
    description: Optional[str] = None
    requiredCredits: int = 120
    requiredCourses: List[int] = []
    electiveCourses: List[int] = []
    duration: Optional[int] = None  # years
    isActive: bool = True
    requirements: Dict[str, Any] = {}
    created_at: datetime

class AIInstructor(BaseModel):
    id: int
    courseId: int
    name: str
    avatar_url: Optional[str] = None
    personality: Optional[str] = None
    expertise: List[str] = []
    systemPrompt: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.7
    isActive: bool = True
    settings: Dict[str, Any] = {}
    createdBy: int
    created_at: datetime

class AIContentRequest(BaseModel):
    prompt: str
    content_type: str  # "lesson", "quiz", "assignment", "explanation"
    subject: Optional[str] = None
    difficulty: Optional[str] = "intermediate"  # "beginner", "intermediate", "advanced"
    length: Optional[str] = "medium"  # "short", "medium", "long"

class QuizGenerationRequest(BaseModel):
    topic: str
    num_questions: int = 5
    difficulty: str = "intermediate"
    question_types: List[str] = ["multiple_choice", "true_false"]

class StudyAssistantRequest(BaseModel):
    question: str
    context: Optional[str] = None
    course_id: Optional[int] = None

class AIResponse(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}
    success: bool = True
    error_message: Optional[str] = None

# Utility Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Ensure password is not too long for bcrypt
    if len(plain_password) > 72:
        plain_password = plain_password[:72]
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    # Ensure password is not too long for bcrypt
    if len(password) > 72:
        password = password[:72]
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# AI Utility Functions
def generate_educational_content(prompt: str, content_type: str, subject: str = None, difficulty: str = "intermediate", length: str = "medium") -> Dict[str, Any]:
    """Generate educational content using OpenAI GPT"""
    if not openai_client:
        return {
            "content": "AI service is currently unavailable. Please contact your administrator to configure the OpenAI API key.",
            "metadata": {},
            "success": False,
            "error_message": "OpenAI client not initialized"
        }
    
    try:
        # Customize system prompt based on content type
        system_prompts = {
            "lesson": f"You are an expert educator creating {difficulty} level lesson content for {subject or 'general studies'}. Create engaging, well-structured educational material.",
            "quiz": f"You are an expert educator creating {difficulty} level quiz questions for {subject or 'general studies'}. Create clear, fair, and educational quiz content.",
            "assignment": f"You are an expert educator creating {difficulty} level assignments for {subject or 'general studies'}. Create meaningful, practical assignments that reinforce learning.",
            "explanation": f"You are an expert tutor providing {difficulty} level explanations for {subject or 'general studies'}. Provide clear, comprehensive explanations."
        }
        
        length_instructions = {
            "short": "Keep the response concise and focused (200-400 words).",
            "medium": "Provide a moderate length response (400-800 words).",
            "long": "Create a comprehensive, detailed response (800-1200 words)."
        }
        
        system_prompt = system_prompts.get(content_type, system_prompts["explanation"])
        system_prompt += f" {length_instructions.get(length, length_instructions['medium'])}"
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        return {
            "content": response.choices[0].message.content,
            "metadata": {
                "content_type": content_type,
                "subject": subject,
                "difficulty": difficulty,
                "length": length,
                "tokens_used": response.usage.total_tokens
            },
            "success": True
        }
    except Exception as e:
        return {
            "content": "",
            "metadata": {},
            "success": False,
            "error_message": str(e)
        }

def generate_quiz(topic: str, num_questions: int = 5, difficulty: str = "intermediate", question_types: List[str] = None) -> Dict[str, Any]:
    """Generate quiz questions using OpenAI GPT"""
    if question_types is None:
        question_types = ["multiple_choice", "true_false"]
    
    if not openai_client:
        return {
            "content": {},
            "metadata": {},
            "success": False,
            "error_message": "OpenAI client not initialized"
        }
    
    try:
        prompt = f"""
Create a {difficulty} level quiz about {topic} with {num_questions} questions.
Include question types: {', '.join(question_types)}

Format as JSON with this structure:
{{
    "quiz_title": "{topic} Quiz",
    "questions": [
        {{
            "id": 1,
            "type": "multiple_choice",
            "question": "Question text here?",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct_answer": "A",
            "explanation": "Brief explanation of the correct answer"
        }}
    ]
}}

Ensure all questions are educational, clear, and appropriate for {difficulty} level.
"""
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert educator creating educational quizzes. Always respond with valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.6
        )
        
        quiz_content = response.choices[0].message.content
        # Try to parse JSON, fallback to text if parsing fails
        try:
            quiz_data = json.loads(quiz_content)
        except json.JSONDecodeError:
            quiz_data = {"quiz_title": f"{topic} Quiz", "raw_content": quiz_content}
        
        return {
            "content": quiz_data,
            "metadata": {
                "topic": topic,
                "num_questions": num_questions,
                "difficulty": difficulty,
                "question_types": question_types,
                "tokens_used": response.usage.total_tokens
            },
            "success": True
        }
    except Exception as e:
        return {
            "content": {},
            "metadata": {},
            "success": False,
            "error_message": str(e)
        }

def study_assistant(question: str, context: str = None, course_info: str = None) -> Dict[str, Any]:
    """AI study assistant to help students with questions"""
    if not openai_client:
        return {
            "content": "AI study assistant is currently unavailable. Please contact your instructor or administrator for assistance.",
            "metadata": {},
            "success": False,
            "error_message": "OpenAI client not initialized"
        }
    
    try:
        system_prompt = "You are a helpful AI tutor assistant. Provide clear, educational answers to student questions. Be encouraging and supportive while maintaining academic accuracy."
        
        user_prompt = f"Student Question: {question}"
        if context:
            user_prompt += f"\n\nContext: {context}"
        if course_info:
            user_prompt += f"\n\nCourse Information: {course_info}"
            
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return {
            "content": response.choices[0].message.content,
            "metadata": {
                "question": question,
                "has_context": bool(context),
                "has_course_info": bool(course_info),
                "tokens_used": response.usage.total_tokens
            },
            "success": True
        }
    except Exception as e:
        return {
            "content": "I apologize, but I'm unable to process your question at the moment. Please try again later or contact your instructor for assistance.",
            "metadata": {},
            "success": False,
            "error_message": str(e)
        }

# In-memory storage (replace with actual database in production)
users_db = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@hbiu.edu",
        "password": get_password_hash("admin123"),
        "role": "admin",
        "created_at": datetime.now(timezone.utc)
    },
    {
        "id": 2,
        "username": "lecturer1",
        "email": "lecturer1@hbiu.edu",
        "password": get_password_hash("lecturer123"),
        "role": "lecturer",
        "created_at": datetime.now(timezone.utc)
    },
    {
        "id": 3,
        "username": "student1",
        "email": "student1@hbiu.edu",
        "password": get_password_hash("student123"),
        "role": "student",
        "created_at": datetime.now(timezone.utc)
    }
]

courses_db = [
    {
        "id": 1,
        "title": "Introduction to Computer Science",
        "description": "Basic programming concepts and algorithms",
        "instructor": "Dr. Smith",
        "created_at": datetime.now(timezone.utc)
    },
    {
        "id": 2,
        "title": "Web Development",
        "description": "Full-stack web development with modern frameworks",
        "instructor": "Prof. Johnson",
        "created_at": datetime.now(timezone.utc)
    },
    {
        "id": 3,
        "title": "Database Systems",
        "description": "Database design and SQL fundamentals",
        "instructor": "Dr. Williams",
        "created_at": datetime.now(timezone.utc)
    }
]

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_username(username: str):
    for user in users_db:
        if user["username"] == username:
            return user
    return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise credentials_exception
    
    user = get_user_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.get("/")
async def root():
    return {"message": "HBIU University Backend API", "status": "running"}

@app.post("/api/auth/login", response_model=Token)
async def login(user_login: UserLogin):
    user = get_user_by_username(user_login.username)
    if not user or not verify_password(user_login.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    user_response = User(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        role=user["role"],
        created_at=user["created_at"]
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }

@app.post("/api/auth/register", response_model=User)
async def register(user_create: UserCreate):
    # Check if user already exists
    if get_user_by_username(user_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    new_user = {
        "id": len(users_db) + 1,
        "username": user_create.username,
        "email": user_create.email,
        "password": get_password_hash(user_create.password),
        "role": user_create.role,
        "created_at": datetime.now(timezone.utc)
    }
    users_db.append(new_user)
    
    return User(
        id=new_user["id"],
        username=new_user["username"],
        email=new_user["email"],
        role=new_user["role"],
        created_at=new_user["created_at"]
    )

@app.get("/api/auth/me", response_model=User)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return User(
        id=current_user["id"],
        username=current_user["username"],
        email=current_user["email"],
        role=current_user["role"],
        created_at=current_user["created_at"]
    )

@app.get("/api/courses", response_model=List[Course])
async def get_courses(current_user: dict = Depends(get_current_user)):
    return [Course(**course) for course in courses_db]

@app.get("/api/courses/{course_id}", response_model=Course)
async def get_course(course_id: int, current_user: dict = Depends(get_current_user)):
    course = next((course for course in courses_db if course["id"] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return Course(**course)

@app.get("/api/users", response_model=List[User])
async def get_users(current_user: dict = Depends(get_current_user)):
    # Only admin can see all users
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return [
        User(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            role=user["role"],
            created_at=user["created_at"]
        ) for user in users_db
    ]

@app.get("/api/dashboard/stats")
async def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    if current_user["role"] == "admin":
        return {
            "total_users": len(users_db),
            "total_courses": len(courses_db),
            "total_students": len([u for u in users_db if u["role"] == "student"]),
            "total_lecturers": len([u for u in users_db if u["role"] == "lecturer"])
        }
    elif current_user["role"] == "lecturer":
        return {
            "my_courses": len(courses_db),  # In real app, filter by lecturer
            "total_students": len([u for u in users_db if u["role"] == "student"]),
            "assignments": 0,  # Placeholder
            "submissions": 0   # Placeholder
        }
    else:  # student
        return {
            "enrolled_courses": len(courses_db),  # In real app, filter by enrollment
            "assignments": 0,  # Placeholder
            "grades": 0,       # Placeholder
            "attendance": 85   # Placeholder
        }

# AI-Powered Educational Endpoints
@app.post("/api/ai/generate-content", response_model=AIResponse)
async def generate_content(request: AIContentRequest, current_user: dict = Depends(get_current_user)):
    """Generate educational content using AI"""
    if not openai_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured. Please contact administrator."
        )
    
    result = generate_educational_content(
        prompt=request.prompt,
        content_type=request.content_type,
        subject=request.subject,
        difficulty=request.difficulty,
        length=request.length
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI content generation failed: {result.get('error_message', 'Unknown error')}"
        )
    
    return AIResponse(**result)

@app.post("/api/ai/generate-quiz", response_model=AIResponse)
async def generate_quiz_endpoint(request: QuizGenerationRequest, current_user: dict = Depends(get_current_user)):
    """Generate quiz questions using AI"""
    if not openai_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured. Please contact administrator."
        )
    
    # Only lecturers and admins can generate quizzes
    if current_user["role"] not in ["lecturer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only lecturers and administrators can generate quizzes"
        )
    
    result = generate_quiz(
        topic=request.topic,
        num_questions=request.num_questions,
        difficulty=request.difficulty,
        question_types=request.question_types
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Quiz generation failed: {result.get('error_message', 'Unknown error')}"
        )
    
    return AIResponse(**result)

@app.post("/api/ai/study-assistant", response_model=AIResponse)
async def study_assistant_endpoint(request: StudyAssistantRequest, current_user: dict = Depends(get_current_user)):
    """AI-powered study assistant for students"""
    if not openai_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured. Please contact administrator."
        )
    
    # Get course info if course_id is provided
    course_info = None
    if request.course_id:
        course = next((course for course in courses_db if course["id"] == request.course_id), None)
        if course:
            course_info = f"Course: {course['title']} - {course['description']}"
    
    result = study_assistant(
        question=request.question,
        context=request.context,
        course_info=course_info
    )
    
    return AIResponse(**result)

@app.get("/api/ai/capabilities")
async def get_ai_capabilities(current_user: dict = Depends(get_current_user)):
    """Get available AI capabilities based on user role"""
    base_capabilities = {
        "study_assistant": {
            "available": True,
            "description": "Get help with questions and explanations"
        }
    }
    
    if current_user["role"] in ["lecturer", "admin"]:
        base_capabilities.update({
            "content_generation": {
                "available": True,
                "description": "Generate lessons, assignments, and explanations",
                "types": ["lesson", "assignment", "explanation"]
            },
            "quiz_generation": {
                "available": True,
                "description": "Generate quiz questions and assessments",
                "question_types": ["multiple_choice", "true_false", "short_answer"]
            }
        })
    
    if current_user["role"] == "admin":
        base_capabilities.update({
            "advanced_analytics": {
                "available": True,
                "description": "Generate reports and analytics using AI"
            }
        })
    
    return {
        "user_role": current_user["role"],
        "ai_service_available": bool(openai_client),
        "capabilities": base_capabilities
    }

@app.post("/api/ai/explain-concept")
async def explain_concept(request: dict, current_user: dict = Depends(get_current_user)):
    """Explain a specific concept or term"""
    if not openai_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not configured. Please contact administrator."
        )
    
    concept = request.get("concept", "")
    subject = request.get("subject", "")
    level = request.get("level", "intermediate")
    
    if not concept:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Concept is required"
        )
    
    result = generate_educational_content(
        prompt=f"Explain the concept: {concept}",
        content_type="explanation",
        subject=subject,
        difficulty=level,
        length="medium"
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Concept explanation failed: {result.get('error_message', 'Unknown error')}"
        )
    
    return AIResponse(**result)


# ===== Base44 SDK Compatible Entity Routes =====

# Mock data for entities (in-memory storage)
mock_users = []
mock_courses = []

# Generic entity storage (in-memory for now - replace with database)
entity_store = {
    "User": mock_users,
    "Course": mock_courses,
    "Enrollment": [],
    "Assignment": [],
    "College": [],
    "Module": [],
    "Announcement": [],
    "Quiz": [],
    "Submission": [],
    "SystemSetting": [],
    "StaffApplication": [],
    "UniversityAnnouncement": [],
    "Notification": [],
    "InternalMessage": [],
    "Document": [],
    "DocumentVersion": [],
    "CollegeTransferHistory": [],
    "AuditLog": [],
    "EmployeeRecord": [],
    "LeaveRequest": [],
    "PerformanceReview": [],
    "PayrollRecord": [],
    "CommunityGroup": [],
    "CommunityMember": [],
    "CommunityPost": [],
    "SystemAccess": [],
}

def get_entity_store(entity_name: str):
    """Get or create entity store"""
    if entity_name not in entity_store:
        entity_store[entity_name] = []
    return entity_store[entity_name]

@app.get("/api/entities/{entity}")
async def list_entities(entity: str, sort: str = "-created_at", limit: int = 100):
    """Base44 SDK compatible - List all entities"""
    try:
        store = get_entity_store(entity)
        
        # Parse sort (Base44 uses '-field' for DESC)
        reverse = sort.startswith('-')
        sort_field = sort[1:] if reverse else sort
        
        # Sort if possible
        try:
            if sort_field in ['created_at', 'createdAt', 'id']:
                sorted_data = sorted(store, key=lambda x: x.get(sort_field, x.get('id', 0)), reverse=reverse)
            else:
                sorted_data = store
        except:
            sorted_data = store
        
        # Apply limit
        result = sorted_data[:limit]
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to list {entity}",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@app.get("/api/entities/{entity}/{entity_id}")
async def get_entity(entity: str, entity_id: int):
    """Base44 SDK compatible - Get single entity"""
    try:
        store = get_entity_store(entity)
        
        # Find entity by ID
        found = next((item for item in store if item.get('id') == entity_id), None)
        
        if not found:
            raise HTTPException(
                status_code=404,
                detail=f"{entity} with id {entity_id} not found"
            )
        
        return {
            "success": True,
            "data": found,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to get {entity}",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@app.post("/api/entities/{entity}/filter")
async def filter_entities(entity: str, filters: dict, sort: str = "-created_at", limit: int = 100):
    """Base44 SDK compatible - Filter entities"""
    try:
        store = get_entity_store(entity)
        
        # Apply filters
        filtered = []
        for item in store:
            match = True
            for key, value in filters.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                filtered.append(item)
        
        # Parse sort
        reverse = sort.startswith('-')
        sort_field = sort[1:] if reverse else sort
        
        # Sort if possible
        try:
            if sort_field in ['created_at', 'createdAt', 'id']:
                sorted_data = sorted(filtered, key=lambda x: x.get(sort_field, x.get('id', 0)), reverse=reverse)
            else:
                sorted_data = filtered
        except:
            sorted_data = filtered
        
        # Apply limit
        result = sorted_data[:limit]
        
        return {
            "success": True,
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to filter {entity}",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@app.post("/api/entities/{entity}")
async def create_entity(entity: str, data: dict):
    """Base44 SDK compatible - Create new entity"""
    try:
        store = get_entity_store(entity)
        
        # Generate ID if not present
        if 'id' not in data:
            max_id = max([item.get('id', 0) for item in store], default=0)
            data['id'] = max_id + 1
        
        # Add timestamps if not present
        if 'created_at' not in data and 'createdAt' not in data:
            data['created_at'] = datetime.now(timezone.utc).isoformat()
        
        # Add to store
        store.append(data)
        
        return {
            "success": True,
            "data": data,
            "message": f"{entity} created successfully",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to create {entity}",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@app.put("/api/entities/{entity}/{entity_id}")
async def update_entity(entity: str, entity_id: int, data: dict):
    """Base44 SDK compatible - Update entity"""
    try:
        store = get_entity_store(entity)
        
        # Find and update entity
        for i, item in enumerate(store):
            if item.get('id') == entity_id:
                # Merge data
                store[i] = {**item, **data}
                
                # Add updated timestamp
                if 'updated_at' not in store[i] and 'updatedAt' not in store[i]:
                    store[i]['updated_at'] = datetime.now(timezone.utc).isoformat()
                
                return {
                    "success": True,
                    "data": store[i],
                    "message": f"{entity} updated successfully",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
        
        raise HTTPException(
            status_code=404,
            detail=f"{entity} with id {entity_id} not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to update {entity}",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@app.delete("/api/entities/{entity}/{entity_id}")
async def delete_entity(entity: str, entity_id: int):
    """Base44 SDK compatible - Delete entity"""
    try:
        store = get_entity_store(entity)
        
        # Find and remove entity
        for i, item in enumerate(store):
            if item.get('id') == entity_id:
                deleted = store.pop(i)
                return {
                    "success": True,
                    "data": None,
                    "message": f"{entity} deleted successfully",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
        
        raise HTTPException(
            status_code=404,
            detail=f"{entity} with id {entity_id} not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to delete {entity}",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    # Only use reload in development
    reload = os.getenv("RAILWAY_ENVIRONMENT") != "production"
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=reload)