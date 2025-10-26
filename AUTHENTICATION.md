# 🔐 Authentication System - HelpX

## ✅ Complete Authentication Implemented!

Your HelpX application now has **full authentication** with industry-standard security practices.

---

## 🎯 What's Been Added

### Backend Authentication (FastAPI)

#### 1. **Password Hashing with bcrypt**
- Passwords are never stored in plain text
- Uses bcrypt algorithm for secure hashing
- Automatic salt generation

#### 2. **JWT Token Authentication**
- JSON Web Tokens for stateless authentication
- Tokens expire after 24 hours
- Secure token generation with HS256 algorithm

#### 3. **Protected Endpoints**
- `/add-skill` now requires authentication
- Automatic user identification from token
- 401 Unauthorized for invalid/missing tokens

#### 4. **New Authentication Endpoints**

**POST `/register`**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```
Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**POST `/login`**
```json
{
  "email": "john@example.com",
  "password": "securepass123"
}
```
Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**GET `/me`** (Protected)
- Requires: `Authorization: Bearer <token>` header
- Returns current user information

---

## 📁 New Files Added

### `helpx-backend/auth.py`
Contains all authentication logic:
- `get_password_hash()` - Hash passwords
- `verify_password()` - Verify passwords
- `create_access_token()` - Generate JWT tokens
- `decode_token()` - Decode JWT tokens
- `get_current_user()` - Get user from token
- `authenticate_user()` - Verify email/password

### Updated Files

**`models.py`**
- Added `hashed_password` field to User model

**`crud.py`**
- Updated `create_user()` to hash passwords

**`main.py`**
- Added `/register` and `/login` endpoints
- Added `/me` endpoint (protected)
- Updated `/add-skill` to use authentication
- Protected routes require Bearer token

**`requirements.txt`**
- `passlib[bcrypt]==1.7.4` - Password hashing
- `python-jose[cryptography]==3.3.0` - JWT tokens
- `bcrypt==4.1.2` - Bcrypt algorithm

---

## 🎨 Frontend Integration

### Token Storage
- JWT tokens stored in `localStorage`
- Persistent sessions across browser refreshes
- Automatic token attachment to API calls

### Authentication Flow

1. **Registration**:
   - User fills form → POST to `/register`
   - Backend hashes password
   - Backend returns JWT token
   - Frontend stores token and user info
   - User logged in automatically

2. **Login**:
   - User enters credentials → POST to `/login`
   - Backend verifies password
   - Backend returns JWT token
   - Frontend stores token
   - User logged in

3. **Protected Actions**:
   - Frontend attaches token to requests
   - Header: `Authorization: Bearer <token>`
   - Backend validates token
   - Action performed if valid

4. **Logout**:
   - Frontend clears token from localStorage
   - User redirected to login page

---

## 🔒 Security Features

### ✅ Password Security
- **Bcrypt hashing**: Industry-standard algorithm
- **Automatic salting**: Each password has unique salt
- **One-way encryption**: Cannot reverse-engineer passwords
- **Minimum length**: 6 characters enforced

### ✅ Token Security
- **JWT tokens**: Stateless, self-contained
- **Token expiration**: 24 hours validity
- **Secret key**: Encrypted with secret key
- **Bearer scheme**: Standard HTTP authentication

### ✅ API Security
- **Protected endpoints**: Require valid tokens
- **Automatic user identification**: No need to pass user_id
- **401 Unauthorized**: Clear error messages
- **CORS enabled**: Controlled cross-origin access

---

## 📊 Database Schema Changes

### User Table (Updated)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL  -- NEW FIELD
);
```

**Note**: Old database was deleted and recreated with new schema.

---

## 🧪 Testing Authentication

### Test with API Docs (http://localhost:8000/docs)

1. **Register a User**:
   - Go to POST `/register`
   - Click "Try it out"
   - Enter:
     ```json
     {
       "name": "Test User",
       "email": "test@example.com",
       "password": "test123456"
     }
     ```
   - Execute
   - Copy the `access_token` from response

2. **Use Protected Endpoint**:
   - Go to POST `/add-skill`
   - Click "Authorize" button (🔒)
   - Paste your token
   - Click "Authorize"
   - Try adding a skill

