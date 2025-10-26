"""
PostgreSQL Setup Helper for HelpX
This script helps you configure your PostgreSQL connection.
"""

import getpass
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

def test_connection(password):
    """Test PostgreSQL connection with the provided password"""
    DATABASE_URL = f"postgresql://postgres:{password}@localhost:5432/postgres"
    
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"PostgreSQL version: {version[:50]}...")
            return True
    except OperationalError as e:
        if "password authentication failed" in str(e):
            print("❌ Wrong password. Please try again.")
            return False
        elif "could not connect to server" in str(e):
            print("❌ PostgreSQL server is not running or not installed.")
            print("Please install PostgreSQL from: https://www.postgresql.org/download/windows/")
            return None
        else:
            print(f"❌ Error: {e}")
            return False

def create_database(password):
    """Create the helpx database"""
    DATABASE_URL = f"postgresql://postgres:{password}@localhost:5432/postgres"
    
    try:
        engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")
        with engine.connect() as conn:
            # Check if database exists
            result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='helpx'"))
            if result.fetchone():
                print("✅ Database 'helpx' already exists!")
                return True
            else:
                # Create database
                conn.execute(text("CREATE DATABASE helpx"))
                print("✅ Database 'helpx' created successfully!")
                return True
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def update_config_file(password):
    """Update database.py with the correct password"""
    config_content = f'''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL Configuration
DATABASE_URL = "postgresql://postgres:{password}@localhost:5432/helpx"

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
'''
    
    try:
        with open('database.py', 'w') as f:
            f.write(config_content)
        print("✅ Configuration file updated successfully!")
        return True
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

def main():
    print("=" * 60)
    print("PostgreSQL Setup Helper for HelpX")
    print("=" * 60)
    print()
    
    # Get password from user
    password = getpass.getpass("Enter your PostgreSQL password for user 'postgres': ")
    
    print("\n🔍 Testing connection...")
    connection_status = test_connection(password)
    
    if connection_status is None:
        # PostgreSQL not installed or not running
        print("\n📝 To install PostgreSQL:")
        print("1. Download from: https://www.postgresql.org/download/windows/")
        print("2. Run the installer")
        print("3. Remember your password during installation")
        print("4. Run this script again after installation")
        return
    elif not connection_status:
        # Wrong password
        print("\n💡 Tips:")
        print("- Make sure you're using the password you set during PostgreSQL installation")
        print("- Try running pgAdmin 4 to verify your password")
        print("- Run this script again with the correct password")
        return
    
    # Connection successful, create database
    print("\n🔧 Creating database...")
    if not create_database(password):
        return
    
    # Update configuration file
    print("\n📝 Updating configuration...")
    if not update_config_file(password):
        return
    
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print("\n🚀 Next steps:")
    print("1. Run: python main.py")
    print("2. Your app will now use PostgreSQL database!")
    print("3. Open http://localhost:8000/docs to test your API")
    print()

if __name__ == "__main__":
    main()
