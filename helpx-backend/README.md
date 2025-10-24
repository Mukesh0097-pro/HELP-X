# HelpX Backend - Skill Sharing Platform

A FastAPI backend for a skill-sharing platform where users can register, list their skills, and connect with others.

## 🚀 Features

- User registration and management
- Skill creation and listing
- RESTful API with FastAPI
- PostgreSQL database with SQLAlchemy ORM
- CORS enabled for frontend integration
- Interactive API documentation

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

## 🛠️ Installation

1. **Install PostgreSQL** (if not already installed)
   - Download from: https://www.postgresql.org/download/
   - Create a database named `helpx`

2. **Update database credentials**
   - Open `database.py`
   - Update the DATABASE_URL with your PostgreSQL credentials:
     ```python
     DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/helpx"
     ```
   - Replace `yourpassword` with your actual PostgreSQL password

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Running the Application

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

2. The API will be available at:
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

## 📡 API Endpoints

### Users

- **GET /users** - Get all users
  ```
  http://localhost:8000/users
  ```

- **POST /add-user** - Add a new user
  ```
  http://localhost:8000/add-user?name=John%20Doe&email=john@example.com
  ```

### Skills

- **GET /skills** - Get all skills (optional: filter by user_id)
  ```
  http://localhost:8000/skills
  http://localhost:8000/skills?user_id=1
  ```

- **POST /add-skill** - Add a new skill
  ```
  http://localhost:8000/add-skill?skill=Python&description=Advanced%20Python%20programming&user_id=1
  ```

## 📊 Database Schema

### User Model
- `id` - Primary Key (Integer)
- `name` - User's name (String)
- `email` - User's email (String, Unique)

### Skill Model
- `id` - Primary Key (Integer)
- `skill` - Skill name (String)
- `description` - Skill description (Text)
- `user_id` - Foreign Key to User (Integer)

## 🧪 Testing with Frontend

The backend includes CORS middleware, so you can connect it with the HTML/JS frontend in the `Frontend` folder.

## 📝 Notes

- Database tables are created automatically on startup
- All responses are in JSON format
- Email validation prevents duplicate user registration
- User ID validation ensures skills are linked to existing users

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.
