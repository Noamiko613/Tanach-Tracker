# Building Tanach Tracker for Windows

This guide will help you create a standalone Windows executable (.exe) for the Tanach Tracker application.

## Prerequisites

- Windows OS
- Python 3.8 or higher installed ([Download Python](https://www.python.org/downloads/))
- Internet connection (for installing dependencies)

## Quick Build Instructions

### Method 1: Using the Build Script (Easiest)

1. Open the folder containing the Tanach Tracker files
2. Double-click `build_windows.bat`
3. Wait for the build process to complete
4. The executable will be in the `dist` folder as `TanachTracker.exe`

### Method 2: Manual Build

1. Open Command Prompt in the project directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Build the executable:
   ```bash
   pyinstaller --clean main_windows.spec
   ```
4. Find your executable in the `dist` folder

## Running the Application

After building, you can:

1. Navigate to the `dist` folder
2. Double-click `TanachTracker.exe` to run the application
3. (Optional) Copy `TanachTracker.exe` to any location on your computer

## Features

The application includes professional animations for:

- ✨ **Checkbox clicks** - Smooth pulse animation with visual feedback
- 🎉 **Day completion** - Confetti celebration when finishing a day
- 🏅 **Milestone achievements**:
  - 50% completion - Encouraging message with confetti
  - 75% completion - Motivational boost
- 🏆 **Plan completion** - Grand celebration when finishing 30/60/90 day plan

## Troubleshooting

### "Python is not recognized"
- Make sure Python is installed and added to your PATH
- During Python installation, check "Add Python to PATH"

### Build fails
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Delete `build` and `dist` folders, then rebuild
- Try: `pip install --upgrade pyinstaller`

### Executable won't run
- Make sure `torah_icon.ico` is in the same folder during build
- Try running from Command Prompt to see error messages
- Check Windows Defender/Antivirus isn't blocking the file

## File Structure After Build

```
Tanach-Tracker/
├── dist/
│   └── TanachTracker.exe  ← Your standalone executable
├── build/                  ← Temporary build files (can be deleted)
├── main.py
├── main_windows.spec
├── build_windows.bat
└── torah_icon.ico
```

## Distributing the Application

The `TanachTracker.exe` file is completely standalone and can be:

- Copied to any Windows computer (no Python required)
- Shared with others
- Placed anywhere on your system
- Run without internet connection

The application will create `progress.json` and `progress.txt` files in the same directory as the executable to track your progress.

## Support

If you encounter any issues, please check:
1. Python version: `python --version` (should be 3.8+)
2. PyInstaller version: `pyinstaller --version`
3. All files are present in the project directory
