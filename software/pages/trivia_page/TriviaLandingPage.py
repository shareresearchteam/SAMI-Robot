# ==============================================================================
# TriviaLandingPage.py — Trivia landing page for the SAMI UI.
#
# Lets the user choose 5 or 10 questions, then starts the trivia game.
# ==============================================================================

# ── PyQt6 imports ─────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,
)
from PyQt6.QtCore import Qt

# ── Project imports ───────────────────────────────────────────────────────────
from components.home_button import HomeButton
from components.page_title import PageTitle
from styles.theme import (
    BG_BUTTON, BG_BUTTON_HOVER, BG_SELECTED, BG_DISABLED,
    TEXT_PRIMARY, TEXT_ON_BUTTON, TEXT_DISABLED,
    BORDER_COLOR, BORDER_DISABLED, BORDER_WIDTH,
    RADIUS_LG, FONT_SUBTITLE, FONT_HEADING,
)


# ==============================================================================
# Trivia Landing Page
# ==============================================================================

class TriviaLandingPage(QWidget):
    """Landing page — choose 5 or 10 questions, then start."""

    def __init__(self, parent_ui):
        super().__init__()
        self.parent_ui = parent_ui
        self._selected_count = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 10)
        layout.setSpacing(8)

        # ── Title ────────────────────────────────────────────────────────────
        layout.addWidget(PageTitle("Trivia"))
        layout.addStretch(1)

        # ── Question count prompt ────────────────────────────────────────────
        choose_label = QLabel("How many questions?")
        choose_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        choose_label.setStyleSheet(f"font-size: {FONT_HEADING}px; font-weight: bold; color: {TEXT_PRIMARY};")
        layout.addWidget(choose_label)

        layout.addSpacing(16)

        # ── 5 / 10 selector row ─────────────────────────────────────────────
        BTN_STYLE = f"""
            QPushButton {{{{
                font-size: {FONT_SUBTITLE}px;
                font-weight: bold;
                color: {TEXT_ON_BUTTON};
                border-radius: {RADIUS_LG}px;
                background: {{bg}};
                border: {{border}};
            }}}}
            QPushButton:hover {{{{ background: {BG_BUTTON_HOVER}; }}}}
        """
        NORMAL_BG       = BG_BUTTON
        SELECTED_BG_VAL = BG_SELECTED
        NORMAL_BORDER   = f"{BORDER_WIDTH}px solid {BORDER_COLOR}"
        SELECTED_BORDER = "5px solid #000"

        count_row = QHBoxLayout()
        count_row.setSpacing(40)
        count_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._btn5  = QPushButton("5 Questions")
        self._btn10 = QPushButton("10 Questions")

        for btn in (self._btn5, self._btn10):
            btn.setMinimumSize(360, 140)
            btn.setStyleSheet(BTN_STYLE.format(bg=NORMAL_BG, border=NORMAL_BORDER))
            count_row.addWidget(btn)

        def select_count(count):
            self._selected_count = count
            if count == 5:
                self._btn5.setStyleSheet(BTN_STYLE.format(bg=SELECTED_BG_VAL, border=SELECTED_BORDER))
                self._btn10.setStyleSheet(BTN_STYLE.format(bg=NORMAL_BG, border=NORMAL_BORDER))
            else:
                self._btn10.setStyleSheet(BTN_STYLE.format(bg=SELECTED_BG_VAL, border=SELECTED_BORDER))
                self._btn5.setStyleSheet(BTN_STYLE.format(bg=NORMAL_BG, border=NORMAL_BORDER))
            self._start_btn.setEnabled(True)
            self._start_btn.setStyleSheet(BTN_STYLE.format(bg=NORMAL_BG, border=NORMAL_BORDER))

        self._btn5.clicked.connect(lambda: select_count(5))
        self._btn10.clicked.connect(lambda: select_count(10))

        layout.addLayout(count_row)
        layout.addSpacing(32)

        # ── Start button (disabled until a count is chosen) ──────────────────
        self._start_btn = QPushButton("Start Trivia")
        self._start_btn.setMinimumSize(400, 140)
        self._start_btn.setEnabled(False)
        self._start_btn.setStyleSheet(f"""
            QPushButton {{
                font-size: {FONT_SUBTITLE}px;
                font-weight: bold;
                color: {TEXT_DISABLED};
                border-radius: {RADIUS_LG}px;
                background: {BG_DISABLED};
                border: {BORDER_WIDTH}px solid {BORDER_DISABLED};
            }}
        """)
        self._start_btn.clicked.connect(self._start_trivia)
        layout.addWidget(self._start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch(1)

        # ── Home button ──────────────────────────────────────────────────────
        home_button = HomeButton("Return Home")
        home_button.clicked.connect(
            lambda _: self.parent_ui.stack.setCurrentWidget(self.parent_ui.home_page)
        )
        layout.addWidget(home_button)

    # ── Events ───────────────────────────────────────────────────────────────
    def showEvent(self, event):
        """Reset selection every time the page is shown."""
        super().showEvent(event)
        self._selected_count = None
        BTN_STYLE = f"""
            QPushButton {{{{
                font-size: {FONT_SUBTITLE}px; font-weight: bold; color: {TEXT_ON_BUTTON};
                border-radius: {RADIUS_LG}px; background: {BG_BUTTON}; border: {BORDER_WIDTH}px solid {BORDER_COLOR};
            }}}}
            QPushButton:hover {{{{ background: {BG_BUTTON_HOVER}; }}}}
        """
        self._btn5.setStyleSheet(BTN_STYLE.format())
        self._btn10.setStyleSheet(BTN_STYLE.format())
        self._start_btn.setEnabled(False)
        self._start_btn.setStyleSheet(f"""
            QPushButton {{
                font-size: {FONT_SUBTITLE}px; font-weight: bold; color: {TEXT_DISABLED};
                border-radius: {RADIUS_LG}px; background: {BG_DISABLED}; border: {BORDER_WIDTH}px solid {BORDER_DISABLED};
            }}
        """)

    def _start_trivia(self):
        """Load questions and navigate to the first question page."""
        self.parent_ui.trivia_load_questions(limit=self._selected_count)
        self.parent_ui.stack.setCurrentWidget(self.parent_ui.trivia_question_page)
        self.parent_ui.trivia_question_page.load_question()
