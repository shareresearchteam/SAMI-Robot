# ==============================================================================
# action_button.py — Reusable pink action button component.
# ==============================================================================

from PyQt6.QtWidgets import QPushButton
from styles.theme import (
    BG_BUTTON, BG_BUTTON_HOVER, TEXT_ON_BUTTON,
    BORDER_COLOR, BORDER_WIDTH, RADIUS_LG, FONT_LABEL,
)


class ActionButton(QPushButton):
    """
    Styled QPushButton with the app's signature pink theme.

    Parameters
    ----------
    text : str
        Button label.
    min_width : int
        Minimum width in pixels (default 400).
    min_height : int
        Minimum height in pixels (default 120).
    font_size : int
        Font size in pixels (default FONT_LABEL).
    bg : str
        Background colour (default BG_BUTTON).
    bg_hover : str
        Hover background colour (default BG_BUTTON_HOVER).
    text_align : str
        CSS text-align value (default "center").
    """

    def __init__(
        self,
        text: str,
        min_width: int = 400,
        min_height: int = 120,
        font_size: int = FONT_LABEL,
        bg: str = BG_BUTTON,
        bg_hover: str = BG_BUTTON_HOVER,
        text_align: str = "center",
    ):
        super().__init__(text)
        self.setMinimumSize(min_width, min_height)
        self.setStyleSheet(f"""
            QPushButton {{
                font-size: {font_size}px;
                font-weight: bold;
                color: {TEXT_ON_BUTTON};
                border-radius: {RADIUS_LG}px;
                background: {bg};
                border: {BORDER_WIDTH}px solid {BORDER_COLOR};
                text-align: {text_align};
                padding-left: 24px;
                padding-right: 24px;
            }}
            QPushButton:hover {{ background: {bg_hover}; }}
        """)
