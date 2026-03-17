# ==============================================================================
# icon_nav_button.py — Large icon-over-text navigation tile component.
# ==============================================================================

from PyQt6.QtWidgets import QToolButton
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from styles.theme import (
    BG_BUTTON, BG_BUTTON_HOVER, TEXT_ON_BUTTON,
    BORDER_COLOR, BORDER_WIDTH, RADIUS_LG, FONT_SUBTITLE,
)


class IconNavButton(QToolButton):
    """
    Large square navigation tile with an icon above a text label.

    Used on HomePage (Exercises / Trivia / Data) and DataPage
    (Sensor Demo / Rating Data).

    Parameters
    ----------
    text : str
        Button label shown below the icon.
    icon_path : str
        Path to the icon file.
    size : int
        Minimum width and height in pixels (default 400).
    icon_size : int
        Icon width and height in pixels (default 170).
    bg : str
        Background colour (default BG_BUTTON).
    bg_hover : str
        Hover background colour (default BG_BUTTON_HOVER).
    font_size : int
        Font size in pixels (default FONT_SUBTITLE).
    """

    def __init__(
        self,
        text: str,
        icon_path: str,
        size: int = 400,
        icon_size: int = 170,
        bg: str = BG_BUTTON,
        bg_hover: str = BG_BUTTON_HOVER,
        font_size: int = FONT_SUBTITLE,
    ):
        super().__init__()
        self.setText(text)
        self.setIcon(QIcon(QPixmap(icon_path)))
        self.setIconSize(QSize(icon_size, icon_size))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setMinimumSize(size, size)
        self.setStyleSheet(f"""
            QToolButton {{
                color: {TEXT_ON_BUTTON};
                font-size: {font_size}px;
                font-weight: bold;
                padding: 20px;
                border-radius: {RADIUS_LG}px;
                background: {bg};
                border: {BORDER_WIDTH}px solid {BORDER_COLOR};
            }}
            QToolButton:hover {{ background: {bg_hover}; }}
        """)
