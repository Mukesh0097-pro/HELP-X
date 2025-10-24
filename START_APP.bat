@echo off
echo ====================================
echo      Starting HelpX Application
echo ====================================
echo.

:: Start Backend Server
echo [1/2] Starting Backend Server...
start cmd /k "cd /d helpx-backend && python main.py"
timeout /t 3 /nobreak >nul

:: Open Frontend in Browser
echo [2/2] Opening Frontend...
timeout /t 2 /nobreak >nul
start Frontend/Index.html

echo.
echo ====================================
echo    HelpX Application Started!
echo ====================================
echo.
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: Opening in your browser...
echo.
echo Press any key to exit this window...
pause >nul
