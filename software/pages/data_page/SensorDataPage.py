# ==============================================================================
# SensorDataPage.py — Sensor demo video player page.
#
# Displays a playable video (capstone-proof.mp4) using Qt's multimedia stack.
# Provides Play/Pause and Stop controls beneath the video.
# ==============================================================================

import os

# ── PyQt6 imports ─────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
)
from PyQt6.QtCore import Qt

# ── Project imports ───────────────────────────────────────────────────────────
from components.page_title import PageTitle
from components.action_button import ActionButton
from components.back_home_nav import BackHomeNav


# ==============================================================================
# Sensor Data Page
# ==============================================================================

class SensorDataPage(QWidget):
    """
    Displays a playable video (capstone-proof.mp4) using Qt's multimedia stack.
    Provides Play/Pause and Stop controls beneath the video.
    """

    def __init__(self, parent_ui):
        super().__init__()

        self.parent_ui = parent_ui

        from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
        from PyQt6.QtMultimediaWidgets import QVideoWidget
        from PyQt6.QtCore import QUrl

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(16)

        # ── Page title ───────────────────────────────────────────────────────
        layout.addWidget(PageTitle("Sensor Demo"))

        # ── Video widget ─────────────────────────────────────────────────────
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumHeight(480)
        self.video_widget.setStyleSheet("background: #000; border-radius: 12px;")
        layout.addWidget(self.video_widget)

        # ── Media player wired to the video widget ───────────────────────────
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)
        self.player.setSource(QUrl.fromLocalFile(
            os.path.abspath("assets/capstone-proof.mp4")
        ))

        # ── Playback controls ────────────────────────────────────────────────
        controls = QHBoxLayout()
        controls.setSpacing(24)
        controls.setAlignment(Qt.AlignmentFlag.AlignCenter)

        play_btn = ActionButton("\u25b6  Play / Pause", min_width=300, min_height=80)
        play_btn.clicked.connect(self._toggle_play)
        controls.addWidget(play_btn)

        stop_btn = ActionButton("\u25a0  Stop", min_width=200, min_height=80)
        stop_btn.clicked.connect(self._stop)
        controls.addWidget(stop_btn)

        layout.addLayout(controls)
        layout.addStretch(1)

        # ── Back and Home buttons ────────────────────────────────────────────
        nav = BackHomeNav(parent_ui, back_page=parent_ui.data_page)
        layout.addLayout(nav.layout)

    def _toggle_play(self):
        """Toggle between playing and paused."""
        from PyQt6.QtMultimedia import QMediaPlayer
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def _stop(self):
        """Stop playback and return to the beginning."""
        self.player.stop()