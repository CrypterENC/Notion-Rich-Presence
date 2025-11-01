#!/usr/bin/env python3
"""
NotionPresence Build Script
Builds executable with PyInstaller and creates installer with Inno Setup
Run from project root: python build.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print()
    print("=" * 40)
    print(f"  {text}")
    print("=" * 40)
    print()


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"{description}...")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Error: {description} failed")
        sys.exit(1)


def main():
    print_header("NotionPresence Build Script")
    
    # Get project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    venv_path = project_root / "venv"
    venv_scripts = venv_path / "Scripts"
    
    # Check if virtual environment exists
    if not (venv_scripts / "activate.bat").exists():
        print("Creating virtual environment with Python 3.12...")
        run_command("py -3.12 -m venv venv", "Virtual environment creation")
    
    # Activate virtual environment (for Windows)
    activate_cmd = str(venv_scripts / "activate.bat")
    
    # Upgrade pip
    print()
    print("Upgrading pip...")
    python_exe = str(venv_scripts / "python.exe")
    run_command(f"{python_exe} -m pip install --upgrade pip", "Pip upgrade")
    
    # Install dependencies
    print()
    print("Installing dependencies...")
    run_command(f"{python_exe} -m pip install -r requirements.txt", "Dependency installation")
    
    # Clean previous builds
    print()
    print("Cleaning previous builds...")
    build_dist = project_root / "build" / "dist"
    build_build = project_root / "build" / "build"
    
    if build_dist.exists():
        shutil.rmtree(build_dist)
    if build_build.exists():
        shutil.rmtree(build_build)
    
    # Build executable with PyInstaller
    print()
    print("Building executable with PyInstaller...")
    python_exe = str(venv_scripts / "python.exe")
    run_command(
        f"{python_exe} -m PyInstaller --distpath=dist --workpath=build\\build NotionPresence.spec",
        "PyInstaller build"
    )
    
    print()
    print("Executable built successfully!")
    print(f"Location: {project_root / 'dist' / 'NotionPresence' / 'NotionPresence.exe'}")
    
    # Clean up build folder
    print()
    print("Cleaning up build folder...")
    build_folder = project_root / "build"
    if build_folder.exists():
        shutil.rmtree(build_folder)
    
    print_header("Build Complete!")
    print(f"Executable: {project_root / 'dist' / 'NotionPresence' / 'NotionPresence.exe'}")
    print()
    print("Next steps:")
    print("1. Test the executable: dist\\NotionPresence\\NotionPresence.exe")
    print("2. (Optional) Build installer with Inno Setup:")
    print("   - Install from: https://jrsoftware.org/isdl.php")
    print("   - Open: build/installer.iss")
    print("   - Build > Compile")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBuild cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
