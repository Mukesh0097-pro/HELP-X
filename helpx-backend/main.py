from fastapi import FastAPI, Depends, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta
import uvicorn
from pydantic import BaseModel, EmailStr

from database import engine, get_db, Base
from models import User, Skill, Booking
import crud
from auth import (
    authenticate_user, 
    create_access_token, 
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from firebase_auth import verify_id_token as firebase_verify_id_token, extract_user_info as firebase_extract_user_info, init_firebase
import firebase_admin

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
    bio: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    message: str
    success: bool
    access_token: str
    token_type: str
    user: dict

class FirebaseTokenIn(BaseModel):
    id_token: str

class BookingCreate(BaseModel):
    provider_id: int
    skill_id: int
    booking_date: Optional[str] = None  # ISO format datetime string
    duration_hours: int = 1
    notes: Optional[str] = None

class BookingStatusUpdate(BaseModel):
    status: str  # "pending", "accepted", "completed", "cancelled"

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

@app.get("/firebase/project")
def firebase_project_info():
    """Return Firebase project identifier (debug endpoint)."""
    try:
        init_firebase()
        app_obj = firebase_admin.get_app()
        # project_id can be available via options or attribute depending on SDK internals
        project_id = getattr(app_obj, 'project_id', None) or app_obj.options.get('projectId')
        return {"success": True, "project_id": project_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firebase not initialized: {e}")

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
        new_user = crud.create_user(db, name=user_data.name, email=user_data.email, password=user_data.password, bio=user_data.bio)
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


@app.post("/auth/firebase/session", response_model=Token)
def create_session_from_firebase_token(payload: FirebaseTokenIn, db: Session = Depends(get_db)):
    """Exchange a Firebase ID token for a local JWT and user profile.

    Frontend should obtain Firebase ID token via Firebase JS SDK, then POST here with { id_token }.
    """
    try:
        claims = firebase_verify_id_token(payload.id_token)
        info = firebase_extract_user_info(claims)
        if not info.get("email"):
            raise HTTPException(status_code=400, detail="Firebase token missing email")

        # Find or create a local user
        user = crud.get_user_by_email(db, email=info["email"])
        if not user:
            name = info.get("name") or info["email"].split("@")[0]
            # Create with a generated password (won't be used; Firebase handles auth)
            user = crud.create_user(db, name=name, email=info["email"], password=f"firebase-{info['uid'] or 'uid'}")

        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {
            "message": "Session created from Firebase token",
            "success": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.to_dict(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Firebase token: {e}")

## OAuth routes removed per revert request

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
    print(f"✅ Authenticated user: {current_user.name} (ID: {current_user.id})")
    # Create new skill for the authenticated user
    new_skill = crud.create_skill(db, skill=skill, description=description, user_id=current_user.id)
    return {
        "success": True,
        "message": "Skill added successfully",
        "skill": new_skill.to_dict()
    }

# Booking endpoints
@app.post("/bookings")
def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new booking (protected endpoint - requires authentication)"""
    try:
        # Verify skill exists
        skill = db.query(Skill).filter(Skill.id == booking_data.skill_id).first()
        if not skill:
            raise HTTPException(status_code=404, detail="Skill not found")
        
        # Verify provider exists
        provider = db.query(User).filter(User.id == booking_data.provider_id).first()
        if not provider:
            raise HTTPException(status_code=404, detail="Provider not found")
        
        # Can't book your own service
        if booking_data.provider_id == current_user.id:
            raise HTTPException(status_code=400, detail="Cannot book your own service")
        
        # Parse booking date if provided
        from datetime import datetime
        booking_date = None
        if booking_data.booking_date:
            try:
                booking_date = datetime.fromisoformat(booking_data.booking_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
        
        # Create booking
        new_booking = crud.create_booking(
            db=db,
            customer_id=current_user.id,
            provider_id=booking_data.provider_id,
            skill_id=booking_data.skill_id,
            booking_date=booking_date,
            duration_hours=booking_data.duration_hours,
            notes=booking_data.notes
        )
        
        return {
            "success": True,
            "message": "Booking created successfully",
            "booking": new_booking.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create booking: {str(e)}")


@app.get("/bookings")
def get_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    as_customer: bool = Query(None, description="Filter bookings as customer"),
    as_provider: bool = Query(None, description="Filter bookings as provider")
):
    """Get bookings for current user (protected endpoint)"""
    try:
        if as_customer:
            bookings = crud.get_bookings_by_customer(db, current_user.id)
        elif as_provider:
            bookings = crud.get_bookings_by_provider(db, current_user.id)
        else:
            # Get all bookings (as customer and provider)
            customer_bookings = crud.get_bookings_by_customer(db, current_user.id)
            provider_bookings = crud.get_bookings_by_provider(db, current_user.id)
            bookings = customer_bookings + provider_bookings
        
        return {
            "success": True,
            "count": len(bookings),
            "bookings": [booking.to_dict() for booking in bookings]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get bookings: {str(e)}")


@app.get("/bookings/{booking_id}")
def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific booking by ID (protected endpoint)"""
    booking = crud.get_booking_by_id(db, booking_id)
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Only customer or provider can view the booking
    if booking.customer_id != current_user.id and booking.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this booking")
    
    return {
        "success": True,
        "booking": booking.to_dict()
    }


@app.patch("/bookings/{booking_id}/status")
def update_booking_status(
    booking_id: int,
    status_update: BookingStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update booking status (protected endpoint - only provider can update)"""
    booking = crud.get_booking_by_id(db, booking_id)
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Only provider can update booking status
    if booking.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the service provider can update booking status")
    
    # Validate status
    valid_statuses = ["pending", "accepted", "completed", "cancelled"]
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
    
    updated_booking = crud.update_booking_status(db, booking_id, status_update.status)
    
    return {
        "success": True,
        "message": f"Booking status updated to {status_update.status}",
        "booking": updated_booking.to_dict()
    }


@app.delete("/bookings/{booking_id}")
def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a booking (protected endpoint - customer or provider can cancel)"""
    booking = crud.get_booking_by_id(db, booking_id)
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Only customer or provider can cancel
    if booking.customer_id != current_user.id and booking.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this booking")
    
    # Update status to cancelled instead of deleting
    updated_booking = crud.update_booking_status(db, booking_id, "cancelled")
    
    return {
        "success": True,
        "message": "Booking cancelled successfully",
        "booking": updated_booking.to_dict()
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
