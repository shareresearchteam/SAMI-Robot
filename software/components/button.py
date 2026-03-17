from PyQt6.QtWidgets import QToolButton, QPushButton
from PyQt6.QtGui import QIcon, QPixmap 
from PyQt6.QtCore import Qt, QSize
from styles.theme import (
    TEXT_HOME, BORDER_WIDTH_SM, RADIUS_LG, FONT_HEADING,
)



class Button(QToolButton):
    def __init__(self, text, width, height, color):
        super().__init__()
        self.setText(text)
        self.setMinimumSize(width, height)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setStyleSheet(f"""
            QToolButton {{
                background-color: {color};
                color: {TEXT_HOME};
                border: {BORDER_WIDTH_SM}px solid #000;
                border-radius: {RADIUS_LG}px;
                font-size: {FONT_HEADING}px;
                font-weight: 600;
                padding: 16px 32px;
                padding-left: 48px;  
            }}
        """)
