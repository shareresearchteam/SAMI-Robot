# ==============================================================================
# page_title.py — Reusable page title label component.
# ==============================================================================

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from styles.theme import TEXT_PRIMARY, FONT_TITLE


class PageTitle(QLabel):
    """
    Centered, bold page title used at the top of every page.
    Default style: FONT_TITLE px, bold, TEXT_PRIMARY colour.
    """

    def __init__(self, text: str, font_size: int = FONT_TITLE):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            f"font-size: {font_size}px; font-weight: bold; color: {TEXT_PRIMARY};"
        )
