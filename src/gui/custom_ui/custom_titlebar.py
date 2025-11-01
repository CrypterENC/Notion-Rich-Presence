"""
Custom Title Bar Widget - Modern, reusable title bar with control buttons
Features: Frameless window support, minimize/close buttons, draggable, icon support
"""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt


class CustomTitleBar(QFrame):
    """
    Modern custom title bar with:
    - Window icon
    - Title text
    - Minimize button
    - Close button
    - Draggable support
    - Modern styling
    """
    
    def __init__(self, parent=None, title="Application", icon_path=None, show_minimize=True, show_close=True):
        super().__init__(parent)
        self.parent_window = parent
        self.drag_position = None
        
        # Configure frame
        self.setObjectName("titleBar")
        self.setFixedHeight(40)
        self.setStyleSheet("""
            #titleBar {
                background: rgba(10, 14, 39, 0.95);
                border-bottom: 1px solid rgba(99, 102, 241, 0.2);
            }
        """)
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(8)
        
        # Window icon
        if icon_path:
            icon_label = QLabel()
            icon_label.setObjectName("titleIcon")
            try:
                icon_pixmap = QIcon(icon_path).pixmap(24, 24)
                icon_label.setPixmap(icon_pixmap)
                icon_label.setFixedSize(24, 24)
                layout.addWidget(icon_label)
            except:
                pass
        
        # Title label
        title_label = QLabel(title)
        title_label.setObjectName("titleLabel")
        title_label.setStyleSheet("font-weight: 600; font-size: 13px; color: #e8f0ff; margin-left: 8px;")
        layout.addWidget(title_label)
        layout.addStretch()
        
        # Minimize button
        if show_minimize:
            self.minimize_btn = QPushButton('−')
            self.minimize_btn.setObjectName("minimizeBtn")
            self.minimize_btn.setFixedSize(32, 32)
            self.minimize_btn.setStyleSheet("""
                QPushButton#minimizeBtn {
                    background: transparent;
                    border: none;
                    color: #e8f0ff;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 0px;
                }
                QPushButton#minimizeBtn:hover {
                    background: rgba(99, 102, 241, 0.2);
                    border-radius: 6px;
                }
                QPushButton#minimizeBtn:pressed {
                    background: rgba(99, 102, 241, 0.4);
                }
            """)
            if parent:
                self.minimize_btn.clicked.connect(parent.showMinimized)
            layout.addWidget(self.minimize_btn)
        
        # Close button
        if show_close:
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
            if parent:
                self.close_btn.clicked.connect(parent.close)
            layout.addWidget(self.close_btn)
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.MouseButton.LeftButton and self.parent_window:
            self.drag_position = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position is not None and self.parent_window:
            self.parent_window.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def set_title(self, title):
        """Update title text"""
        # Find and update title label
        for widget in self.findChildren(QLabel):
            if widget.objectName() == "titleLabel":
                widget.setText(title)
                break
    
    def set_icon(self, icon_path):
        """Update window icon"""
        try:
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleIcon":
                    icon_pixmap = QIcon(icon_path).pixmap(24, 24)
                    widget.setPixmap(icon_pixmap)
                    break
        except:
            pass
    
    def hide_minimize_button(self):
        """Hide minimize button"""
        if hasattr(self, 'minimize_btn'):
            self.minimize_btn.hide()
    
    def hide_close_button(self):
        """Hide close button"""
        if hasattr(self, 'close_btn'):
            self.close_btn.hide()
    
    def show_minimize_button(self):
        """Show minimize button"""
        if hasattr(self, 'minimize_btn'):
            self.minimize_btn.show()
    
    def show_close_button(self):
        """Show close button"""
        if hasattr(self, 'close_btn'):
            self.close_btn.show()
