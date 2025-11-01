# Setting Up GitHub to Build Your macOS App

## Step 1: Initialize Git Repository

Open a terminal in your project folder and run:

```bash
git init
git add .
git commit -m "Initial commit with macOS build setup"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (name it something like "tanach-tracker")
3. **DO NOT** initialize it with README, .gitignore, or license (we already have these)
4. Click "Create repository"

## Step 3: Push to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.

## Step 4: Watch the Build

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. You should see the "Build macOS App" workflow running
4. Wait for it to complete (takes about 5-10 minutes)

## Step 5: Download Your macOS App

Once the workflow completes:

1. Click on the completed workflow run
2. Scroll down to "Artifacts"
3. Download "TanachTracker-macOS" or "TanachTracker-macOS-DMG"
4. Extract the ZIP file
5. You'll have your `TanachTracker.app`!

## Troubleshooting

### If the workflow fails:
- Click on the failed workflow to see error details
- The most common issue is missing dependencies (already handled in the workflow)

### If you need to rebuild:
- Just push any new commit to GitHub:
  ```bash
  git add .
  git commit -m "Update"
  git push
  ```
- The workflow will automatically run again

### To manually trigger the build:
1. Go to the "Actions" tab
2. Click "Build macOS App" workflow
3. Click "Run workflow" button
4. Select the branch and click "Run workflow"

## What Happens Behind the Scenes

The GitHub Actions workflow:
1. Spins up a macOS virtual machine
2. Installs Python and dependencies (PyQt6, PyInstaller)
3. Runs PyInstaller to build the macOS app
4. Optionally creates a DMG disk image
5. Makes the app available for download

All of this happens automatically in the cloud - no Mac needed!
