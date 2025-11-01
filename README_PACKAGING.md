# macOS App Packaging Files

This project includes files for creating a macOS application bundle.

## Files Created

### 1. `setup_macos.py`
- **Purpose**: cx_Freeze setup script for building macOS apps
- **Usage**: Run on a Mac with `python setup_macos.py bdist_mac`

### 2. `main_macos.spec`
- **Purpose**: PyInstaller specification file for macOS app bundle
- **Usage**: Run on a Mac with `pyinstaller main_macos.spec`

### 3. `BUILD_MACOS.md`
- **Purpose**: Comprehensive instructions for building on macOS
- **Contains**: 
  - Prerequisites
  - Step-by-step build instructions
  - Code signing guidance
  - Troubleshooting tips

### 4. `.github/workflows/build-macos.yml`
- **Purpose**: GitHub Actions workflow for automatic building
- **Usage**: Push to GitHub and it will automatically build the app
- **Benefit**: No Mac computer needed!

## Quick Start

### If you have a Mac:
1. Read `BUILD_MACOS.md`
2. Run either:
   - `pyinstaller main_macos.spec` (recommended)
   - OR `python setup_macos.py bdist_mac`

### If you DON'T have a Mac:
1. Push this code to GitHub
2. The GitHub Actions workflow will automatically build it
3. Download the built app from the "Actions" tab

## Why Can't I Build from Windows?

Python packaging tools like PyInstaller and cx_Freeze create platform-specific executables. They cannot cross-compile - you must build on the target platform. This is a fundamental limitation of these tools.

## Need Help?

See `BUILD_MACOS.md` for detailed instructions and troubleshooting.
