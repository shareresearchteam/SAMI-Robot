# ==============================================================================
# DevPage.py — Component showcase / development testing page.
#
# Displays every reusable component from the components/ package so you
# can visually verify styling, sizing, and click behaviour before rolling
# them out across the real pages.
# ==============================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QScrollArea,
)
from PyQt6.QtCore import Qt

# ── Project imports (every component) ─────────────────────────────────────────
from components.page_title import PageTitle
from components.action_button import ActionButton
from components.icon_nav_button import IconNavButton
from components.confirm_dialog import ConfirmDialog
from components.back_home_nav import BackHomeNav
from components.home_button import HomeButton
from components.button import Button
from styles.theme import BG_BUTTON, BG_HOME_BUTTON, TEXT_SECONDARY, FONT_BUTTON


# ==============================================================================
# Dev Page
# ==============================================================================

class DevPage(QWidget):
    """
    Component showcase page.
    Scroll through labelled sections, each demonstrating one component.
    """

    def __init__(self, parent_ui):
        super().__init__()
        self.parent_ui = parent_ui

        # ── Outer layout with scroll area ────────────────────────────────────
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        outer.addWidget(scroll)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(24)
        scroll.setWidget(container)

        # ==================================================================
        # 1. PageTitle
        # ==================================================================
        layout.addWidget(self._section_header("1 · PageTitle"))

        layout.addWidget(PageTitle("Default PageTitle (64 px)"))
        layout.addWidget(PageTitle("Smaller PageTitle (36 px)", font_size=36))

        # ==================================================================
        # 2. ActionButton
        # ==================================================================
        layout.addWidget(self._section_header("2 · ActionButton"))

        row2 = QHBoxLayout()
        row2.setSpacing(20)

        btn_default = ActionButton("Default (400×120)")
        btn_default.clicked.connect(lambda: print("[DevPage] ActionButton default clicked"))
        row2.addWidget(btn_default)

        btn_small = ActionButton("Small (200×80, 24px)", min_width=200, min_height=80, font_size=24)
        btn_small.clicked.connect(lambda: print("[DevPage] ActionButton small clicked"))
        row2.addWidget(btn_small)

        btn_left = ActionButton("Left-aligned text", text_align="left")
        btn_left.clicked.connect(lambda: print("[DevPage] ActionButton left-align clicked"))
        row2.addWidget(btn_left)

        layout.addLayout(row2)

        # custom colours
        row2b = QHBoxLayout()
        row2b.setSpacing(20)

        btn_green = ActionButton("Custom green", bg="#b3ff66", bg_hover="#99e64d")
        row2b.addWidget(btn_green)

        btn_red = ActionButton("Custom red", bg="#ff6666", bg_hover="#ff3333")
        row2b.addWidget(btn_red)

        layout.addLayout(row2b)

        # ==================================================================
        # 3. IconNavButton
        # ==================================================================
        layout.addWidget(self._section_header("3 · IconNavButton"))

        row3 = QHBoxLayout()
        row3.setSpacing(40)

        nav_exercises = IconNavButton("Exercises", "assets/interactions/Exercises.png")
        nav_exercises.clicked.connect(lambda: print("[DevPage] IconNavButton 'Exercises' clicked"))
        row3.addWidget(nav_exercises)

        nav_trivia = IconNavButton("Trivia", "assets/interactions/Trivia.png")
        nav_trivia.clicked.connect(lambda: print("[DevPage] IconNavButton 'Trivia' clicked"))
        row3.addWidget(nav_trivia)

        nav_data = IconNavButton("Data", "assets/interactions/Data.svg")
        nav_data.clicked.connect(lambda: print("[DevPage] IconNavButton 'Data' clicked"))
        row3.addWidget(nav_data)

        layout.addLayout(row3)

        # smaller variant
        row3b = QHBoxLayout()
        row3b.setSpacing(20)

        nav_small = IconNavButton("Small tile", "assets/interactions/Sensor.svg", size=250, icon_size=100, font_size=28)
        nav_small.clicked.connect(lambda: print("[DevPage] small IconNavButton clicked"))
        row3b.addWidget(nav_small)

        nav_custom = IconNavButton("Custom colour", "assets/interactions/Rating.png", bg="#b3ff66", bg_hover="#99e64d")
        nav_custom.clicked.connect(lambda: print("[DevPage] custom-colour IconNavButton clicked"))
        row3b.addWidget(nav_custom)

        row3b.addStretch()
        layout.addLayout(row3b)

        # ==================================================================
        # 4. ConfirmDialog
        # ==================================================================
        layout.addWidget(self._section_header("4 · ConfirmDialog"))

        row4 = QHBoxLayout()
        row4.setSpacing(20)

        btn_dialog_default = ActionButton("Open default ConfirmDialog", min_width=450, min_height=80, font_size=24)
        btn_dialog_default.clicked.connect(self._show_default_dialog)
        row4.addWidget(btn_dialog_default)

        btn_dialog_custom = ActionButton("Open custom ConfirmDialog", min_width=450, min_height=80, font_size=24)
        btn_dialog_custom.clicked.connect(self._show_custom_dialog)
        row4.addWidget(btn_dialog_custom)

        row4.addStretch()
        layout.addLayout(row4)

        # ==================================================================
        # 5. HomeButton (existing)
        # ==================================================================
        layout.addWidget(self._section_header("5 · HomeButton (existing)"))

        row5 = QHBoxLayout()
        row5.setSpacing(20)

        hb = HomeButton("Return Home")
        hb.clicked.connect(lambda _: print("[DevPage] HomeButton clicked"))
        row5.addWidget(hb)

        hb2 = HomeButton("← Back")
        hb2.clicked.connect(lambda _: print("[DevPage] Back HomeButton clicked"))
        row5.addWidget(hb2)

        layout.addLayout(row5)

        # ==================================================================
        # 6. Button (existing generic)
        # ==================================================================
        layout.addWidget(self._section_header("6 · Button (existing generic)"))

        row6 = QHBoxLayout()
        row6.setSpacing(20)

        gb1 = Button("Prefer Not To Rate", 300, 80, BG_HOME_BUTTON)
        gb1.clicked.connect(lambda: print("[DevPage] Button BG_HOME_BUTTON clicked"))
        row6.addWidget(gb1)

        gb2 = Button("Another Button", 300, 80, BG_BUTTON)
        gb2.clicked.connect(lambda: print("[DevPage] Button BG_BUTTON clicked"))
        row6.addWidget(gb2)

        row6.addStretch()
        layout.addLayout(row6)

        # ==================================================================
        # 7. BackHomeNav
        # ==================================================================
        layout.addWidget(self._section_header("7 · BackHomeNav"))

        # We pass parent_ui.home_page as the "back" page just for demo purposes.
        # In real usage you'd pass the actual parent page, e.g. parent_ui.data_page.
        nav = BackHomeNav(parent_ui, back_page=parent_ui.home_page)
        layout.addLayout(nav.layout)

        # ==================================================================
        # Bottom spacer + Return Home
        # ==================================================================
        layout.addStretch(1)

        home_button = HomeButton("Return Home")
        home_button.clicked.connect(
            lambda _: self.parent_ui.stack.setCurrentWidget(self.parent_ui.home_page)
        )
        layout.addWidget(home_button)

    # ── Helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _section_header(text: str) -> QLabel:
        """Create a styled section header label."""
        lbl = QLabel(text)
        lbl.setStyleSheet(
            f"font-size: {FONT_BUTTON}px; font-weight: bold; color: {TEXT_SECONDARY};"
            "border-bottom: 2px solid #999; padding-bottom: 6px;"
            "margin-top: 16px;"
        )
        return lbl

    def _show_default_dialog(self):
        """Open a ConfirmDialog with default settings."""
        dlg = ConfirmDialog(parent=self)
        result = dlg.exec()
        print(f"[DevPage] Default ConfirmDialog result: {'Accepted' if result else 'Rejected'}")

    def _show_custom_dialog(self):
        """Open a ConfirmDialog with custom message and button labels."""
        dlg = ConfirmDialog(
            message="🗑️  This will delete all ratings.\nAre you sure?",
            confirm_text="Yes, Delete",
            cancel_text="Keep Ratings",
            parent=self,
        )
        result = dlg.exec()
        print(f"[DevPage] Custom ConfirmDialog result: {'Accepted' if result else 'Rejected'}")
