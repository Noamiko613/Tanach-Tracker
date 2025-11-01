# How to Install Tanach Tracker on macOS

## The "Unidentified Developer" Issue

When you download and try to open the app, macOS may block it with a message like:
> "TanachTracker.app can't be opened because it is from an unidentified developer."

This is a security feature called **Gatekeeper**. Since this app is not signed with an Apple Developer certificate ($99/year), you'll need to manually allow it.

## Solution: Allow the App (2 Easy Methods)

### Method 1: Right-Click to Open (Easiest)
1. Download and extract the app
2. **Don't** double-click the app
3. Instead, **right-click** (or Control-click) on `TanachTracker.app`
4. Select **"Open"** from the menu
5. A dialog will appear with an "Open" button - click it
6. The app will now open and remember this choice for future launches

### Method 2: Terminal Command (Quick Fix)
1. Download and extract the app to your desired location (e.g., Applications folder)
2. Open Terminal (press Cmd+Space, type "Terminal", press Enter)
3. Copy and paste this command:
```bash
xattr -cr /Applications/TanachTracker.app
```
4. Press Enter
5. Now you can double-click the app normally

**Note:** Replace `/Applications/TanachTracker.app` with the actual path if you placed it elsewhere.

### Method 3: System Settings (One-Time Setup)
1. Try to open the app (it will be blocked)
2. Go to **System Settings** (or System Preferences on older macOS)
3. Click **Privacy & Security**
4. Scroll down to the **Security** section
5. You'll see a message about TanachTracker being blocked
6. Click **"Open Anyway"**
7. Confirm by clicking **"Open"** in the next dialog

## Moving Forward

After using any of these methods once, macOS will remember your choice and the app will open normally from then on.

## Why This Happens

Apple requires developers to:
1. Pay $99/year for an Apple Developer account
2. Sign all apps with their certificate

Since this is a free, open-source app, it's not commercially signed. The workarounds above are completely safe and standard for running open-source macOS apps.

## Troubleshooting

### If the app still won't open:
Try this Terminal command to check for issues:
```bash
codesign -dvv /Applications/TanachTracker.app
```

### If you get "damaged app" error:
Run this command:
```bash
xattr -cr /Applications/TanachTracker.app
sudo spctl --master-disable  # Disables Gatekeeper entirely (not recommended)
```

Then try opening the app again.

## For Advanced Users

If you want to completely disable Gatekeeper (not recommended for security):
```bash
sudo spctl --master-disable
```

To re-enable it:
```bash
sudo spctl --master-enable
```
