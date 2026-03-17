# ==============================================================================
# DataPage.py — Data hub page for the SAMI UI.
#
# Presents two navigation buttons: Sensor Demo and Rating Data,
# linking to their respective sub-pages.
# ==============================================================================

# ── PyQt6 imports ─────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout,
)

# ── Project imports ───────────────────────────────────────────────────────────
from components.home_button import HomeButton
from components.page_title import PageTitle
from components.icon_nav_button import IconNavButton


# ==============================================================================
# Data Page (hub)
# ==============================================================================

class DataPage(QWidget):
    """
    Hub page replacing the old SensorPage.
    Presents two navigation buttons: Sensor Data and Rating Data.
    """

    def __init__(self, parent_ui):
        super().__init__()

        self.parent_ui = parent_ui

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 10)
        layout.setSpacing(8)

        # ── Page title ───────────────────────────────────────────────────────
        layout.addWidget(PageTitle("Data"))
        layout.addStretch(1)

        # ── Navigation button grid ───────────────────────────────────────────
        grid = QGridLayout()
        grid.setHorizontalSpacing(40)
        grid.setVerticalSpacing(40)

        sections = [
            ("Sensor Demo", "assets/interactions/Sensor.svg"),
            ("Rating Data", "assets/interactions/Rating.png"),
        ]

        for col, (name, icon_path) in enumerate(sections):
            btn = IconNavButton(name, icon_path)

            if name == "Sensor Demo":
                btn.clicked.connect(
                    lambda: self.parent_ui.stack.setCurrentWidget(self.parent_ui.sensor_data_page)
                )
            elif name == "Rating Data":
                btn.clicked.connect(
                    lambda: self.parent_ui.stack.setCurrentWidget(self.parent_ui.rating_data_page)
                )

            grid.addWidget(btn, 0, col)

        layout.addLayout(grid)
        layout.addStretch(1)

        # ── Home button ──────────────────────────────────────────────────────
        home_button = HomeButton("Return Home")
        home_button.clicked.connect(
            lambda _: self.parent_ui.stack.setCurrentWidget(self.parent_ui.home_page)
        )
        layout.addWidget(home_button)
