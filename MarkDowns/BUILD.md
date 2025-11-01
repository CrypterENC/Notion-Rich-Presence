# Build Guide - NotionPresence

This guide explains how to build NotionPresence from source into a standalone executable and create an installer.

## Prerequisites

### System Requirements
- **Windows 10/11** (64-bit recommended)
- **Python 3.8+** installed and in PATH
- **PyInstaller** for creating executables
- **Inno Setup** for creating the installer

### Required Tools

1. **Python 3.8+**
   - Download from: https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **PyInstaller**
   - Installed via pip (see installation steps below)

3. **Inno Setup 6.0+**
   - Download from: https://jrsoftware.org/isdl.php
   - Install to default location (C:\Program Files (x86)\Inno Setup 6)

## Step 1: Prepare Environment

### 1.1 Clone Repository
```bash
git clone https://github.com/CrypterENC/Notion-Rich-Presence.git
cd NotionPresence
```

### 1.2 Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### 1.4 Verify Installation
```bash
python main.py
```

The app should launch successfully before building.

## Step 2: Build Executable with PyInstaller

### 2.1 Create PyInstaller Spec File

The spec file is already provided: `build/NotionPresence.spec`

### 2.2 Build the Executable

From the project root:
```bash
pyinstaller build/NotionPresence.spec
```

**Build Output:**
- Executable: `dist/NotionPresence/NotionPresence.exe`
- Supporting files: `dist/NotionPresence/` (all dependencies)

### 2.3 Verify Build

Test the built executable:
```bash
dist\NotionPresence\NotionPresence.exe
```

The app should launch and function identically to the source version.

## Step 3: Create Installer with Inno Setup

### 3.1 Prepare Installer Files

Ensure the following files exist:
- `build/installer.iss` - Inno Setup script
- `Assets/Notion.png` - App icon
- `dist/NotionPresence/` - Built executable and files

### 3.2 Build Installer

**Option A: Using Inno Setup GUI**
1. Open Inno Setup
2. File → Open → Select `build/installer.iss`
3. Build → Compile
4. Output: `userdocs:Inno Setup Output/NotionPresence_Installer.exe`

**Option B: Using Command Line**
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build/installer.iss
```

### 3.3 Installer Output

The installer will be created at:
```
NotionPresence_Installer.exe
```

Located in your Documents folder under "Inno Setup Output"

## Step 4: Test Installation

### 4.1 Run Installer
1. Double-click `NotionPresence_Installer.exe`
2. Follow the installation wizard
3. Choose installation options:
   - ✅ Create desktop icon (optional)
   - ✅ Run on system startup (optional)
4. Click "Install"

### 4.2 Verify Installation
1. Launch app from Start Menu or Desktop
2. Verify all features work:
   - Discord presence updates
   - Notion page selection
   - System tray functionality
   - Settings persistence

### 4.3 Test Uninstall
1. Go to Add/Remove Programs
2. Find "Notion Discord Auto RPC"
3. Click Uninstall
4. Verify app is removed

## Automated Build Script

Use the provided `build/build.bat` script for automated building:

```bash
build\build.bat
```

This script will:
1. Create virtual environment
2. Install dependencies
3. Build executable
4. Create installer
5. Display results

## Troubleshooting

### PyInstaller Issues

**Issue: "ModuleNotFoundError" when running executable**
- Solution: Add missing modules to `hiddenimports` in spec file
- Rebuild with: `pyinstaller build/NotionPresence.spec --clean`

**Issue: Icon not showing in executable**
- Solution: Ensure `Assets/Notion.png` exists and path is correct in spec file
- Rebuild and verify

**Issue: App crashes on startup**
- Solution: Run with console to see errors:
  - Change `console=False` to `console=True` in spec file
  - Rebuild and run to see error messages

### Inno Setup Issues

**Issue: "ISCC.exe not found"**
- Solution: Install Inno Setup from https://jrsoftware.org/isdl.php
- Verify installation path: `C:\Program Files (x86)\Inno Setup 6\`

**Issue: Installer won't run**
- Solution: Run as Administrator
- Check Windows Defender/Antivirus isn't blocking

**Issue: App won't start after installation**
- Solution: Check config.json exists in `%LOCALAPPDATA%\NotionPresence\`
- Verify all dependencies are included in installer

## Build Optimization

### Reduce Executable Size

Add to spec file:
```python
# Remove unnecessary modules
excludedimports=[
    'matplotlib',
    'numpy',
    'pandas',
]

# Use UPX compression
upx=True
```

### Faster Builds

```bash
# Skip analysis cache
pyinstaller build/NotionPresence.spec --clean

# Use onefile (slower but single executable)
# Change in spec: exe = EXE(..., onefile=True, ...)
```

## Distribution

### Release Checklist

- [ ] Update version in code
- [ ] Update CHANGELOG.md
- [ ] Build executable with PyInstaller
- [ ] Test executable thoroughly
- [ ] Build installer with Inno Setup
- [ ] Test installer on clean Windows machine
- [ ] Create GitHub release
- [ ] Upload NotionPresence_Installer.exe to release
- [ ] Update README with download link

### File Structure for Release

```
NotionPresence_v1.0.0/
├── NotionPresence_Installer.exe
├── README.md
├── CHANGELOG.md
├── LICENSE
└── SECURITY.md
```

## Advanced Configuration

### Code Signing (Optional)

For production releases, sign the executable:

```bash
# Requires code signing certificate
signtool sign /f certificate.pfx /p password NotionPresence.exe
```

### Version Information

Update in spec file:
```python
exe = EXE(
    ...,
    version_file='version_info.txt',
    ...
)
```

## Support

For build issues:
1. Check Python version: `python --version`
2. Verify dependencies: `pip list`
3. Check PyInstaller version: `pyinstaller --version`
4. Review build logs for errors
5. Open GitHub issue: https://github.com/CrypterENC/Notion-Rich-Presence/issues

## References

- **PyInstaller Docs**: https://pyinstaller.org/
- **Inno Setup Docs**: https://jrsoftware.org/ishelp/
- **Python Packaging**: https://packaging.python.org/

---

**Last Updated**: 2025-11-01
**Version**: 1.0.0
**Status**: Production Ready
