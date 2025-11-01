# Changelog

All notable changes to NotionPresence will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-11-01 (Build & Packaging)

### Added
- 📦 **PyInstaller Build System** - Automated executable generation with `build.py`
- 🎯 **Professional Installer** - Inno Setup configuration with author information
- 🔧 **Build Automation** - Dependency management and clean build process
- 📝 **Installer Welcome Page** - Author and project information display

### Fixed
- ✅ **Icon Display** - Fixed Notion icon in title bar and taskbar (PNG → ICO conversion)
- ✅ **Title Bar Styling** - Removed underline border for cleaner appearance
- ✅ **Asset Bundling** - Properly included src/, styles/, and Assets/ in executable
- ✅ **PyInstaller Compatibility** - Resolved base_library.zip and DLL load errors
- ✅ **Custom UI Import** - Ensured all custom components bundled correctly

### Changed
- 🔄 **Build Tool**: Switched from Nuitka to PyInstaller for better PyQt6 compatibility
- 📦 **Spec File**: Created optimized PyInstaller.spec with collect_all() for dependencies
- 🎨 **Icon Format**: Updated from PNG to ICO for better Windows integration
- 📋 **Config File**: Marked as automatically added in documentation

### Technical Details

#### Build Configuration
- **PyInstaller**: 6.16.0
- **Build Mode**: --onedir (directory mode for stability)
- **Console**: Disabled (--windowed)
- **Icon**: Assets/Notion.ico
- **Output**: dist/NotionPresence/NotionPresence.exe

#### Bundled Assets
- `src/` - All source code and modules
- `styles/` - QSS stylesheet files
- `Assets/` - Icons and images
- `config.json` - Configuration template

#### Installer Features
- Modern wizard style
- Desktop shortcut option
- Startup option (unchecked by default)
- Author information display
- GitHub repository link
- Professional branding

---

## [1.0.0] - 2025-11-01

### Added

#### UI/UX Improvements
- ✨ **Modern Glassmorphism Design** - Beautiful semi-transparent UI with gradient backgrounds
- 🎨 **Custom Title Bar** - Frameless window with draggable title bar and control buttons
- 🎯 **Custom Dropdown Widget** - Modern, animated page selector with multiple size variants
- 📋 **Custom Dialog Components** - Styled info, warning, and error message dialogs
- 🔗 **GitHub Link** - Clickable link with pulsing glow animation
- 🎭 **Smooth Animations** - Professional transitions and hover effects

#### Core Features
- ✨ **Discord Rich Presence Integration** - Real-time presence updates every 30 seconds
- 📝 **Notion Workspace Integration** - Connect and display Notion pages
- 🎯 **Page Selection** - Modern dropdown to select which Notion page to track
- 📌 **System Tray Integration** - Minimize to tray with notification support
- 🪟 **Frameless Window** - Modern window design with custom controls
- 🖼️ **Discord Icon Support** - Display Notion icon in Discord presence

#### System Integration
- 🔄 **Auto-Startup Registration** - Automatic Windows registry integration
- 📦 **Professional Installer** - Inno Setup installer with optional startup
- 🎯 **Taskbar Icon** - Professional icon in taskbar and system tray
- 📋 **Registry Management** - Proper app registration in Windows
- 🚀 **Startup Options** - Optional run on system boot

#### Performance Optimizations
- ⚡ **Reduced Memory Usage** - Optimized from 63MB to 30-40MB
- 🔋 **Efficient Updates** - 30-second update interval (reduced from 10s)
- 🎨 **No Shadow Effects** - Removed GPU-intensive shadow effects
- 🚀 **Fast Startup** - < 2 seconds startup time

#### Window Controls
- **Minimize Button (−)** - Minimizes to taskbar silently
- **Close Button (✕)** - Minimizes to system tray with notification
- **Draggable Title Bar** - Click and drag to move window
- **System Tray Menu** - Right-click for options

#### Security Features
- 🔐 **Triple AES Encryption** - 3-layer encryption for sensitive data
- 🔑 **PBKDF2 Key Derivation** - 100,000 iterations for strong keys
- 🛡️ **Machine-Specific Keys** - Unique encryption per machine + user
- 📋 **Automatic Encryption** - Transparent encrypt/decrypt on save/load
- ⚠️ **Error Recovery** - Automatic config recovery on corruption
- 📄 **Security Documentation** - Comprehensive SECURITY.md guide

#### Developer Features
- 📚 **Reusable UI Components** - Custom UI library in `/custom_ui` folder
- 📖 **Comprehensive Documentation** - README with setup and troubleshooting
- 🔧 **Registry Manager** - Python module for Windows registry management
- 🔐 **Security Manager** - Python module for encryption/decryption
- 🎨 **Modern Styling** - Glassmorphism CSS with indigo/cyan color scheme

### Fixed
- ✅ Text rendering issues on startup
- ✅ Window positioning and layout
- ✅ Console warnings for unknown CSS properties
- ✅ Icon display in system tray
- ✅ Config file corruption handling
- ✅ Empty config file recovery
- ✅ JSON parsing errors with graceful fallback

### Changed
- 🔄 Updated presence update interval from 10s to 30s for better performance
- 🎨 Replaced standard QComboBox with CustomDropdown
- 🎭 Replaced standard title bar with CustomTitleBar
- 📊 Optimized memory usage by removing shadow effects
- 🪟 Changed window flags for better frameless support

### Technical Details

#### New Files
- `src/registry_manager.py` - Windows registry management
- `src/security_manager.py` - AES encryption/decryption with PBKDF2
- `custom_ui/custom_dropdown.py` - Modern dropdown widget
- `custom_ui/custom_titlebar.py` - Custom title bar component
- `custom_ui/custom_dialog.py` - Styled dialog components
- `custom_ui/demo.py` - UI components showcase
- `installer.iss` - Professional Inno Setup installer
- `SECURITY.md` - Comprehensive security documentation
- `requirements.txt` - Python dependencies

#### Modified Files
- `src/gui/window.py` - Integrated custom components and registry manager
- `src/gui/presence_manager.py` - Enhanced presence updates
- `README.md` - Comprehensive documentation

#### Dependencies
- PyQt6 (6.6.1) - GUI framework
- pypresence (4.3.0) - Discord Rich Presence
- requests (2.31.0) - HTTP library for Notion API
- cryptography (41.0.7) - AES encryption/PBKDF2
- psutil (5.9.6) - System utilities

### Performance Metrics
- **Memory**: 30-40 MB (down from 63 MB)
- **CPU**: Minimal usage with 30-second intervals
- **Startup**: < 2 seconds
- **Update Latency**: < 1 second

### Browser Compatibility
- Windows 10/11
- Python 3.8+

### Known Issues
- None reported

### Future Roadmap
- [ ] Multi-page presence tracking
- [ ] Custom status messages
- [ ] Theme customization
- [ ] Cross-platform support (macOS, Linux)
- [ ] Settings GUI
- [ ] Auto-update functionality

---

## Version History

### v1.0.0 (Current)
- Initial release with full feature set
- Professional UI with glassmorphism design
- Windows registry integration
- Professional installer

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](LICENSE) for details.

## Support

For issues and feature requests: https://github.com/CrypterENC/Notion-Rich-Presence/issues
