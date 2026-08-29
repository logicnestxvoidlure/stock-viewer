@echo off
title StockPulse - Free Stock Viewer
echo ========================================================
echo   StockPulse - Free Stock Viewer & Market Terminal
echo ========================================================
echo.

if not exist venv (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    call .\venv\Scripts\activate.bat
    echo [INFO] Installing required dependencies...
    pip install -r requirements.txt
) else (
    call .\venv\Scripts\activate.bat
)

echo [INFO] Starting StockPulse Web Server...
echo.
python app.py
pause
