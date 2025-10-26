from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# IMPORTANT: Before running, make sure PostgreSQL is installed and running!
# Update the password below with your PostgreSQL password
DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/helpx"

# For testing without PostgreSQL, you can use SQLite instead:
# Uncomment the line below to use SQLite (no PostgreSQL needed)
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
