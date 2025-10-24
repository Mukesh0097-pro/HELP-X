from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from database import engine, get_db, Base
from models import User, Skill
import crud

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

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to HelpX API - A Skill Sharing Platform",
        "docs": "/docs",
        "endpoints": {
            "users": "/users",
            "add_user": "/add-user",
            "skills": "/skills",
            "add_skill": "/add-skill"
        }
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
    db: Session = Depends(get_db)
):
    """Add a new user"""
    # Check if email already exists
    existing_user = crud.get_user_by_email(db, email=email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = crud.create_user(db, name=name, email=email)
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
    user_id: int = Query(..., description="User ID who owns this skill"),
    db: Session = Depends(get_db)
):
    """Add a new skill"""
    # Check if user exists
    user = crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    # Create new skill
    new_skill = crud.create_skill(db, skill=skill, description=description, user_id=user_id)
    return {
        "success": True,
        "message": "Skill added successfully",
        "skill": new_skill.to_dict()
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
