from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError

# Connect to default postgres database (@ is encoded as %40 in URL)
try:
    engine = create_engine('postgresql://postgres:project8610%40@localhost:5432/postgres', isolation_level='AUTOCOMMIT')
    
    with engine.connect() as conn:
        # Check if database exists
        result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='helpx'"))
        exists = result.fetchone()
        
        if exists:
            print("✅ Database 'helpx' already exists!")
        else:
            # Create database
            conn.execute(text("CREATE DATABASE helpx"))
            print("✅ Database 'helpx' created successfully!")
    
    engine.dispose()
    print("\n🎉 PostgreSQL setup complete!")
    print("You can now run: python main.py")
    
except OperationalError as e:
    if "password authentication failed" in str(e):
        print("❌ Password authentication failed!")
        print("Please check your PostgreSQL password.")
    elif "could not connect" in str(e):
        print("❌ Could not connect to PostgreSQL server!")
        print("Make sure PostgreSQL is installed and running.")
    else:
        print(f"❌ Error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
