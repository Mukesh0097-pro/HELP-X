"""
Check what data is stored in the PostgreSQL database
"""
from database import SessionLocal
from models import User, Skill

db = SessionLocal()

print("=" * 60)
print("CHECKING DATABASE CONTENTS")
print("=" * 60)

# Check users
print("\n📊 USERS TABLE:")
print("-" * 60)
users = db.query(User).all()
if users:
    for user in users:
        print(f"ID: {user.id}")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        print(f"Has Password: {'Yes' if user.hashed_password else 'No'}")
        print("-" * 60)
    print(f"Total users: {len(users)}")
else:
    print("❌ No users found in database")

# Check skills
print("\n📊 SKILLS TABLE:")
print("-" * 60)
skills = db.query(Skill).all()
if skills:
    for skill in skills:
        print(f"ID: {skill.id}")
        print(f"Skill: {skill.skill}")
        print(f"Description: {skill.description}")
        print(f"User ID: {skill.user_id}")
        print(f"Owner: {skill.owner.name if skill.owner else 'Unknown'}")
        print("-" * 60)
    print(f"Total skills: {len(skills)}")
else:
    print("❌ No skills found in database")

db.close()
print("\n✅ Database check complete!")
