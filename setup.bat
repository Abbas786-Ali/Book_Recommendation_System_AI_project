@echo off
REM Quick Setup Script for Windows - Book Recommendation System

echo.
echo 🚀 Book Recommendation System - Windows Setup
echo ==========================================
echo.

REM Check if Python is available
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✓ Python version: %python_version%
echo.

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt > nul 2>&1

echo.
echo ✅ Setup Complete!
echo.
echo 📖 Next steps:
echo   1. Activate virtual environment:
echo      venv\Scripts\activate.bat
echo.
echo   2. Run the application:
echo      python run.py
echo.
echo   3. Open in browser:
echo      http://127.0.0.1:5000/
echo.
pause
