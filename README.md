# Tanach Tracker - מעקב לימוד תנ"ך

A Hebrew Bible reading tracker app with customizable reading plans (30, 60, or 90 days).

![Hebrew Interface](https://img.shields.io/badge/Language-Hebrew-blue)
![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey)

## Features

- 📖 Track your Tanach (Hebrew Bible) reading progress
- 📅 Three reading plans: 30, 60, or 90 days
- ✅ Daily checklist for Torah, Prophets, Writings, and Psalms
- 💾 Automatic progress saving
- 🇮🇱 Beautiful Hebrew interface

## Installation (macOS)

### ⚠️ Important: Gatekeeper Security Notice

macOS will block the app because it's not signed with an Apple Developer certificate. This is normal for free, open-source apps.

**Quick Fix (Method 1):**
1. Download and extract the app
2. **Right-click** (or Control-click) on `TanachTracker.app`
3. Select **"Open"**
4. Click **"Open"** in the dialog

**Alternative (Method 2):**
Open Terminal and run:
```bash
xattr -cr /path/to/TanachTracker.app
```

📄 **See `MACOS_INSTALL_INSTRUCTIONS.md` for detailed installation help**

## Download

Get the latest version from the [GitHub Actions](https://github.com/Noamiko613/Tanach-Tracker/actions) page:
1. Click on the latest successful workflow run
2. Download "TanachTracker-macOS" from Artifacts
3. Extract the ZIP file
4. Follow the installation instructions above

## Building from Source

See `BUILD_MACOS.md` for instructions on building the app yourself on macOS.

## Usage

1. Launch the app
2. Select your reading plan (30, 60, or 90 days)
3. Check off each section as you complete it
4. Click "שמור התקדמות" (Save Progress) when done
5. The app automatically advances to the next day when all items are checked

## Technical Details

- **Language:** Python 3.11+
- **GUI Framework:** PyQt6
- **Packaging:** PyInstaller
- **Platform:** macOS (arm64 & x86_64)

## License

Open source - free to use and modify

## Support

Having issues? Check `MACOS_INSTALL_INSTRUCTIONS.md` or open an issue on GitHub.

---

**עברית:**

יישום למעקב אחר קריאת התנ"ך עם תוכניות קריאה של 30, 60 או 90 יום.

לשאלות או בעיות, פנה דרך GitHub.
