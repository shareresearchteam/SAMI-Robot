# ==============================================================================
# TriviaAnswerPage.py — Trivia answer feedback page for the SAMI UI.
#
# Shows whether the user's answer was correct or wrong, displays the
# correct answer, and provides a "Next Question" button to continue.
# ==============================================================================

# ── PyQt6 imports ─────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,
    QLabel, QDialog,
)
from PyQt6.QtCore import Qt

# ── Project imports ───────────────────────────────────────────────────────────
from components.home_button import HomeButton
from components.action_button import ActionButton
from components.confirm_dialog import ConfirmDialog
from styles.theme import (
    TEXT_PRIMARY, COLOR_CORRECT, COLOR_WRONG,
    FONT_TITLE, FONT_BODY, FONT_LABEL, FONT_HEADING,
)


# ==============================================================================
# Trivia Answer Feedback Page
# ==============================================================================

class TriviaAnswerPage(QWidget):
    """Shows correct/wrong feedback and a Next button."""

    def __init__(self, parent_ui):
        super().__init__()
        self.parent_ui = parent_ui

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 10)
        layout.setSpacing(8)

        layout.addStretch(1)

        # ── Result labels ────────────────────────────────────────────────────
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet(f"font-size: {FONT_TITLE}px; font-weight: bold; color: {TEXT_PRIMARY};")
        layout.addWidget(self.result_label)

        self.correct_label = QLabel()
        self.correct_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.correct_label.setStyleSheet(f"font-size: {FONT_BODY}px; color: {TEXT_PRIMARY};")
        layout.addWidget(self.correct_label)

        self.score_label = QLabel()
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setStyleSheet(f"font-size: {FONT_LABEL}px; font-weight: bold; color: {TEXT_PRIMARY};")
        layout.addWidget(self.score_label)

        layout.addStretch(1)

        # ── Next question button ─────────────────────────────────────────────
        next_btn = ActionButton("Next Question", min_width=400, min_height=120, font_size=FONT_HEADING)
        next_btn.clicked.connect(self._next)
        layout.addWidget(next_btn, alignment=Qt.AlignmentFlag.AlignCenter)

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

    def refresh(self):
        """Update the page with the result of the last answered question."""
        was_correct = self.parent_ui.trivia_last_correct
        q = self.parent_ui.trivia_current_question(offset=-1)
        correct_text = q["correct_answer"] if q else ""

        if was_correct:
            self.result_label.setText("✅  Correct!")
            self.result_label.setStyleSheet(f"font-size: {FONT_TITLE}px; font-weight: bold; color: {COLOR_CORRECT};")
        else:
            self.result_label.setText("❌  Wrong!")
            self.result_label.setStyleSheet(f"font-size: {FONT_TITLE}px; font-weight: bold; color: {COLOR_WRONG};")

        self.correct_label.setText(f"Answer: {correct_text}")
        answered = self.parent_ui.trivia_index
        self.score_label.setText(
            f"Score: {self.parent_ui.trivia_score} / {answered}"
        )

    def _next(self):
        """Advance to the next question or show the final score."""
        if self.parent_ui.trivia_index >= len(self.parent_ui.trivia_questions):
            self.parent_ui.stack.setCurrentWidget(self.parent_ui.trivia_score_page)
            self.parent_ui.trivia_score_page.refresh()
        else:
            self.parent_ui.stack.setCurrentWidget(self.parent_ui.trivia_question_page)
            self.parent_ui.trivia_question_page.load_question()
