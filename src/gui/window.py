import sys
import threading
import json
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QComboBox, QLineEdit, QMessageBox, QSystemTrayIcon, QMenu, QDialog, QGraphicsDropShadowEffect, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtGui import QIcon, QAction, QColor, QFont, QFontMetrics, QCursor
from PyQt6.QtCore import Qt, QTimer, QEvent, QFile, QUrl, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import Qt as QtCore
from .page_manager import PageManager
from .presence_manager import PresenceManager
from .setup_dialog import SetupDialog
from .custom_ui.custom_dialog import CustomMessageDialog
from .custom_ui.custom_dropdown import CustomDropdown
from .custom_ui.custom_titlebar import CustomTitleBar
from ..registry_manager import RegistryManager
from ..security_manager import SecurityManager

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and bundled app"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), '..', '..', relative_path)

class NotionDiscordGUI(QMainWindow):
    def __init__(self, client_id):
        super().__init__()
        # Apply frameless window style for custom title bar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        icon_path = get_resource_path('Assets/Notion.ico')
        self.setWindowIcon(QIcon(icon_path))
        try:
            # Load and decrypt config
            self.config = SecurityManager.load_encrypted_config('config.json')
            if not self.config:
                self.config = {"notion_token": "", "id": "", "client_id": ""}
        except:
            self.config = {"notion_token": "", "id": "", "client_id": ""}
        
        if not self.config.get('client_id') or not self.config.get('notion_token'):
            dialog = SetupDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                client_id = dialog.get_client_id()
                token = dialog.get_token()
                if client_id and token:
                    self.config['client_id'] = client_id
                    self.config['notion_token'] = token
                    try:
                        # Save config with encryption
                        SecurityManager.save_encrypted_config(self.config, 'config.json')
                    except:
                        pass
                    dialog_complete = CustomMessageDialog(
                        'Setup Complete',
                        'Configuration saved successfully!\n\nThe app will now restart to load your Notion pages.',
                        'info',
                        self
                    )
                    dialog_complete.exec()
                    # Restart the app
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                else:
                    dialog_error = CustomMessageDialog(
                        'Setup Required',
                        'Both Discord Client ID and Notion Integration Token are required to proceed.',
                        'error',
                        self
                    )
                    dialog_error.exec()
                    sys.exit(1)
            else:
                dialog_setup = CustomMessageDialog(
                    'Setup Required',
                    'Setup is required to use this application. Please provide your Discord Client ID and Notion Integration Token.',
                    'warning',
                    self
                )
                dialog_setup.exec()
                sys.exit(1)
        
        self.pages = []
        self.page_manager = PageManager(self)
        self.presence_manager = PresenceManager(self, self.config['client_id'])
        
        # Register app for startup on first launch
        if not RegistryManager.is_registered():
            success, message = RegistryManager.register_startup()
            if success:
                RegistryManager.create_app_registry_entries()
        
        self.init_ui()
        
        if self.config.get('notion_token'):
            self.page_manager.reload_pages()
        
        # Start Discord connection in a thread to avoid blocking GUI
        threading.Thread(target=self.presence_manager.connect_discord_thread, daemon=True).start()
        
        # Auto-update presence - increased interval to reduce CPU usage
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.presence_manager.auto_update_presence)
        self.auto_timer.start(30000)  # Check every 30 seconds instead of 10

    def init_ui(self):
        self.setWindowTitle('Notion Discord Auto RPC')
        self.setGeometry(100, 100, 600, 320)
        self.setFixedSize(600, 357)
        # Remove default window frame and buttons
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)

        # Load styles from external QSS file
        style_path = get_resource_path('styles/styles.qss')
        style_file = QFile(style_path)
        if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            self.setStyleSheet(str(style_file.readAll(), 'utf-8'))
            style_file.close()
        else:
            # Fallback inline styles if file not found
            self.setStyleSheet("""
                QWidget { background: #0a0e27; color: #e8f0ff; font-family: 'Segoe UI', sans-serif; font-size: 14px; }
                QLabel { color: #e8f0ff; }
                QPushButton { background: #6366f1; border: none; border-radius: 10px; padding: 10px 16px; color: #ffffff; font-weight: 600; font-size: 13px; }
                QPushButton:hover { background: #4f46e5; }
            """)

        # Central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add custom title bar
        icon_path = get_resource_path('Assets/Notion.ico')
        title_bar = CustomTitleBar(
            parent=self,
            title='Notion Discord Auto RPC',
            icon_path=icon_path,
            show_minimize=True,
            show_close=True
        )
        main_layout.addWidget(title_bar)
        
        # Content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 20, 40, 30)
        content_layout.setSpacing(8)

        # Section 1: Status label - optimized without shadow for performance
        self.status_label = QLabel('Status: Not connected to Discord')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.status_label.setObjectName("presenceLabel")
        self.status_label.setMinimumHeight(70)
        font_status = QFont('Segoe UI', 18, QFont.Weight.Bold)
        self.status_label.setFont(font_status)
        self.status_label.setWordWrap(True)
        content_layout.addWidget(self.status_label)
        
        # Section 2: Presence label - optimized without shadow for performance
        self.presence_label = QLabel('Presence: Not set')
        self.presence_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.presence_label.setObjectName("presence1Label")
        self.presence_label.move(0, 30)
        font_presence = QFont('Segoe UI', 13)
        self.presence_label.setFont(font_presence)
        content_layout.addWidget(self.presence_label)
        
        # Add gap after presence label
        content_layout.addSpacing(12)

        # Section 3: Page selector - Using Custom Dropdown
        self.page_combo = CustomDropdown()
        self.page_combo.setObjectName("pageCombo")
        self.page_combo.currentIndexChanged.connect(self.on_page_selected)
        content_layout.addWidget(self.page_combo)

        # Add gap after custom dropdown
        content_layout.addSpacing(12)

        # Section 4: Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        self.set_button = QPushButton('Set Presence')
        self.set_button.setMinimumHeight(40)
        self.set_button.clicked.connect(self.presence_manager.auto_update_presence)
        buttons_layout.addWidget(self.set_button)

        self.clear_button = QPushButton('Clear Presence')
        self.clear_button.setMinimumHeight(40)
        self.clear_button.clicked.connect(self.presence_manager.clear_presence)
        buttons_layout.addWidget(self.clear_button)
        
        content_layout.addLayout(buttons_layout)
        content_layout.addSpacing(12)
        
        # GitHub link label with glow animation
        github_link = QLabel('<a href="https://github.com/CrypterENC/Notion-Rich-Presence.git" style="color: #a5f3fc; text-decoration: none;">📌 View on GitHub</a>')
        github_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        github_link.setOpenExternalLinks(True)
        github_link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        github_link.setObjectName("githubLink")
        github_link.setStyleSheet("""
            QLabel#githubLink {
                color: #a5f3fc;
                font-size: 11px;
                padding: 8px;
                border-radius: 6px;
            }
            QLabel#githubLink:hover {
                color: #6366f1;
                background: rgba(99, 102, 241, 0.1);
                border: 1px solid rgba(99, 102, 241, 0.3);
            }
        """)
        
        # Add glow effect using shadow with fixed blur
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(10)
        glow_effect.setXOffset(0)
        glow_effect.setYOffset(0)
        glow_effect.setColor(QColor(165, 243, 252, 150))
        github_link.setGraphicsEffect(glow_effect)
        
        # Create pulsing animation for glow color opacity
        self.glow_animation = QPropertyAnimation(glow_effect, b"color")
        color_start = QColor(165, 243, 252, 80)
        color_end = QColor(165, 243, 252, 200)
        self.glow_animation.setStartValue(color_start)
        self.glow_animation.setEndValue(color_end)
        self.glow_animation.setDuration(1500)
        self.glow_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.glow_animation.setLoopCount(-1)
        self.glow_animation.start()
        
        content_layout.addWidget(github_link)
        
        content_layout.addStretch()
        
        main_layout.addWidget(content_widget)

        # System Tray
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = get_resource_path('Assets/Notion.png')
        # Create larger tray icon (48x48 instead of default)
        tray_icon = QIcon(icon_path)
        self.tray_icon.setIcon(tray_icon)
        self.tray_icon.setToolTip('NotionPresence - Notion Discord Auto RPC')

        # Create enhanced tray menu
        tray_menu = QMenu()
        tray_menu.setStyleSheet("""
            QMenu {
                background: linear-gradient(135deg, #0a0e27 0%, #0f1535 100%);
                color: #e8f0ff;
                border: 1px solid rgba(99, 102, 241, 0.3);
                border-radius: 8px;
                padding: 8px 0px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
            QMenu::item:selected {
                background: rgba(99, 102, 241, 0.3);
                border-radius: 6px;
                margin: 2px 4px;
                padding: 6px 12px;
            }
            QMenu::item {
                padding: 6px 12px;
                margin: 2px 4px;
            }
            QMenu::separator {
                background: rgba(99, 102, 241, 0.2);
                height: 1px;
                margin: 6px 0px;
            }
        """)
        
        # Show action
        show_action = QAction('👁 Show Window', self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)
        
        # Set Presence action
        set_presence_action = QAction('✓ Set Presence', self)
        set_presence_action.triggered.connect(self.presence_manager.auto_update_presence)
        tray_menu.addAction(set_presence_action)
        
        # Clear Presence action
        clear_presence_action = QAction('✕ Clear Presence', self)
        clear_presence_action.triggered.connect(self.presence_manager.clear_presence)
        tray_menu.addAction(clear_presence_action)
        
        # Separator
        tray_menu.addSeparator()
        
        # Status indicator
        status_action = QAction('● Status: Connected', self)
        status_action.setEnabled(False)
        tray_menu.addAction(status_action)
        
        # Separator
        tray_menu.addSeparator()
        
        # Quit action
        quit_action = QAction('⊗ Quit', self)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            if self.windowState() & Qt.WindowState.WindowMinimized:
                self.hide()
        super().changeEvent(event)

    def closeEvent(self, event):
        # Hide to tray instead of closing - app continues running
        self.hide()
        self.tray_icon.showMessage('NotionPresence', 'App minimized to tray. Right-click to quit.', QSystemTrayIcon.MessageIcon.Information, 3000)
        event.ignore()

    def on_page_selected(self):
        selected_id = self.page_combo.currentData()
        self.config['id'] = selected_id
        try:
            # Save config with encryption
            SecurityManager.save_encrypted_config(self.config, 'config.json')
        except:
            pass
        self.presence_manager.auto_update_presence()
