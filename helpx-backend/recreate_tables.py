"""
Recreate database tables with the correct schema
"""
from database import Base, engine
from models import User, Skill

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating all tables with new schema...")
Base.metadata.create_all(bind=engine)

print("✅ Tables recreated successfully!")
print("\nTables created:")
print("- users (id, name, email, hashed_password)")
print("- skills (id, skill, description, user_id)")
