@echo off
setlocal EnableDelayedExpansion
echo ====================================
echo      Starting HelpX Application
echo ====================================
echo.

REM Check Firebase service account env var
if not defined GOOGLE_APPLICATION_CREDENTIALS (
	echo [WARN] GOOGLE_APPLICATION_CREDENTIALS not set. Firebase Admin may fail verifying ID tokens.
	echo        Set it before running, e.g.:
	echo        set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account.json
	echo.
)

REM Start Backend Server (port 8000)
echo [1/3] Starting Backend Server...
start "HelpX-Backend" cmd /k "cd /d helpx-backend && python main.py"
timeout /t 3 /nobreak >nul

REM Start Frontend static server (Python http.server on port 5500)
echo [2/3] Starting Frontend static server (port 5500)...
pushd Frontend >nul
start "HelpX-Frontend" cmd /k "python -m http.server 5500"
popd >nul
timeout /t 3 /nobreak >nul

REM Open browser to served Index.html
echo [3/3] Opening Frontend in browser...
start "" http://localhost:5500/Index.html

echo.
echo ====================================
echo    HelpX Application Started!
echo ====================================
echo.
echo Backend API:   http://localhost:8000
echo API Docs:      http://localhost:8000/docs
echo Frontend App:  http://localhost:5500/Index.html
echo.
echo NOTE: Close the Frontend/Backend terminals to stop servers.
echo Press any key to exit this launcher window...
pause >nul
endlocal
