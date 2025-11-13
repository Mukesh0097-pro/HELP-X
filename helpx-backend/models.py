from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum


class BookingStatus(enum.Enum):
    """Enum for booking status"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)  # User bio/description
    
    # Relationship with skills
    skills = relationship("Skill", back_populates="owner", cascade="all, delete-orphan")
    
    # Relationship with bookings (as customer)
    bookings_as_customer = relationship("Booking", foreign_keys="Booking.customer_id", back_populates="customer", cascade="all, delete-orphan")
    
    # Relationship with bookings (as provider)
    bookings_as_provider = relationship("Booking", foreign_keys="Booking.provider_id", back_populates="provider", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "bio": self.bio
        }


class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    skill = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationship with user
    owner = relationship("User", back_populates="skills")
    
    # Relationship with bookings
    bookings = relationship("Booking", back_populates="skill", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "skill": self.skill,
            "description": self.description,
            "user_id": self.user_id,
            "user_name": self.owner.name if self.owner else None
        }


class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    booking_date = Column(DateTime, nullable=True)
    duration_hours = Column(Integer, default=1, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    customer = relationship("User", foreign_keys=[customer_id], back_populates="bookings_as_customer")
    provider = relationship("User", foreign_keys=[provider_id], back_populates="bookings_as_provider")
    skill = relationship("Skill", back_populates="bookings")
    
    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "customer_name": self.customer.name if self.customer else None,
            "provider_id": self.provider_id,
            "provider_name": self.provider.name if self.provider else None,
            "skill_id": self.skill_id,
            "skill_name": self.skill.skill if self.skill else None,
            "status": self.status,
            "booking_date": self.booking_date.isoformat() if self.booking_date else None,
            "duration_hours": self.duration_hours,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
