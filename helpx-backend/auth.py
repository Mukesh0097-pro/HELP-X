from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User

# Security configuration
SECRET_KEY = "your-secret-key-here-change-in-production-09876543210"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Ensure 'sub' is a string (JWT standard requires it)
    if 'sub' in to_encode and not isinstance(to_encode['sub'], str):
        to_encode['sub'] = str(to_encode['sub'])
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("❌ JWT Error: Token has expired")
        return None
    except jwt.JWTClaimsError as e:
        print(f"❌ JWT Error: Invalid claims - {e}")
        return None
    except JWTError as e:
        print(f"❌ JWT Error: {type(e).__name__} - {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error decoding token: {type(e).__name__} - {e}")
        return None

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    print(f"🔍 Received token: {token[:50]}..." if len(token) > 50 else f"🔍 Received token: {token}")
    payload = decode_token(token)
    
    if payload is None:
        print("❌ Token decode failed")
        raise credentials_exception
    
    print(f"✅ Token payload: {payload}")
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        print("❌ No user_id in payload")
        raise credentials_exception
    
    # Convert string user_id back to integer
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        print(f"❌ Invalid user_id format: {user_id_str}")
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        print(f"❌ User {user_id} not found in database")
        raise credentials_exception
    
    print(f"✅ Authenticated user: {user.name} (ID: {user.id})")
    return user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
