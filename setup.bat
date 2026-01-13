@echo off
echo ========================================
echo AI Career Intelligence System - Setup
echo ========================================
echo.

echo [1/2] Installing Frontend Dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo [2/2] Installing Backend Dependencies...
cd backend
call pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo 1. Run 'start-backend.bat' in one terminal
echo 2. Run 'start-frontend.bat' in another terminal
echo.
pause
