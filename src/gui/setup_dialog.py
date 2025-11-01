import sys
import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QGraphicsDropShadowEffect, QFrame
from PyQt6.QtGui import QIcon, QColor, QFont
from PyQt6.QtCore import Qt, QFile

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and bundled app"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), '..', '..', relative_path)

class SetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drag_position = None
        self.setWindowTitle('Setup Notion Token')
        icon_path = get_resource_path('Assets/Notion.png')
        self.setWindowIcon(QIcon(icon_path))
        self.setFixedSize(500, 380)
        self.setModal(True)
        
        # Apply frameless window style
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        # Load styles from external QSS file
        style_path = get_resource_path('styles/setup_styles.qss')
        style_file = QFile(style_path)
        if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            self.setStyleSheet(str(style_file.readAll(), 'utf-8'))
            style_file.close()
        else:
            # Fallback inline styles
            self.setStyleSheet("""
                QDialog { background: linear-gradient(135deg, #0a0e27 0%, #0f1535 100%); }
                QLabel { color: #e8f0ff; font-family: 'Segoe UI', sans-serif; }
                QLineEdit { background: rgba(26, 31, 58, 0.7); border: 2px solid #2d3561; border-radius: 12px; padding: 12px; color: #ffffff; font-size: 13px; }
                QLineEdit:focus { border: 2px solid #6366f1; background: rgba(34, 40, 68, 0.9); }
                QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6366f1, stop:1 #4f46e5); border: none; border-radius: 12px; padding: 12px 20px; color: #ffffff; font-weight: 600; font-size: 13px; }
                QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7c3aed, stop:1 #6366f1); }
                QPushButton:pressed { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4338ca, stop:1 #3730a3); }
            """)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Title bar
        title_bar = QFrame()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(40)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(16, 0, 16, 0)
        title_bar_layout.setSpacing(8)
        
        # Title label
        title_label = QLabel('Setup Notion Token')
        title_label.setObjectName("titleLabel")
        title_label.setStyleSheet("font-weight: 600; font-size: 13px; color: #e8f0ff;")
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        
        # Close button
        self.close_btn = QPushButton('✕')
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setStyleSheet("""
            QPushButton#closeBtn {
                background: transparent;
                border: none;
                color: #e8f0ff;
                font-size: 16px;
                font-weight: bold;
                padding: 0px;
            }
            QPushButton#closeBtn:hover {
                background: rgba(239, 68, 68, 0.3);
                border-radius: 6px;
            }
            QPushButton#closeBtn:pressed {
                background: rgba(239, 68, 68, 0.5);
            }
        """)
        self.close_btn.clicked.connect(self.reject)
        title_bar_layout.addWidget(self.close_btn)
        
        main_layout.addWidget(title_bar)
        
        # Content area
        content_widget = QFrame()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 25, 30, 30)
        content_layout.setSpacing(16)

        # Client ID label and input
        client_label = QLabel('Enter your Discord Client ID:')
        client_label.setFont(QFont('Segoe UI', 12, QFont.Weight.Bold))
        content_layout.addWidget(client_label)

        self.client_input = QLineEdit()
        self.client_input.setObjectName("inputField")
        self.client_input.setMinimumHeight(40)
        self.client_input.setPlaceholderText("Paste your Discord Client ID here...")
        
        # Add shadow to client input
        shadow_client = QGraphicsDropShadowEffect()
        shadow_client.setBlurRadius(10)
        shadow_client.setXOffset(0)
        shadow_client.setYOffset(2)
        shadow_client.setColor(QColor(0, 0, 0, 60))
        self.client_input.setGraphicsEffect(shadow_client)
        content_layout.addWidget(self.client_input)

        # Token label and input
        token_label = QLabel('Enter your Notion Integration Token:')
        token_label.setFont(QFont('Segoe UI', 12, QFont.Weight.Bold))
        content_layout.addWidget(token_label)

        self.token_input = QLineEdit()
        self.token_input.setObjectName("inputField")
        self.token_input.setMinimumHeight(40)
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_input.setPlaceholderText("Paste your Notion Integration Token here...")
        
        # Add shadow to token input
        shadow_token = QGraphicsDropShadowEffect()
        shadow_token.setBlurRadius(10)
        shadow_token.setXOffset(0)
        shadow_token.setYOffset(2)
        shadow_token.setColor(QColor(0, 0, 0, 60))
        self.token_input.setGraphicsEffect(shadow_token)
        content_layout.addWidget(self.token_input)

        content_layout.addSpacing(10)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        ok_button = QPushButton('OK')
        ok_button.setMinimumHeight(40)
        ok_button.clicked.connect(self.accept)
        
        # Add shadow to OK button
        shadow_ok = QGraphicsDropShadowEffect()
        shadow_ok.setBlurRadius(12)
        shadow_ok.setXOffset(0)
        shadow_ok.setYOffset(3)
        shadow_ok.setColor(QColor(99, 102, 241, 120))
        ok_button.setGraphicsEffect(shadow_ok)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton('Cancel')
        cancel_button.setMinimumHeight(40)
        cancel_button.clicked.connect(self.reject)
        
        # Add shadow to Cancel button
        shadow_cancel = QGraphicsDropShadowEffect()
        shadow_cancel.setBlurRadius(12)
        shadow_cancel.setXOffset(0)
        shadow_cancel.setYOffset(3)
        shadow_cancel.setColor(QColor(99, 102, 241, 120))
        cancel_button.setGraphicsEffect(shadow_cancel)
        button_layout.addWidget(cancel_button)

        content_layout.addLayout(button_layout)
        
        main_layout.addWidget(content_widget)

    def get_token(self):
        return self.token_input.text().strip()

    def get_client_id(self):
        return self.client_input.text().strip()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
