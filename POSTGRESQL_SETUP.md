# PostgreSQL Setup Guide for HelpX

## ✅ Configuration Status
Your database configuration has been switched to **PostgreSQL**.

## 📋 Setup Steps

### 1. Install PostgreSQL
If you haven't installed PostgreSQL yet:
1. Download from: https://www.postgresql.org/download/windows/
2. Run the installer
3. **Remember the password** you set for the `postgres` user during installation
4. Default port: `5432` (keep this unless you have a specific reason to change)

### 2. Create the Database

**Option A - Using pgAdmin 4 (GUI):**
1. Open **pgAdmin 4** (installed with PostgreSQL)
2. Connect to your local PostgreSQL server (enter your postgres password)
3. Right-click on **"Databases"** → **Create** → **Database**
4. Name: `helpx`
5. Click **Save**

**Option B - Using psql (Command Line):**
```powershell
# Open Command Prompt or PowerShell and run:
psql -U postgres

# Then in the psql prompt:
CREATE DATABASE helpx;
\q
```

### 3. Update Your Database Password

⚠️ **IMPORTANT:** Edit the file `helpx-backend\database.py`

Find this line:
```python
DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/helpx"
```

Replace `yourpassword` with your actual PostgreSQL password:
```python
DATABASE_URL = "postgresql://postgres:YOUR_ACTUAL_PASSWORD@localhost:5432/helpx"
```

### 4. Verify PostgreSQL is Running

**Check if PostgreSQL service is running:**
1. Press `Win + R`
2. Type `services.msc` and press Enter
3. Look for **"postgresql-x64-XX"** service
4. Status should be **"Running"**

If not running, right-click and select **Start**.

### 5. Test the Connection

Start your backend to create the tables automatically:

```powershell
cd helpx-backend
python main.py
```

If successful, you'll see:
- Server starting on `http://127.0.0.1:8000`
- No database connection errors

The tables (`users` and `skills`) will be created automatically in your PostgreSQL database!

## 🔍 Verify Tables Were Created

**Using pgAdmin:**
1. Open pgAdmin 4
2. Navigate to: Servers → PostgreSQL → Databases → helpx → Schemas → public → Tables
3. You should see: `users` and `skills` tables

**Using psql:**
```powershell
psql -U postgres -d helpx

# Then run:
\dt
```

You should see both `users` and `skills` tables listed.

## 📊 Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| name | VARCHAR(100) | User's full name |
| email | VARCHAR(100) | Unique email (indexed) |
| hashed_password | VARCHAR(255) | Bcrypt hashed password |

### Skills Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| skill | VARCHAR(100) | Skill name |
| description | TEXT | Skill description |
| user_id | INTEGER | Foreign key to users.id |

## 🔧 Connection String Format

```
postgresql://username:password@host:port/database_name
```

Current configuration:
- **Username:** postgres
- **Password:** [YOUR_PASSWORD]
- **Host:** localhost
- **Port:** 5432
- **Database:** helpx

## ⚠️ Troubleshooting

### Error: "could not connect to server"
- Make sure PostgreSQL service is running
- Check if port 5432 is not blocked by firewall

### Error: "password authentication failed"
- Double-check your password in `database.py`
- Try resetting the postgres user password in pgAdmin

### Error: "database 'helpx' does not exist"
- Create the database using pgAdmin or psql (see Step 2)

### Error: "psycopg2 not found"
- Run: `pip install psycopg2-binary==2.9.9`

## 🎯 Next Steps

After setup is complete:
1. Update your password in `database.py`
2. Run the backend: `python main.py`
3. Open your browser to `http://localhost:8000/docs` to test the API
4. Register a new user through the frontend
5. Check the database to see your data stored in PostgreSQL!

## 🔐 Security Note for Production

For production deployment:
- Never commit passwords to Git
- Use environment variables for sensitive data
- Create a `.env` file:
  ```
  DATABASE_URL=postgresql://postgres:your_password@localhost:5432/helpx
  ```
- Update `database.py` to read from environment variables:
  ```python
  import os
  DATABASE_URL = os.getenv("DATABASE_URL")
  ```
