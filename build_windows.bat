@echo off
echo ===============================================
echo Building Tanach Tracker for Windows
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Installing/Updating dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Building executable with PyInstaller...
pyinstaller --clean main_windows.spec

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ===============================================
echo Build Complete!
echo ===============================================
echo.
echo Your executable is located at:
echo %CD%\dist\TanachTracker.exe
echo.
echo You can now run TanachTracker.exe
echo.
pause
