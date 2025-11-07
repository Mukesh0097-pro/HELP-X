from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL Configuration
# Set your actual postgres password (the password appears to be 'project8610@' so '@' is URL-encoded as %40)
DATABASE_URL = "postgresql://postgres:project8610%40@localhost:5432/helpx"

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
