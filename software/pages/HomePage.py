# ==============================================================================
# HomePage.py — Main landing page for the SAMI UI.
#
# Presents interaction buttons (Exercises, Trivia, Data) that navigate
# to their respective pages via the parent's QStackedWidget.
# ==============================================================================

# ── PyQt6 imports ─────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout,
    QPushButton,
)
from PyQt6.QtCore import Qt

# ── Project imports ───────────────────────────────────────────────────────────
from components.page_title import PageTitle
from components.icon_nav_button import IconNavButton
from styles.theme import TEXT_SECONDARY, RADIUS_SM, FONT_CAPTION


# ==============================================================================
# Home Page
# ==============================================================================

class HomePage(QWidget):
    """Main landing page — presents interaction buttons."""

    def __init__(self, parent_ui):
        super().__init__()

        self.parent_ui = parent_ui

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 10)
        layout.setSpacing(8)

        # ── Title ────────────────────────────────────────────────────────────
        layout.addWidget(PageTitle("Select an Interaction"))
        layout.addStretch(1)

        # ── Interaction grid ─────────────────────────────────────────────────
        grid = QGridLayout()
        grid.setHorizontalSpacing(40)
        grid.setVerticalSpacing(40)

        interactions = [
            ("Exercises", "assets/interactions/Exercises.png"),
            ("Trivia", "assets/interactions/Trivia.png"),
            ("Data", "assets/interactions/Data.svg")
        ]

        for col, (name, icon_path) in enumerate(interactions):
            interaction_btn = IconNavButton(name, icon_path)

            if name == "Exercises":
                interaction_btn.clicked.connect(
                    lambda: (
                        self.parent_ui.move_to_home(),  # first move robot home
                        self.parent_ui.stack.setCurrentWidget(self.parent_ui.exercise_page)  # then go to exercise page
                    )
                )
            elif name == "Data":
                interaction_btn.clicked.connect(
                    lambda: self.parent_ui.stack.setCurrentWidget(self.parent_ui.data_page)
                )
            elif name == "Trivia":
                interaction_btn.clicked.connect(
                    lambda: self.parent_ui.stack.setCurrentWidget(self.parent_ui.trivia_page)
                )
            else:
                interaction_btn.clicked.connect(
                    lambda _, n=name: print(f"{n} clicked")
                )

            grid.addWidget(interaction_btn, 0, col)

        layout.addLayout(grid)
        layout.addStretch(1)

        # ── Dev page shortcut (remove before production) ─────────────────────
        dev_btn = QPushButton("🛠  Component Dev Page")
        dev_btn.setMinimumSize(350, 60)
        dev_btn.setStyleSheet(f"""
            QPushButton {{
                font-size: {FONT_CAPTION}px; font-weight: bold; color: {TEXT_SECONDARY};
                border-radius: {RADIUS_SM}px; background: #ddd; border: 2px dashed #999;
            }}
            QPushButton:hover {{ background: #ccc; }}
        """)
        dev_btn.clicked.connect(
            lambda: self.parent_ui.stack.setCurrentWidget(self.parent_ui.dev_page)
        )
        layout.addWidget(dev_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # home_robot_btn = QPushButton("Home", self)
        # home_robot_btn.clicked.connect(self.parent_ui.move_to_home)
        # layout.addWidget(home_robot_btn)
