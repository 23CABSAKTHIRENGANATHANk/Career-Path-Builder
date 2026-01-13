@echo off
echo ============================================
echo Starting AI Career Intelligence Backend
echo ============================================
echo.

cd backend

echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Starting Flask server...
python app.py

pause