3. **Get Current User**:
   - Go to GET `/me`
   - Execute (token already set)
   - See your user info

### Test with Frontend

1. **Register**:
   - Open frontend
   - Click "Register here"
   - Fill form with valid details
   - Click "Register"
   - ✅ You're logged in automatically!

2. **Logout and Login**:
   - Click "Logout"
   - Click "Login here"
   - Enter your email and password
   - Click "Login"
   - ✅ Welcome back!

3. **Post a Service**:
   - Click "+ Post Service"
   - Fill in service details
   - Click "Post Service"
   - ✅ Service created with your user ID!

4. **Refresh Browser**:
   - Press F5
   - ✅ Still logged in (token persists)!

---

## 🔄 How It Works

### Registration Flow
```
User Form → Frontend
    ↓
POST /register {name, email, password}
    ↓
Backend: Hash password with bcrypt
    ↓
Backend: Save to database
    ↓
Backend: Generate JWT token
    ↓
Return {token, user}
    ↓
Frontend: Store in localStorage
    ↓
User logged in ✅
```

### Login Flow
```
User Form → Frontend
    ↓
POST /login {email, password}
    ↓
Backend: Find user by email
    ↓
Backend: Verify password hash
    ↓
Backend: Generate JWT token
    ↓
Return {token, user}
    ↓
Frontend: Store in localStorage
    ↓
User logged in ✅
```

### Protected Request Flow
```
User Action → Frontend
    ↓
Add Header: Authorization: Bearer <token>
    ↓
POST /add-skill {skill, description}
    ↓
Backend: Extract token
    ↓
Backend: Decode & validate token
    ↓
Backend: Get user from token
    ↓
Backend: Create skill for user
    ↓
Return success
```

---

## 🛡️ Security Best Practices Implemented

1. ✅ **Never store plain text passwords**
2. ✅ **Hash passwords with bcrypt**
3. ✅ **Use JWT for stateless authentication**
4. ✅ **Set token expiration**
5. ✅ **Validate tokens on protected routes**
6. ✅ **Return proper HTTP status codes**
7. ✅ **Clear error messages**
8. ✅ **HTTPS ready** (use HTTPS in production)

---

## 🚀 Production Recommendations

### Before Deploying:

1. **Change Secret Key**:
   ```python
   # In auth.py
   SECRET_KEY = "your-production-secret-key-very-long-and-random"
   ```
   Generate a secure key:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Use Environment Variables**:
   ```python
   import os
   SECRET_KEY = os.getenv("SECRET_KEY")
   DATABASE_URL = os.getenv("DATABASE_URL")
   ```

3. **Enable HTTPS**:
   - All traffic should use HTTPS
   - JWT tokens are sensitive

4. **Update CORS**:
   ```python
   allow_origins=["https://yourdomain.com"]  # Specific domain
   ```

5. **Set Shorter Token Expiration**:
   ```python
   ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
   ```

6. **Add Refresh Tokens** (Optional):
   - Implement token refresh mechanism
   - Extend sessions without re-login

---

## 📝 API Endpoints Summary

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/register` | POST | ❌ No | Register new user |
| `/login` | POST | ❌ No | Login and get token |
| `/me` | GET | ✅ Yes | Get current user |
| `/users` | GET | ❌ No | List all users |
| `/skills` | GET | ❌ No | List all skills |
| `/add-skill` | POST | ✅ Yes | Add new skill |
| `/add-user` | POST | ❌ No | Legacy endpoint |

---

## ✨ Benefits

1. **Security**: Passwords are protected
2. **Scalability**: Stateless JWT tokens
3. **User Experience**: Persistent sessions
4. **Professional**: Industry-standard practices
5. **Flexible**: Easy to extend with more features

---

## 🎉 Success!

Your HelpX application now has:
- ✅ Secure password hashing
- ✅ JWT token authentication
- ✅ Protected API endpoints
- ✅ Persistent user sessions
- ✅ Professional security practices

**Ready for production (after security checklist)!** 🚀

---

## 📞 Quick Reference

**Test Credentials** (after registration):
- Email: your-email@example.com
- Password: your-password

**Token Header Format**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Check if logged in** (Frontend):
```javascript
if (authToken && isLoggedIn) {
    // User is authenticated
}
```
