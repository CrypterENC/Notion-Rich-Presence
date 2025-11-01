# NotionPresence - Notion Discord Auto RPC

![GitHub](https://img.shields.io/badge/GitHub-CrypterENC%2FNotion--Rich--Presence-blue?style=flat-square&logo=github)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)

A modern, feature-rich application to display your current Notion page activity on Discord Rich Presence with a beautiful glassmorphism UI.

## 🎯 Features

### Core Functionality
- ✨ **Real-time Discord Presence** - Auto-updates every 30 seconds
- 📝 **Notion Integration** - Connect to your Notion workspace
- 🎨 **Modern UI** - Glassmorphism design with smooth animations
- 🎯 **Custom Dropdown** - Modern page selector with multiple size variants
- 📌 **System Tray** - Minimize to tray with notification support
- 🔄 **Auto-Startup** - Automatically runs on Windows startup
- 🖼️ **Discord Rich Presence** - Display Notion icon and page details

### UI Components
- **Custom Title Bar** - Frameless window with draggable title bar
- **Custom Dropdown** - Modern, animated dropdown widget
- **Custom Dialogs** - Info, Warning, and Error message dialogs
- **Glow Animation** - GitHub link with pulsing glow effect
- **Smooth Transitions** - Professional animations throughout

### System Integration
- 🪟 **Windows Registry** - Automatic app registration
- 📦 **Installer** - Professional Inno Setup installer
- 🚀 **Startup Integration** - Optional startup on boot
- 🎯 **Taskbar Icon** - Professional icon in taskbar and system tray

### Security
- 🔐 **Triple AES Encryption** - 3 layers of encryption for sensitive data
- 🔑 **PBKDF2 Key Derivation** - 100,000 iterations for strong keys
- 🛡️ **Machine-Specific Keys** - Unique encryption per machine + user
- 📋 **Automatic Encryption** - Transparent encryption/decryption
- ⚠️ **Error Recovery** - Automatic config recovery on corruption

## 📋 Requirements

- **Windows 10/11** (built with PyInstaller)
- **Python 3.8+** (if running from source)
- **Internet connection** for API calls
- **Discord** running for Rich Presence

## 🚀 Installation

### Option 1: Using Installer (Recommended)
1. [Download](https://github.com/CrypterENC/Notion-Rich-Presence/releases/download/v1.0.0/NotionPresence_Installer_v1.0.1.exe) `NotionPresence_Installer_v1.0.1.exe`
2. Run the installer
3. Optionally enable "Run on system startup"
4. Launch the app

### Option 2: From Source
```bash
git clone https://github.com/CrypterENC/Notion-Rich-Presence.git
cd NotionPresence
pip install -r requirements.txt
python main.py
```

## ⚙️ Setup

### 1. Discord Application
1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Copy your **Client ID**
4. Go to "Rich Presence" → "Art Assets"
5. Upload `Notion.png` as asset named `notion`

### 2. Notion Integration
1. Visit https://www.notion.so/my-integrations
2. Create a new integration
3. Copy the **Internal Integration Token**
4. Share your workspace/pages with the integration

### 3. App Configuration
1. Launch NotionPresence
2. Enter your Discord Client ID
3. Enter your Notion Integration Token
4. Click "Save"
5. Select a page from the dropdown
6. Click "Set Presence"

## 📖 Usage

### Basic Operations
- **Set Presence**: Click "Set Presence" to update Discord with current page
- **Clear Presence**: Click "Clear Presence" to remove Discord status
- **Select Page**: Use dropdown to choose which Notion page to track
- **Minimize**: Click minimize button (−) to minimize to taskbar
- **Close**: Click close button (✕) to minimize to system tray

### System Tray
- **Double-click tray icon**: Restore window
- **Right-click menu**: 
  - Show/Hide window
  - Quit application

### Startup
- App automatically registers for Windows startup on first launch
- Optional during installation
- Can be managed via Windows Registry

## 🎨 UI Features

### Modern Design
- Glassmorphism effects with semi-transparent backgrounds
- Gradient backgrounds (indigo/cyan color scheme)
- Smooth hover transitions
- Professional typography

### Custom Components
- **CustomDropdown**: Modern page selector with animations
- **CustomTitleBar**: Frameless window with control buttons
- **CustomDialog**: Styled message dialogs
- **GitHub Link**: With pulsing glow animation

## 🔧 Configuration

### config.json (Automatically added)
```json
{
  "notion_token": "your_notion_token_here",
  "id": "your_page_id_here",
  "client_id": "your_discord_client_id_here"
}
```

### Registry Entries
- **Startup**: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
- **Uninstall**: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Uninstall`

## 🔐 Security

### Encryption
- **Triple AES Encryption**: All sensitive data (tokens, IDs) encrypted 3 times
- **PBKDF2 Key Derivation**: 100,000 iterations with SHA256
- **Machine-Specific Keys**: Unique per machine and user
- **Transparent**: Automatic encryption/decryption, no manual steps

### Protected Data
- ✅ Notion Integration Token - Encrypted
- ✅ Discord Client ID - Encrypted
- ❌ Page ID - Not encrypted (not sensitive)

### Error Recovery
- Automatic config recovery on corruption
- Creates fresh config if file is empty or corrupted
- Graceful degradation - app continues safely

For detailed security information, see [SECURITY.md](SECURITY.md)

## 📊 Performance

- **Memory Usage**: ~30-40 MB
- **CPU Usage**: Minimal (30-second update interval)
- **Startup Time**: < 2 seconds
- **No Shadow Effects**: Optimized for performance

## 🐛 Troubleshooting

### Icon not showing in Discord
1. Verify asset name is exactly `notion` (lowercase)
2. Restart Discord completely
3. Restart the app
4. Wait 30 seconds for Discord to refresh

### App not starting on boot
1. Run app with administrator privileges once
2. Check Windows Registry for startup entry
3. Verify app path in registry

### Connection issues
1. Check internet connection
2. Verify Notion token is valid
3. Verify Discord Client ID is correct
4. Ensure Discord is running

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and feature requests, visit: https://github.com/CrypterENC/Notion-Rich-Presence/issues

## 🙏 Credits

- Built with PyQt6
- Discord Rich Presence via pypresence
- Notion API integration
- Custom UI components with glassmorphism design
