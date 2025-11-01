# Building Tanach Tracker for macOS

## Important Note
**You cannot build a macOS app from Windows.** You must use one of these methods:

## Method 1: Build on a Mac Computer

### Prerequisites
1. Access to a Mac computer (or macOS virtual machine)
2. Python 3.8+ installed
3. Install dependencies:
```bash
pip install PyQt6 pyinstaller
# OR for cx_Freeze:
pip install PyQt6 cx-Freeze
```

### Option A: Using PyInstaller (Recommended)
1. Copy all project files to the Mac
2. Open Terminal and navigate to the project folder
3. Run:
```bash
pyinstaller main_macos.spec
```
4. The app will be in `dist/TanachTracker.app`

### Option B: Using cx_Freeze
1. Copy all project files to the Mac
2. Open Terminal and navigate to the project folder
3. Run:
```bash
python setup_macos.py bdist_mac
```
4. The app will be in `build/TanachTracker.app`

### Converting Icon (Optional)
If you want to convert the .ico to .icns (native macOS format):
```bash
# Install ImageMagick if needed
brew install imagemagick

# Convert
mkdir torah_icon.iconset
sips -z 16 16 torah_icon.ico --out torah_icon.iconset/icon_16x16.png
sips -z 32 32 torah_icon.ico --out torah_icon.iconset/icon_16x16@2x.png
sips -z 32 32 torah_icon.ico --out torah_icon.iconset/icon_32x32.png
sips -z 64 64 torah_icon.ico --out torah_icon.iconset/icon_32x32@2x.png
sips -z 128 128 torah_icon.ico --out torah_icon.iconset/icon_128x128.png
sips -z 256 256 torah_icon.ico --out torah_icon.iconset/icon_128x128@2x.png
iconutil -c icns torah_icon.iconset
```

## Method 2: Using GitHub Actions (Automated)

If you have this code in a GitHub repository, I can create a GitHub Actions workflow that automatically builds the macOS app for you.

### Benefits:
- No Mac needed
- Automatic builds
- Download the .app file from GitHub releases

Would you like me to create the GitHub Actions workflow file?

## Method 3: Using Cloud macOS Services

You can use cloud services that provide macOS environments:
- **MacStadium** (paid)
- **MacinCloud** (paid)
- **GitHub Codespaces** with macOS runner (requires GitHub Actions)

## Distribution

### Code Signing (Optional but Recommended)
For distributing to other Mac users:
1. Get an Apple Developer account ($99/year)
2. Sign the app:
```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" TanachTracker.app
```

### Creating a DMG (Optional)
To create a disk image for easy distribution:
```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "Tanach Tracker" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --app-drop-link 600 185 \
  "TanachTracker.dmg" \
  "dist/TanachTracker.app"
```

## Troubleshooting

### "TanachTracker.app is damaged" error
This happens with unsigned apps. Users can fix by:
```bash
xattr -cr /path/to/TanachTracker.app
```

### Python not found
Make sure Python 3 is installed:
```bash
brew install python3
```

### Qt platform plugin error
Reinstall PyQt6:
```bash
pip uninstall PyQt6
pip install PyQt6
```
