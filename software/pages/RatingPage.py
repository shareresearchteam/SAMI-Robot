# ==============================================================================
# RatingPage.py — Post-exercise rating page.
#
# Presents a 1–5 rating scale with emoji icons so the user can rate
# the exercise they just completed. Also offers a "Prefer Not To Rate" option.
# ==============================================================================

# ── PyQt6 imports ─────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QToolButton, QButtonGroup,
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

# ── Project imports ───────────────────────────────────────────────────────────
from components.home_button import HomeButton
from components.button import Button
from components.page_title import PageTitle
from styles.theme import BORDER_COLOR, BORDER_WIDTH, RADIUS_LG, FONT_LABEL, BG_HOME_BUTTON


# ==============================================================================
# Rating Page
# ==============================================================================

class RatingPage(QWidget):
    """Post-exercise rating page — 1-to-5 scale with emoji icons."""

    def __init__(self, parent_ui):
        super().__init__()

        self.parent_ui = parent_ui

        layout = QVBoxLayout(self)

        # ── Title ────────────────────────────────────────────────────────────
        layout.addWidget(PageTitle("Rate this Interaction"))
        layout.addStretch(1)

        # ── Rating buttons row ───────────────────────────────────────────────
        row = QHBoxLayout()
        row.setSpacing(40)
        layout.addLayout(row)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        ratings = [
            ("Bad", 1, "#ff4d4d", "assets/ratings/Bad.png"),
            ("Poor", 2, "#ff944d", "assets/ratings/Poor.png"),
            ("Neutral", 3, "#ffe666", "assets/ratings/Neutral.png"),
            ("Good", 4, "#b3ff66", "assets/ratings/Good.png"),
            ("Excellent", 5, "#66ff66", "assets/ratings/Excellent.png"),
        ]

        for label, value, color, icon_path in ratings:
            rating_btn = QToolButton()
            rating_btn.setText(label)
            rating_btn.setCheckable(True)
            rating_btn.setIcon(QIcon(QPixmap(icon_path)))
            rating_btn.setIconSize(QSize(170, 170))
            rating_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            rating_btn.setFixedSize(200, 400)
            rating_btn.setStyleSheet(f"""
                QToolButton {{
                    background-color: {color};
                    border-radius: {RADIUS_LG}px;
                    font-size: {FONT_LABEL}px;
                    font-weight: bold;
                    color: black;
                    border: {BORDER_WIDTH}px solid {BORDER_COLOR};
                    padding-top: 60px;
                    padding-bottom: 40px;
                }}
            """)

            rating_btn.clicked.connect(lambda _, v=value: self.parent_ui.submit_rating(v))

            self.group.addButton(rating_btn)
            row.addWidget(rating_btn)

        # ── "Prefer Not To Rate" option ──────────────────────────────────────
        self.no_rate_btn = Button("Prefer Not To Rate", 300, 80, BG_HOME_BUTTON)
        layout.addWidget(self.no_rate_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.no_rate_btn.clicked.connect(lambda: self.parent_ui.submit_rating("None"))

        layout.addStretch(1)

        # ── Home button ──────────────────────────────────────────────────────
        home_button = HomeButton("Return Home")
        layout.addWidget(home_button)

   
        home_button.clicked.connect(lambda _: self.parent_ui.stack.setCurrentWidget(self.parent_ui.home_page))
        layout.addWidget(home_button)