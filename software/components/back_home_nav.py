# ==============================================================================
# back_home_nav.py — Reusable "← Back" + "Return Home" navigation row.
# ==============================================================================

from PyQt6.QtWidgets import QHBoxLayout
from components.home_button import HomeButton


class BackHomeNav:
    """
    Builds a horizontal layout containing a "← Back" button and a
    "Return Home" button.  Both are `HomeButton` instances.

    Usage
    -----
        nav = BackHomeNav(parent_ui, back_page=parent_ui.data_page)
        layout.addLayout(nav.layout)

    Parameters
    ----------
    parent_ui : SAMIControlUI
        The main UI that owns the QStackedWidget.
    back_page : QWidget
        The page to navigate to when "← Back" is pressed.
    back_text : str
        Label for the back button (default "← Back").
    home_text : str
        Label for the home button (default "Return Home").
    """

    def __init__(
        self,
        parent_ui,
        back_page,
        back_text: str = "\u2190 Back",
        home_text: str = "Return Home",
    ):
        self.layout = QHBoxLayout()

        back_btn = HomeButton(back_text)
        back_btn.clicked.connect(
            lambda _: parent_ui.stack.setCurrentWidget(back_page)
        )
        self.layout.addWidget(back_btn)

        home_btn = HomeButton(home_text)
        home_btn.clicked.connect(
            lambda _: parent_ui.stack.setCurrentWidget(parent_ui.home_page)
        )
        self.layout.addWidget(home_btn)
