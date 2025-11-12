"""
Create a second test user for booking testing
"""
from database import SessionLocal
import crud

def create_test_users():
    db = SessionLocal()
    
    try:
        # Check existing users
        existing = crud.get_user_by_email(db, "testprovider@helpx.com")
        
        if existing:
            print(f"✅ Test provider already exists: {existing.name} (ID: {existing.id})")
        else:
            # Create test provider
            provider = crud.create_user(
                db=db,
                name="John Provider",
                email="testprovider@helpx.com",
                password="password123"
            )
            print(f"✅ Created test provider: {provider.name} (ID: {provider.id})")
            
            # Add a skill for the provider
            skill = crud.create_skill(
                db=db,
                skill="Test Service",
                description="A test service for booking",
                user_id=provider.id
            )
            print(f"✅ Created skill: {skill.skill} (ID: {skill.id})")
        
        # Show all users
        users = crud.get_all_users(db)
        print(f"\n📋 Total users: {len(users)}")
        for user in users:
            print(f"   - {user.name} ({user.email}) - ID: {user.id}")
        
        skills = crud.get_all_skills(db)
        print(f"\n📋 Total skills: {len(skills)}")
        for skill in skills:
            print(f"   - {skill.skill} by User ID {skill.user_id}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users()
