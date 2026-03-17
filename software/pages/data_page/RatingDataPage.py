# ==============================================================================
# RatingDataPage.py — Exercise rating history viewer.
#
# Displays per-exercise average summary cards and a full scrollable ratings
# table. Reloads from disk every time the page is shown.
# ==============================================================================

import os

# ── PyQt6 imports ─────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt

# ── Project imports ───────────────────────────────────────────────────────────
from components.page_title import PageTitle
from components.back_home_nav import BackHomeNav
from styles.theme import (
    BG_CARD, BG_BUTTON, TEXT_ON_BUTTON, TEXT_PRIMARY,
    BORDER_COLOR, BORDER_DISABLED, BORDER_WIDTH_SM,
    RADIUS_SM, FONT_TABLE, FONT_CAPTION,
)


# ==============================================================================
# Rating Data Page
# ==============================================================================

class RatingDataPage(QWidget):
    """
    Displays exercise rating history.
    Shows per-exercise average summary cards and a full scrollable ratings table.
    Reloads from disk every time the page is shown.
    """

    def __init__(self, parent_ui):
        super().__init__()

        self.parent_ui  = parent_ui
        self.rating_file = "data/interaction_ratings.txt"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(16)

        # ── Page title ───────────────────────────────────────────────────────
        layout.addWidget(PageTitle("Rating Data"))

        # ── Section heading ──────────────────────────────────────────────────
        layout.addWidget(PageTitle("Exercise Ratings", font_size=36))

        # ── Per-exercise average summary cards (populated dynamically) ───────
        self.summary_layout = QHBoxLayout()
        self.summary_layout.setSpacing(20)
        layout.addLayout(self.summary_layout)

        # ── Full ratings table ───────────────────────────────────────────────
        from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Interaction", "Rating", "Trivia Score"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                color: {TEXT_ON_BUTTON};
                font-size: {FONT_TABLE}px;
                background: {BG_CARD};
                border-radius: {RADIUS_SM}px;
                border: {BORDER_WIDTH_SM}px solid {BORDER_DISABLED};
            }}
            QHeaderView::section {{
                color: {TEXT_ON_BUTTON};
                font-size: {FONT_CAPTION}px;
                font-weight: bold;
                background: {BG_BUTTON};
                border: 1px solid {BORDER_DISABLED};
                padding: 6px;
            }}
        """)
        self.table.setMinimumHeight(400)
        layout.addWidget(self.table)

        # ── Back and Home buttons ────────────────────────────────────────────
        nav = BackHomeNav(parent_ui, back_page=parent_ui.data_page)
        layout.addLayout(nav.layout)

    def showEvent(self, event):
        """Reload ratings from disk every time this page becomes visible."""
        super().showEvent(event)
        self._load_ratings()

    def _load_ratings(self):
        """
        Parse exercise_ratings.txt, fill the table, and rebuild summary cards.
        Each line is expected to be:
            timestamp | interaction | rating | trivia_score (optional)
        Older 3-column lines are handled gracefully.
        """
        from PyQt6.QtWidgets import QTableWidgetItem
        from collections import defaultdict

        # ── Parse the ratings file ────────────────────────────────────────────
        rows = []
        if os.path.exists(self.rating_file):
            with open(self.rating_file, "r") as f:
                for line in f:
                    parts = [p.strip() for p in line.strip().split("|")]
                    if len(parts) >= 3:
                        ts       = parts[0]
                        exercise = parts[1]
                        rating   = parts[2]
                        trivia   = parts[3] if len(parts) >= 4 else ""
                        rows.append((ts, exercise, rating, trivia))

        # ── Populate the table, most-recent entry first ──────────────────────
        self.table.setRowCount(len(rows))
        for r, (ts, exercise, rating, trivia) in enumerate(reversed(rows)):
            self.table.setItem(r, 0, QTableWidgetItem(ts))
            self.table.setItem(r, 1, QTableWidgetItem(exercise))
            rating_item = QTableWidgetItem(rating)
            rating_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(r, 2, rating_item)
            trivia_item = QTableWidgetItem(trivia)
            trivia_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(r, 3, trivia_item)
        if self.table.rowCount() > 0:
            self.table.setRowHeight(0, 48)

        # ── Compute per-exercise averages (ignoring "None" entries) ──────────
        totals: dict = defaultdict(list)
        for _, exercise, rating, _ in rows:
            if rating != "None":
                try:
                    totals[exercise].append(int(rating))
                except ValueError:
                    pass

        # ── Rebuild summary cards, clearing any previous ones first ──────────
        while self.summary_layout.count():
            item = self.summary_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Color scale mirrors the rating button colors on RatingPage
        RATING_COLORS = {
            "1": "#ff4d4d",
            "2": "#ff944d",
            "3": "#ffe666",
            "4": "#b3ff66",
            "5": "#66ff66",
        }

        for exercise, values in sorted(totals.items()):
            avg   = sum(values) / len(values)
            color = RATING_COLORS.get(str(round(avg)), "#ccc")
            card  = QLabel(f"{exercise}\n\u2605 {avg:.1f} ({len(values)} rated)")
            card.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card.setWordWrap(True)
            card.setStyleSheet(f"""
                background: {color};
                border-radius: 14px;
                border: {BORDER_WIDTH_SM}px solid {BORDER_COLOR};
                font-size: {FONT_TABLE}px;
                font-weight: bold;
                padding: 16px 24px;
                color: {TEXT_PRIMARY};
            """)
            self.summary_layout.addWidget(card)