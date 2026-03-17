from PyQt6.QtWidgets import QToolButton
from PyQt6.QtGui import QIcon, QPixmap 
from PyQt6.QtCore import Qt, QSize
from styles.theme import (
    BG_HOME_BUTTON, TEXT_HOME, BORDER_HOME,
    RADIUS_LG, FONT_HEADING, BORDER_WIDTH_SM,
)



class HomeButton(QToolButton):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setMinimumSize(400, 150)
        self.setIcon(QIcon(QPixmap("assets/Home.png")))
        self.setIconSize(QSize(100, 100))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        # self.setMinimumSize(400, 400)
        self.setStyleSheet(f"""
            QToolButton {{
                background-color: {BG_HOME_BUTTON};
                color: {TEXT_HOME};
                border: {BORDER_WIDTH_SM}px dashed {BORDER_HOME};
                border-radius: {RADIUS_LG}px;
                font-size: {FONT_HEADING}px;
                font-weight: 600;
                padding: 16px 32px;
                padding-left: 48px;  
            }}
        """)

    @property
    def home_clicked(self):
        return self.clicked