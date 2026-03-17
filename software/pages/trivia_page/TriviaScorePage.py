# ==============================================================================
# TriviaScorePage.py — Trivia final score page for the SAMI UI.
#
# Displays the user's final score with a congratulatory message and
# offers "Play Again" and "Go Home" options.
# ==============================================================================

# ── PyQt6 imports ─────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt

# ── Project imports ───────────────────────────────────────────────────────────
from components.action_button import ActionButton
from styles.theme import TEXT_PRIMARY, FONT_TITLE, FONT_BODY, FONT_HEADING


# ==============================================================================
# Trivia Score Page
# ==============================================================================

class TriviaScorePage(QWidget):
    """Final score screen with Play Again and Go Home options."""

    def __init__(self, parent_ui):
        super().__init__()
        self.parent_ui = parent_ui

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 10)
        layout.setSpacing(8)

        layout.addStretch(2)

        # ── Trophy and score labels ──────────────────────────────────────────
        trophy = QLabel("🏆")
        trophy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trophy.setStyleSheet("font-size: 100px;")
        layout.addWidget(trophy)

        self.score_label = QLabel()
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setStyleSheet(f"font-size: {FONT_TITLE}px; font-weight: bold; color: {TEXT_PRIMARY};")
        layout.addWidget(self.score_label)

        self.msg_label = QLabel()
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_label.setStyleSheet(f"font-size: {FONT_BODY}px; color: {TEXT_PRIMARY};")
        layout.addWidget(self.msg_label)

        layout.addStretch(1)

        # ── Play Again / Go Home buttons ─────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(40)

        play_again_btn = ActionButton("Play Again", min_width=360, min_height=120, font_size=FONT_HEADING)
        play_again_btn.clicked.connect(self._play_again)
        btn_row.addWidget(play_again_btn)

        home_btn = ActionButton("Rate & Finish", min_width=360, min_height=120, font_size=FONT_HEADING)
        home_btn.clicked.connect(self._rate_and_finish)
        btn_row.addWidget(home_btn)

        layout.addLayout(btn_row)
        layout.addStretch(2)

    def refresh(self):
        """Compute and display the final score with a congratulatory message."""
        total = len(self.parent_ui.trivia_questions)
        score = self.parent_ui.trivia_score
        self.score_label.setText(f"Final Score:  {score} / {total}")
        pct = int(score / total * 100) if total else 0
        if pct == 100:
            msg = "Perfect score! Amazing! 🎉"
        elif pct >= 70:
            msg = "Great job! Keep it up! 👍"
        elif pct >= 40:
            msg = "Good effort! Want to try again?"
        else:
            msg = "Better luck next time! 💪"
        self.msg_label.setText(msg)

        # ── Persist the score to trivia_scores.txt ───────────────────────
        self.parent_ui.trivia_save_score()

    def _play_again(self):
        """Reload questions and restart the trivia game."""
        self.parent_ui.trivia_load_questions(limit=self.parent_ui.trivia_index)
        self.parent_ui.stack.setCurrentWidget(self.parent_ui.trivia_question_page)
        self.parent_ui.trivia_question_page.load_question()

    def _rate_and_finish(self):
        """Navigate to the rating page so the user can rate the trivia round."""
        self.parent_ui.selected_exercise = "Trivia"
        self.parent_ui.stack.setCurrentWidget(self.parent_ui.rating_page)
