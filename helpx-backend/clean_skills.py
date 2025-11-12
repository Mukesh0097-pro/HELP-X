"""
Clean up database - Delete all bookings and skills
"""
from database import SessionLocal
from models import Booking, Skill

def clean_database():
    db = SessionLocal()
    
    try:
        # First, delete all bookings (they reference skills)
        bookings_deleted = db.query(Booking).delete()
        db.commit()
        print(f"✅ Deleted {bookings_deleted} bookings")
        
        # Now delete all skills
        skills_deleted = db.query(Skill).delete()
        db.commit()
        print(f"✅ Deleted {skills_deleted} skills")
        
        print("\n✅ Database cleaned successfully!")
        print("   All bookings and skills have been removed.")
        print("   Users are still intact.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("⚠️  This will delete ALL bookings and skills from the database!")
    response = input("Are you sure? (yes/no): ")
    
    if response.lower() == "yes":
        clean_database()
    else:
        print("❌ Cancelled")
