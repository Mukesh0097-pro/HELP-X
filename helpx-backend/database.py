from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL Configuration
# NOTE: Replace YOUR_PASSWORD with your actual postgres password
DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/helpx"

# For testing with SQLite instead (comment line above and uncomment below):
# DATABASE_URL = "sqlite:///./helpx.db"

# Create database engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
