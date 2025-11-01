"""
Custom Dropdown Widget - Modern, reusable dropdown component
Features: Glassmorphism, smooth animations, custom styling
"""

from PyQt6.QtWidgets import QComboBox, QStyledItemDelegate, QApplication
from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtCore import Qt, QSize


class CustomDropdownDelegate(QStyledItemDelegate):
    """Custom delegate for dropdown items styling"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.item_height = 35
    
    def sizeHint(self, option, index):
        return QSize(option.rect.width(), self.item_height)


class CustomDropdown(QComboBox):
    """
    Modern custom dropdown widget with:
    - Glassmorphism effects
    - Smooth hover transitions
    - Custom styling
    - Draggable support
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drag_position = None
        
        # Set custom delegate for better item styling
        delegate = CustomDropdownDelegate(self)
        self.setItemDelegate(delegate)
        
        # Apply modern stylesheet
        self.apply_modern_style()
        
        # Configure appearance
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Connect signals
        self.currentIndexChanged.connect(self.on_selection_changed)
    
    def apply_modern_style(self):
        """Apply modern glassmorphism styling"""
        self.setStyleSheet("""
            QComboBox {
                background: rgba(26, 31, 58, 0.7);
                border: 2px solid #2d3561;
                border-radius: 12px;
                padding: 10px 14px;
                color: #ffffff;
                font-weight: 500;
                font-size: 13px;
                selection-background-color: #6366f1;
            }
            
            QComboBox:hover {
                border: 2px solid #4f46e5;
                background: rgba(34, 40, 68, 0.85);
            }
            
            QComboBox:focus {
                border: 2px solid #6366f1;
                background: rgba(34, 40, 68, 0.9);
                outline: none;
            }
            
            QComboBox::drop-down {
                border: none;
                background: transparent;
                width: 35px;
                border-radius: 8px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #6366f1;
                margin-right: 12px;
                width: 0px;
                height: 0px;
            }
            
            QComboBox QAbstractItemView {
                background: rgba(26, 31, 58, 0.95);
                border: 2px solid #2d3561;
                border-radius: 12px;
                color: #ffffff;
                selection-background-color: #6366f1;
                selection-color: #ffffff;
                padding: 6px;
                outline: none;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 8px 10px;
                border-radius: 8px;
                margin: 2px 0px;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background: rgba(99, 102, 241, 0.3);
            }
            
            QComboBox QAbstractItemView::item:selected {
                background: #6366f1;
            }
        """)
    
    def add_items_with_icons(self, items_dict):
        """
        Add items with optional icons
        
        Args:
            items_dict: Dictionary with {display_text: data_value}
        """
        for text, value in items_dict.items():
            self.addItem(text, value)
    
    def set_placeholder(self, text):
        """Set placeholder text"""
        self.insertItem(0, text)
        self.setCurrentIndex(0)
    
    def get_selected_value(self):
        """Get the data value of selected item"""
        return self.currentData()
    
    def get_selected_text(self):
        """Get the text of selected item"""
        return self.currentText()
    
    def on_selection_changed(self, index):
        """Handle selection change"""
        # Can be overridden in subclasses for custom behavior
        pass
    
    def set_custom_colors(self, bg_color, border_color, text_color, hover_color):
        """
        Customize colors dynamically
        
        Args:
            bg_color: Background color (e.g., '#1a1f3a')
            border_color: Border color (e.g., '#2d3561')
            text_color: Text color (e.g., '#ffffff')
            hover_color: Hover color (e.g., '#4f46e5')
        """
        self.setStyleSheet(f"""
            QComboBox {{
                background: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 10px 14px;
                color: {text_color};
                font-weight: 500;
                font-size: 13px;
                selection-background-color: {hover_color};
            }}
            
            QComboBox:hover {{
                border: 2px solid {hover_color};
                background: rgba(34, 40, 68, 0.85);
            }}
            
            QComboBox:focus {{
                border: 2px solid {hover_color};
                background: rgba(34, 40, 68, 0.9);
                outline: none;
            }}
            
            QComboBox::drop-down {{
                border: none;
                background: transparent;
                width: 35px;
                border-radius: 8px;
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid {hover_color};
                margin-right: 12px;
                width: 0px;
                height: 0px;
            }}
            
            QComboBox QAbstractItemView {{
                background: rgba(26, 31, 58, 0.95);
                border: 2px solid {border_color};
                border-radius: 12px;
                color: {text_color};
                selection-background-color: {hover_color};
                selection-color: {text_color};
                padding: 6px;
                outline: none;
            }}
            
            QComboBox QAbstractItemView::item {{
                padding: 8px 10px;
                border-radius: 8px;
                margin: 2px 0px;
            }}
            
            QComboBox QAbstractItemView::item:hover {{
                background: rgba(99, 102, 241, 0.3);
            }}
            
            QComboBox QAbstractItemView::item:selected {{
                background: {hover_color};
            }}
        """)


class CustomDropdownCompact(CustomDropdown):
    """Compact version of custom dropdown with smaller height"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(32)
        
        # Update delegate for compact size
        delegate = CustomDropdownDelegate(self)
        delegate.item_height = 28
        self.setItemDelegate(delegate)


class CustomDropdownLarge(CustomDropdown):
    """Large version of custom dropdown with bigger height"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(48)
        
        # Update delegate for larger size
        delegate = CustomDropdownDelegate(self)
        delegate.item_height = 42
        self.setItemDelegate(delegate)
