from sqlalchemy.orm import Session
from models import User, Skill
from typing import List, Optional
from auth import get_password_hash

# User CRUD operations
def get_all_users(db: Session) -> List[User]:
    """Get all users from database"""
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, name: str, email: str, password: str) -> User:
    """Create a new user with hashed password"""
    hashed_password = get_password_hash(password)
    db_user = User(name=name, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Skill CRUD operations
def get_all_skills(db: Session) -> List[Skill]:
    """Get all skills from database"""
    return db.query(Skill).all()

def get_skills_by_user(db: Session, user_id: int) -> List[Skill]:
    """Get all skills for a specific user"""
    return db.query(Skill).filter(Skill.user_id == user_id).all()

def create_skill(db: Session, skill: str, description: str, user_id: int) -> Skill:
    """Create a new skill"""
    db_skill = Skill(skill=skill, description=description, user_id=user_id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill
