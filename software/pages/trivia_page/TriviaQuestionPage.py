# ==============================================================================
# TriviaQuestionPage.py — Trivia question page for the SAMI UI.
#
# Displays the current question with four answer buttons in a 2×2 grid.
# Includes a progress counter, score tracker, and a confirmation dialog
# when the user tries to leave mid-game.
# ==============================================================================

# ── PyQt6 imports ─────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QDialog,
)
from PyQt6.QtCore import Qt

# ── Project imports ───────────────────────────────────────────────────────────
from components.home_button import HomeButton
from components.action_button import ActionButton
from components.confirm_dialog import ConfirmDialog
from styles.theme import (
    TEXT_PRIMARY, BG_CARD, BORDER_COLOR, BORDER_WIDTH,
    RADIUS_MD, FONT_LABEL, FONT_BODY, FONT_BUTTON,
)


# ==============================================================================
# Trivia Question Page
# ==============================================================================

class TriviaQuestionPage(QWidget):
    """Shows the current question and four answer buttons."""

    def __init__(self, parent_ui):
        super().__init__()
        self.parent_ui = parent_ui

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 10)
        layout.setSpacing(8)

        # ── Counter + score row ──────────────────────────────────────────────
        info_row = QHBoxLayout()
        self.counter_label = QLabel("Question 1 / ?")
        self.counter_label.setStyleSheet(f"font-size: {FONT_LABEL}px; font-weight: bold; color: {TEXT_PRIMARY};")
        self.score_label = QLabel("Score: 0 / 0")
        self.score_label.setStyleSheet(f"font-size: {FONT_LABEL}px; font-weight: bold; color: {TEXT_PRIMARY};")
        info_row.addWidget(self.counter_label)
        info_row.addStretch()
        info_row.addWidget(self.score_label)
        layout.addLayout(info_row)

        # ── Question text ────────────────────────────────────────────────────
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setStyleSheet(f"""
            font-size: {FONT_BODY}px;
            font-weight: bold;
            color: {TEXT_PRIMARY};
            background: {BG_CARD};
            border-radius: {RADIUS_MD}px;
            border: {BORDER_WIDTH}px solid {BORDER_COLOR};
            padding: 24px 32px;
        """)
        layout.addWidget(self.question_label)
        layout.addStretch(1)

        # ── Answer buttons grid ──────────────────────────────────────────────
        self.answers_grid = QGridLayout()
        self.answers_grid.setSpacing(24)
        layout.addLayout(self.answers_grid)
        self.answer_buttons = []

        layout.addStretch(1)

        # ── Home button ──────────────────────────────────────────────────────
        home_button = HomeButton("Return Home")
        home_button.clicked.connect(self._confirm_go_home)
        layout.addWidget(home_button)

    # ── Navigation ───────────────────────────────────────────────────────────
    def _confirm_go_home(self, *_):
        """Show a confirmation dialog before abandoning the trivia game."""
        dlg = ConfirmDialog(
            message="⚠️  Your trivia progress will be lost.\nAre you sure you want to go home?",
            parent=self,
        )
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.parent_ui.stack.setCurrentWidget(self.parent_ui.home_page)

    def load_question(self):
        """Populate the page with the current question and answer choices."""
        q = self.parent_ui.trivia_current_question()
        if not q:
            return

        total   = len(self.parent_ui.trivia_questions)
        current = self.parent_ui.trivia_index + 1
        score   = self.parent_ui.trivia_score

        self.counter_label.setText(f"Question {current} / {total}")
        self.score_label.setText(f"Score: {score} / {self.parent_ui.trivia_index}")
        self.question_label.setText(q["question"])

        # Rebuild answer buttons
        for btn in self.answer_buttons:
            self.answers_grid.removeWidget(btn)
            btn.deleteLater()
        self.answer_buttons = []

        options = [("A", q["option_a"]), ("B", q["option_b"]),
                   ("C", q["option_c"]), ("D", q["option_d"])]

        for i, (letter, text) in enumerate(options):
            row, col = divmod(i, 2)
            btn = ActionButton(
                f"{letter}.  {text}",
                min_width=600, min_height=130, font_size=FONT_BUTTON, text_align="left",
            )
            btn.clicked.connect(lambda _, l=letter: self._submit(l))
            self.answers_grid.addWidget(btn, row, col)
            self.answer_buttons.append(btn)

    def _submit(self, letter):
        """Submit the chosen answer and navigate to the feedback page."""
        self.parent_ui.trivia_submit_answer(letter)
        self.parent_ui.stack.setCurrentWidget(self.parent_ui.trivia_answer_page)
        self.parent_ui.trivia_answer_page.refresh()
