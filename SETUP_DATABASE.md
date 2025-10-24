# PostgreSQL Database Setup for HelpX

## 📋 Prerequisites

You need PostgreSQL installed on your system. If you don't have it:

### Download and Install PostgreSQL:
1. Visit: https://www.postgresql.org/download/windows/
2. Download the latest PostgreSQL installer
3. Run the installer
4. During installation, remember the password you set for the 'postgres' user

## 🗄️ Create Database

### Option 1: Using pgAdmin (GUI)
1. Open **pgAdmin 4** (installed with PostgreSQL)
2. Connect to your PostgreSQL server
3. Right-click on "Databases" → Create → Database
4. Name: `helpx`
5. Click "Save"

### Option 2: Using Command Line (psql)
1. Open Command Prompt or PowerShell
2. Run:
   ```bash
   psql -U postgres
   ```
3. Enter your PostgreSQL password
4. Create database:
   ```sql
   CREATE DATABASE helpx;
   \q
   ```

## ⚙️ Update Backend Configuration

1. Open `helpx-backend/database.py`
2. Update the DATABASE_URL with your PostgreSQL password:
   ```python
   DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/helpx"
   ```
   Replace `YOUR_PASSWORD` with your actual PostgreSQL password

## ✅ Verify Connection

Run this command in the helpx-backend directory:
```bash
python -c "from database import engine; engine.connect(); print('✅ Database connection successful!')"
```

If you see "✅ Database connection successful!", you're ready to go!

## 🚀 Start the Application

### Option 1: Use the Batch Script
Double-click `START_APP.bat` in the project root

### Option 2: Manual Start
1. Start Backend:
   ```bash
   cd helpx-backend
   uvicorn main:app --reload
   ```
2. Open Frontend:
   Open `Frontend/Index.html` in your browser

## 🔧 Troubleshooting

### Error: "connection refused"
- Make sure PostgreSQL service is running
- Windows: Check Services → PostgreSQL should be "Running"

### Error: "password authentication failed"
- Check your password in `database.py`
- Make sure you're using the correct PostgreSQL user password

### Error: "database 'helpx' does not exist"
- Create the database using one of the methods above

## 📊 Database Tables

The following tables will be created automatically when you start the backend:

- **users**: Stores user information (id, name, email)
- **skills**: Stores skills/services (id, skill, description, user_id)

No manual table creation needed! 🎉
