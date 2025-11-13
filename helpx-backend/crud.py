from sqlalchemy.orm import Session
from models import User, Skill, Booking
from typing import List, Optional
from datetime import datetime
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

def create_user(db: Session, name: str, email: str, password: str, bio: str = None) -> User:
    """Create a new user with hashed password"""
    hashed_password = get_password_hash(password)
    db_user = User(name=name, email=email, hashed_password=hashed_password, bio=bio)
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


# Booking CRUD operations
def create_booking(
    db: Session,
    customer_id: int,
    provider_id: int,
    skill_id: int,
    booking_date: Optional[datetime] = None,
    duration_hours: int = 1,
    notes: Optional[str] = None
) -> Booking:
    """Create a new booking"""
    db_booking = Booking(
        customer_id=customer_id,
        provider_id=provider_id,
        skill_id=skill_id,
        booking_date=booking_date,
        duration_hours=duration_hours,
        notes=notes,
        status="pending"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_booking_by_id(db: Session, booking_id: int) -> Optional[Booking]:
    """Get booking by ID"""
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_bookings_by_customer(db: Session, customer_id: int) -> List[Booking]:
    """Get all bookings made by a customer"""
    return db.query(Booking).filter(Booking.customer_id == customer_id).all()


def get_bookings_by_provider(db: Session, provider_id: int) -> List[Booking]:
    """Get all bookings received by a provider"""
    return db.query(Booking).filter(Booking.provider_id == provider_id).all()


def get_all_bookings(db: Session) -> List[Booking]:
    """Get all bookings"""
    return db.query(Booking).all()


def update_booking_status(db: Session, booking_id: int, status: str) -> Optional[Booking]:
    """Update booking status"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        booking.status = status
        booking.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(booking)
    return booking


def delete_booking(db: Session, booking_id: int) -> bool:
    """Delete a booking"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        db.delete(booking)
        db.commit()
        return True
    return False
