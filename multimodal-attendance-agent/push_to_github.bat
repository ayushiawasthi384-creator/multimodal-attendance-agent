@echo off
TITLE Push to GitHub - Multimodal Attendance & Engagement Agent
echo ======================================================================
echo    Pushing Multimodal Attendance & Engagement Agent to GitHub
echo ======================================================================
echo.

set /p REPO_URL="Enter your remote GitHub repository URL (e.g. https://github.com/username/multimodal-attendance-agent.git): "
if "%REPO_URL%"=="" (
    echo [ERROR] Repository URL cannot be empty.
    pause
    exit /b
)

echo.
echo [1/4] Initializing Git...
git init
git branch -M main

echo [2/4] Staging files...
git add .

echo [3/4] Committing project milestone...
git commit -m "feat: complete Multimodal Attendance & Engagement Agent with Epics 1-6"

echo [4/4] Setting remote and pushing...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git push -u origin main

echo.
echo ======================================================================
echo    Repository successfully synced with GitHub!
echo ======================================================================
pause
