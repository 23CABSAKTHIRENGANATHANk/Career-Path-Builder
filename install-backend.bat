@echo off
echo ========================================
echo Installing Backend Dependencies (Fast)
echo ========================================
echo.

cd backend
pip install flask flask-cors PyPDF2 python-docx

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Now run: start-all.bat
echo.
pause
