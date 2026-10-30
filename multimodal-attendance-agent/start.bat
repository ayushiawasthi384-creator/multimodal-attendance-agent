@echo off
TITLE Multimodal Attendance & Engagement Agent - Launcher
echo ======================================================================
echo    Multimodal Attendance ^& Engagement Agent - Classroom Intelligence
echo ======================================================================
echo.

echo [1/3] Checking environment directories...
if not exist "backend\storage\audio" mkdir "backend\storage\audio"
if not exist "backend\storage\code" mkdir "backend\storage\code"
if not exist "backend\storage\reports" mkdir "backend\storage\reports"
if not exist "backend\uploads" mkdir "backend\uploads"

echo [2/3] Checking Python dependencies...
python -m pip install -r backend\requirements.txt --quiet

echo [3/3] Starting Flask Classroom Intelligence API Gateway on http://localhost:5000 ...
echo.
echo ======================================================================
echo   Open in your browser:
echo   - Full-Stack Dashboard:  http://localhost:5000
echo   - Standalone Preview:   demo_preview\index.html
echo ======================================================================
echo.

cd backend
python app.py
pause
