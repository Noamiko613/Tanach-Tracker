"""
cx_Freeze setup script for macOS app bundle
Run on macOS: python setup_macos.py bdist_mac
"""
import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "packages": ["PyQt6", "json", "os"],
    "include_files": [
        ("torah_icon.ico", "torah_icon.ico"),
    ],
    "excludes": ["tkinter"],
}

# Base for GUI application
base = "gui" if sys.platform == "darwin" else None

setup(
    name="Tanach Tracker",
    version="1.0",
    description="מעקב לימוד תנ\"ך - Tanach Reading Tracker",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            target_name="TanachTracker",
            icon="torah_icon.ico",
        )
    ],
)
