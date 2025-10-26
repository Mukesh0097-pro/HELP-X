# 🚀 How to Start HelpX Application

## Quick Start (2 Steps)

### Step 1: Start the Backend Server

Open **PowerShell** or **Command Prompt** and run:

```powershell
cd "C:\Users\asus\OneDrive\Desktop\EE-PROJECT\HELP-X\helpx-backend"
python main.py
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process
INFO:     Application startup complete.
```

✅ **Keep this window open!** This is your backend server.

---

### Step 2: Open the Frontend

**Option A - Double Click:**
- Navigate to: `C:\Users\asus\OneDrive\Desktop\EE-PROJECT\HELP-X\Frontend`
- Double-click `Index.html`

**Option B - Using PowerShell:**
```powershell
Start-Process "C:\Users\asus\OneDrive\Desktop\EE-PROJECT\HELP-X\Frontend\Index.html"
```

---

## 🎯 Even Easier - Use the Batch File!

Just **double-click** this file:
```
C:\Users\asus\OneDrive\Desktop\EE-PROJECT\HELP-X\START_APP.bat
```

This will:
1. Start the backend automatically
2. Open the frontend in your browser

---

## 🛑 How to Stop the Application

### Stop Backend:
- Go to the PowerShell window running the backend
- Press `Ctrl + C`
- Type `Y` if asked to confirm

### Close Frontend:
- Simply close your browser tab

---

## ✅ Verify Everything is Working

### Check Backend:
Open in browser: http://localhost:8000

You should see:
```json
{
  "message": "Welcome to HelpX API - A Skill Sharing Platform",
  "docs": "/docs"
}
```

### Check API Documentation:
Open: http://localhost:8000/docs

You should see the Swagger UI with all API endpoints.

---

## 🔧 Troubleshooting

### Problem: "python is not recognized"
**Solution:** Install Python from https://www.python.org/downloads/

### Problem: "No module named 'fastapi'"
**Solution:** Install dependencies:
```powershell
cd "C:\Users\asus\OneDrive\Desktop\EE-PROJECT\HELP-X\helpx-backend"
pip install -r requirements.txt
```

### Problem: Backend won't start
**Solution:** Check if port 8000 is already in use:
```powershell
# Find process using port 8000
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# Kill the process
Stop-Process -Name python -Force
```

### Problem: Frontend can't connect to backend
**Solution:**
1. Make sure backend is running (Step 1)
2. Check http://localhost:8000 works
3. Refresh the frontend page

---

## 📝 Daily Workflow

1. **Morning:**
   ```powershell
   cd "C:\Users\asus\OneDrive\Desktop\EE-PROJECT\HELP-X\helpx-backend"
   python main.py
   ```
   Then open `Index.html`

2. **Working:**
   - Backend runs in background
   - Frontend in browser
   - Make changes to code
   - Refresh browser to see changes

3. **Evening:**
   - Press `Ctrl + C` in backend terminal
   - Close browser

---

## 🎓 Understanding the Components

### Backend (Port 8000)
- **Location:** `helpx-backend/main.py`
- **Purpose:** API server, database, authentication
- **URL:** http://localhost:8000
- **Docs:** http://localhost:8000/docs

### Frontend (Browser)
- **Location:** `Frontend/Index.html`
- **Purpose:** User interface
- **Connects to:** http://localhost:8000

### Database
- **Location:** `helpx-backend/helpx.db`
- **Type:** SQLite
- **Auto-created:** First time you run backend

---

## 🔄 Restart After Code Changes

### Backend Changes:
The server auto-reloads! Just save your file and it restarts automatically.

### Frontend Changes:
Press `F5` or `Ctrl + R` to refresh the browser.

---

## 💡 Pro Tips

### Use Multiple Terminals:
- **Terminal 1:** Backend server (keep running)
- **Terminal 2:** Run other commands (git, pip, etc.)

### Bookmark These:
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: `C:\Users\asus\OneDrive\Desktop\EE-PROJECT\HELP-X\Frontend\Index.html`

### Quick Backend Check:
```powershell
# See if backend is running
curl http://localhost:8000
```

---

## 📦 One-Time Setup (Already Done)

These steps are already completed, but if you move the project:

```powershell
# Navigate to backend
cd "path\to\helpx-backend"

# Install dependencies
pip install -r requirements.txt

# That's it! Now you can run: python main.py
```

---

## 🚀 Alternative: VS Code Integrated Terminal

If you use VS Code:

1. Open VS Code
2. Open folder: `HELP-X`
3. Open integrated terminal (`Ctrl + ~`)
4. Run:
   ```powershell
   cd helpx-backend
   python main.py
   ```
5. Right-click `Index.html` → Open with Live Server (or default browser)

---

## ✨ Summary - Two Simple Commands

**Every time you want to run your app:**

```powershell
# 1. Start Backend (in PowerShell)
cd "C:\Users\asus\OneDrive\Desktop\EE-PROJECT\HELP-X\helpx-backend"
python main.py

# 2. Open Frontend (double-click or run)
Start-Process "C:\Users\asus\OneDrive\Desktop\EE-PROJECT\HELP-X\Frontend\Index.html"
```

**That's it!** 🎉

---

## 📞 Quick Reference Card

```
┌─────────────────────────────────────────┐
│         HelpX Quick Start               │
├─────────────────────────────────────────┤
│ Backend Start:                          │
│   cd helpx-backend                      │
│   python main.py                        │
│                                         │
│ Backend Stop:                           │
│   Ctrl + C                              │
│                                         │
│ Frontend Open:                          │
│   Double-click Index.html               │
│                                         │
│ Backend URL:                            │
│   http://localhost:8000                 │
│                                         │
│ API Docs:                               │
│   http://localhost:8000/docs            │
└─────────────────────────────────────────┘
```

---

**Now you can start your HelpX app anytime!** 🚀
