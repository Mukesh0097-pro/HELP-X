from fastapi import FastAPI, Depends, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta
import uvicorn
from pydantic import BaseModel, EmailStr

from database import engine, get_db, Base
from models import User, Skill
import crud
from auth import (
    authenticate_user, 
    create_access_token, 
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="HelpX API",
    description="A skill-sharing platform backend where users can register and share their skills",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Pydantic models for request/response
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    message: str
    success: bool
    access_token: str
    token_type: str
    user: dict

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to HelpX API - A Skill Sharing Platform",
        "docs": "/docs",
        "endpoints": {
            "register": "/register",
            "login": "/login",
            "users": "/users",
            "skills": "/skills",
            "add_skill": "/add-skill",
            "me": "/me"
        }
    }

# Authentication endpoints
@app.post("/register", response_model=Token)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user with password"""
    try:
        print(f"🔍 Registration attempt: {user_data.email}")
        
        # Check if email already exists
        existing_user = crud.get_user_by_email(db, email=user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Validate password
        if len(user_data.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        
        # Create new user with hashed password
        print(f"🔍 Creating user: {user_data.name}")
        new_user = crud.create_user(db, name=user_data.name, email=user_data.email, password=user_data.password)
        print(f"✅ User created with ID: {new_user.id}")
        
        # Create access token
        access_token = create_access_token(
            data={"sub": new_user.id},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        print(f"✅ Token created successfully")
        
        return {
            "message": "User created successfully",
            "success": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user": new_user.to_dict()
        }
        
    except Exception as e:
        print(f"❌ Registration failed: {str(e)}")
        print(f"❌ Error type: {type(e).__name__}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    # Authenticate user
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "message": "Login successful",
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }

@app.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return {
        "success": True,
        "user": current_user.to_dict()
    }

# User endpoints
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    users = crud.get_all_users(db)
    return {
        "success": True,
        "count": len(users),
        "users": [user.to_dict() for user in users]
    }

@app.post("/add-user")
def add_user(
    name: str = Query(..., description="User's name"),
    email: str = Query(..., description="User's email"),
    password: str = Query(..., description="User's password"),
    db: Session = Depends(get_db)
):
    """Add a new user (legacy endpoint - use /register instead)"""
    # Check if email already exists
    existing_user = crud.get_user_by_email(db, email=email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user with hashed password
    new_user = crud.create_user(db, name=name, email=email, password=password)
    return {
        "success": True,
        "message": "User created successfully",
        "user": new_user.to_dict()
    }

# Skill endpoints
@app.get("/skills")
def get_skills(
    user_id: int = Query(None, description="Filter skills by user ID (optional)"),
    db: Session = Depends(get_db)
):
    """Get all skills or filter by user_id"""
    if user_id:
        # Check if user exists
        user = crud.get_user_by_id(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        skills = crud.get_skills_by_user(db, user_id=user_id)
    else:
        skills = crud.get_all_skills(db)
    
    return {
        "success": True,
        "count": len(skills),
        "skills": [skill.to_dict() for skill in skills]
    }

@app.post("/add-skill")
def add_skill(
    skill: str = Query(..., description="Skill name"),
    description: str = Query(..., description="Skill description"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a new skill (protected endpoint - requires authentication)"""
    # Create new skill for the authenticated user
    new_skill = crud.create_skill(db, skill=skill, description=description, user_id=current_user.id)
    return {
        "success": True,
        "message": "Skill added successfully",
        "skill": new_skill.to_dict()
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
