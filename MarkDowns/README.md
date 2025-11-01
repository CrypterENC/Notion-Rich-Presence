# Build Folder

This folder contains all build-related files and scripts for NotionPresence.

## Contents

- **BUILD.md** - Comprehensive build guide with step-by-step instructions
- **build.bat** - Automated build script (run from project root)
- **NotionPresence.spec** - PyInstaller configuration file
- **installer.iss** - Inno Setup installer configuration

## Quick Start

### Automated Build (Recommended)

From the project root directory:
```bash
build\build.bat
```

This will:
1. Create virtual environment
2. Install dependencies
3. Build executable with PyInstaller
4. Create installer with Inno Setup

### Manual Build

**Build Executable:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller build/NotionPresence.spec
```

**Build Installer:**
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build/installer.iss
```

## Output Files

After building:
- **Executable**: `dist/NotionPresence/NotionPresence.exe`
- **Installer**: `NotionPresence_Installer.exe` (in Documents/Inno Setup Output)

## Requirements

- Python 3.8+
- PyInstaller
- Inno Setup 6.0+

## Documentation

For detailed instructions, see [BUILD.md](BUILD.md)

## File Paths

All paths in the build files are relative to the project root:
- `build/NotionPresence.spec` - Spec file location
- `build/installer.iss` - Installer script location
- `build/build.bat` - Build script location
- `Assets/Notion.png` - Icon location (referenced from root)
- `dist/NotionPresence/` - Output location (created during build)

## Troubleshooting

See BUILD.md for common issues and solutions.

---

**Version**: 1.0.0
**Last Updated**: 2025-11-01
