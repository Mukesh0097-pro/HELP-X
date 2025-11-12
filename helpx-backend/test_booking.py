"""
Test script to verify booking functionality
"""
from database import SessionLocal
from models import User, Skill, Booking
import crud

def test_bookings():
    db = SessionLocal()
    
    try:
        # Check existing data
        users = db.query(User).all()
        skills = db.query(Skill).all()
        bookings = db.query(Booking).all()
        
        print("=" * 50)
        print("📊 CURRENT DATABASE STATE")
        print("=" * 50)
        print(f"Users: {len(users)}")
        for user in users[:5]:  # Show first 5
            print(f"  - ID {user.id}: {user.name} ({user.email})")
        
        print(f"\nSkills: {len(skills)}")
        for skill in skills[:5]:  # Show first 5
            print(f"  - ID {skill.id}: {skill.skill} (User ID: {skill.user_id})")
        
        print(f"\nBookings: {len(bookings)}")
        for booking in bookings:
            print(f"  - ID {booking.id}: Customer {booking.customer_id} -> Provider {booking.provider_id}, Status: {booking.status}")
        
        # Try to create a test booking if we have data
        if len(users) >= 2 and len(skills) >= 1:
            print("\n" + "=" * 50)
            print("🔨 CREATING TEST BOOKING")
            print("=" * 50)
            
            customer = users[0]
            provider = users[1] if len(users) > 1 else users[0]
            skill = skills[0]
            
            print(f"Customer: {customer.name} (ID: {customer.id})")
            print(f"Provider: {provider.name} (ID: {provider.id})")
            print(f"Skill: {skill.skill} (ID: {skill.id})")
            
            new_booking = crud.create_booking(
                db=db,
                customer_id=customer.id,
                provider_id=provider.id,
                skill_id=skill.id,
                duration_hours=2,
                notes="Test booking from script"
            )
            
            print(f"\n✅ Booking created! ID: {new_booking.id}")
            print(f"   Status: {new_booking.status}")
            print(f"   Created at: {new_booking.created_at}")
            
            # Test updating status
            print("\n" + "=" * 50)
            print("🔄 TESTING STATUS UPDATE")
            print("=" * 50)
            
            updated = crud.update_booking_status(db, new_booking.id, "accepted")
            print(f"✅ Status updated to: {updated.status}")
            
            # Verify it was saved
            retrieved = crud.get_booking_by_id(db, new_booking.id)
            print(f"✅ Verified from DB: {retrieved.status}")
            
        else:
            print("\n⚠️  Need at least 2 users and 1 skill to test")
            print("   Sign up some users and add skills first!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_bookings()
