from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtGui import QIcon, QColor, QFont, QPixmap
from PyQt6.QtCore import Qt, QFile, QSize

class CustomMessageDialog(QDialog):
    def __init__(self, title, message, icon_type="info", parent=None):
        super().__init__(parent)
        self.drag_position = None
        self.setWindowTitle(title)
        self.setFixedSize(500, 280)
        self.setModal(True)
        
        # Apply frameless window style
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        # Load styles
        style_file = QFile('setup_styles.qss')
        if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            self.setStyleSheet(str(style_file.readAll(), 'utf-8'))
            style_file.close()
        else:
            # Fallback inline styles
            self.setStyleSheet("""
                QDialog { background: linear-gradient(135deg, #0a0e27 0%, #0f1535 100%); }
                QLabel { color: #e8f0ff; font-family: 'Segoe UI', sans-serif; }
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
        title_label = QLabel(title)
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
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Message content with icon
        message_layout = QHBoxLayout()
        message_layout.setSpacing(20)
        
        # Icon
        icon_label = QLabel()
        icon_label.setFixedSize(60, 60)
        
        if icon_type == "warning":
            # Warning icon (yellow)
            icon_label.setStyleSheet("""
                QLabel {
                    background: rgba(234, 179, 8, 0.2);
                    border-radius: 12px;
                    color: #eab308;
                    font-size: 32px;
                    font-weight: bold;
                    qproperty-alignment: AlignCenter;
                }
            """)
            icon_label.setText("⚠")
        elif icon_type == "error":
            # Error icon (red)
            icon_label.setStyleSheet("""
                QLabel {
                    background: rgba(239, 68, 68, 0.2);
                    border-radius: 12px;
                    color: #ef4444;
                    font-size: 32px;
                    font-weight: bold;
                    qproperty-alignment: AlignCenter;
                }
            """)
            icon_label.setText("✕")
        else:
            # Info icon (blue)
            icon_label.setStyleSheet("""
                QLabel {
                    background: rgba(99, 102, 241, 0.2);
                    border-radius: 12px;
                    color: #6366f1;
                    font-size: 32px;
                    font-weight: bold;
                    qproperty-alignment: AlignCenter;
                }
            """)
            icon_label.setText("ℹ")
        
        message_layout.addWidget(icon_label)
        
        # Message text
        message_label = QLabel(message)
        message_label.setFont(QFont('Segoe UI', 12))
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        message_layout.addWidget(message_label)
        
        content_layout.addLayout(message_layout)
        content_layout.addStretch()

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_button = QPushButton('OK')
        ok_button.setMinimumHeight(40)
        ok_button.setMinimumWidth(100)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        content_layout.addLayout(button_layout)
        
        main_layout.addWidget(content_widget)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
