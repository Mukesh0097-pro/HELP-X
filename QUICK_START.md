# HelpX - Quick Start Guide

## 🎯 Two Options to Run the App

### Option 1: With PostgreSQL (Production-Ready)
Follow the detailed instructions in `SETUP_DATABASE.md`

### Option 2: Quick Demo (SQLite - No PostgreSQL needed)

1. **Edit database.py**:
   - Open `helpx-backend/database.py`
   - Comment line 6: `# DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/helpx"`
   - Uncomment line 10: `DATABASE_URL = "sqlite:///./helpx.db"`

2. **Start the Backend**:
   ```bash
   cd helpx-backend
   uvicorn main:app --reload
   ```

3. **Open the Frontend**:
   - Open `Frontend/Index.html` in your web browser
   - Or double-click the file

4. **Test the Application**:
   - Register a new user
   - Login with your credentials
   - Post services/skills
   - Browse available services

## 🌐 Access Points

- **Frontend**: `Frontend/Index.html`
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Interactive API Testing**: http://localhost:8000/redoc

## 📝 Quick Test

1. Open http://localhost:8000/docs
2. Try these endpoints:
   - POST `/add-user` - Add a user
   - GET `/users` - See all users
   - POST `/add-skill` - Add a skill
   - GET `/skills` - See all skills

## ⚡ Auto-Start Script

**Windows**: Double-click `START_APP.bat`

This will:
- Start the backend server automatically
- Open the frontend in your default browser

---

**Note**: The SQLite version is great for testing, but for production use PostgreSQL as specified in the original requirements.
