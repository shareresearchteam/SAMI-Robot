# ==============================================================================
# ExercisePage.py — Exercise selection and behavior execution page.
#
# Displays available exercises as GIF previews with action buttons.
# Triggers robot behaviors and navigates to the rating page on completion.
# ==============================================================================

import json

# ── PyQt6 imports ─────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout,
    QLabel, QPushButton,
)
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QTimer

# ── Project imports ───────────────────────────────────────────────────────────
from components.home_button import HomeButton
from components.page_title import PageTitle
from components.action_button import ActionButton


# ==============================================================================
# Exercise Page
# ==============================================================================

class ExercisePage(QWidget):
    """Displays available exercises as GIF previews with action buttons."""

    def __init__(self, parent_ui):
        super().__init__()

        self.parent_ui = parent_ui

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 10)
        layout.setSpacing(8)

        # ── Title ────────────────────────────────────────────────────────────
        layout.addWidget(PageTitle("Select an Exercise to Perform"))
        layout.addStretch(1)

        # ── Exercise grid ────────────────────────────────────────────────────
        grid = QGridLayout()
        grid.setSpacing(40)
        layout.addLayout(grid)

        # ── Exercise configuration ───────────────────────────────────────────
        # behaviors = self.parent_ui.get_behavior_files()
        self.exercise_config = [
            {"title": "Wave", "description": "Wave hello to the adoring fans", "file": "Wave.json", "video": "assets/exercises/Waving.gif",
             "why": "Waving engages the shoulder and elbow joints, promoting upper limb mobility and coordination."},
            {"title": "Shrug", "description": "What's Happening?", "file": "Shrug.json", "video": "assets/exercises/Shrug.gif",
             "why": "Shoulder shrugs strengthen the trapezius muscles and help release tension in the neck and upper back."},
            {"title": "Side Stretch", "description": "Helps with core strength", "file": "SideToSide.json", "video": "assets/exercises/SideToSide.gif",
             "why": "Side-to-side stretching improves spinal flexibility, activates the obliques, and enhances balance."},
        ]

        # ── Build exercise grid cells ────────────────────────────────────────
        positions = [(0, c) for c in range(3)]

        for (row, col), behavior in zip(positions, self.exercise_config[:3]):

            # ── Cell container ────────────────────────────────────────────
            cell_widget = QWidget()
            cell_layout = QVBoxLayout(cell_widget)
            cell_layout.setSpacing(10)

            # ── GIF preview ──────────────────────────────────────────────
            gif_label = QLabel()
            gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            movie = QMovie(behavior["video"])
            gif_label.setMovie(movie)
            movie.start()

            cell_layout.addWidget(gif_label)
            cell_layout.addStretch(1)

            # ── Exercise button ──────────────────────────────────────────
            btn = ActionButton(
                behavior["title"] + "\n" + behavior["description"],
                min_width=400, min_height=200,
            )

            btn.clicked.connect(
                lambda _, f=behavior["file"], t=behavior["title"]:
                self.perform_behavior(f, t)
            )

            cell_layout.addWidget(btn)

            grid.addWidget(cell_widget, row, col)

        layout.addStretch(1)

        # ── Home button ──────────────────────────────────────────────────────
        home_button = HomeButton("Return Home")
        layout.addWidget(home_button)
   
        home_button.clicked.connect(lambda _: self.parent_ui.stack.setCurrentWidget(self.parent_ui.home_page))
        layout.addWidget(home_button)

    # ── Load behavior files ──────────────────────────────────────────────────
    # def get_first_six_behaviors(self):
    #     folder = self.parent_ui.behavior_folder
    #     files = [f.replace(".json", "") for f in os.listdir(folder) if f.endswith(".json")]
    #     return files[:6]

    # ── Start behavior ───────────────────────────────────────────────────────
    def start_exercise(self, name):
        """Queue an exercise behavior and return home after a delay."""
        print(f"Starting behavior: {name}")

        # Start behavior from main UI
        self.parent_ui.start_behavior(name)

        # After behavior finishes, return to home
        # If behaviors are synchronous:
        self.return_home_after_delay(3000)

    def return_home_after_delay(self, delay_ms):
        """Schedule a return to the home page after *delay_ms* milliseconds."""
        QTimer.singleShot(delay_ms, self.go_home)

    # def go_home(self):
    #     self.parent_ui.stack.setCurrentWidget(self.parent_ui.home_page)  # assuming home is a widget

    def load_behavior(self, behavior_file):
        """Load keyframes from a behavior JSON file."""
        with open(behavior_file, 'r') as file:
                return json.load(file)['Keyframes']

    def handle_send_command(self):
        """Parse angle/time inputs and send a single joint command."""
        joint_name = self.joint_name_dropdown.currentText()
        try:
            angle = int(self.angle_input.text())
            move_time = int(self.time_input.text())
        except ValueError:
            print("Please enter valid numbers for angle and move time.")
            return
        joint_id = self.get_joint_id(joint_name)
        self.send_joint_command([joint_id], [angle], move_time)

    def move_to_home(self):
        """Send the robot to its home position via the Home behavior file."""
        self.parent_ui.start_behavior("Home.json")

        # neutral_value = self.emote_mapping.get("Neutral", 1)
        # self._send_emote(neutral_value)

    # def move_to_home(self):
    #     joint_ids = [joint['JointID'] for joint in self.full_joint_config]
    #     home_angles = [joint['HomeAngle'] for joint in self.full_joint_config]
    #     self.send_joint_command(joint_ids, home_angles, 10)

    def set_buttons_enabled(self, enabled: bool):
        """Enable or disable all QPushButtons on this page."""
        for btn in self.findChildren(QPushButton):
            btn.setEnabled(enabled)

    # ── Perform behavior ─────────────────────────────────────────────────────
    def perform_behavior(self, behavior_file, display_title):
        """Lock the UI, show the exercise overlay, and start the behavior."""

        self.set_buttons_enabled(False)

        self.parent_ui.selected_exercise = display_title

        # Find the matching exercise config entry for its GIF and why text
        exercise = next((e for e in self.exercise_config if e["title"] == display_title), None)
        video = exercise["video"] if exercise else None
        why   = exercise["why"]   if exercise else ""

        # Show exercise overlay with GIF and reason
        self.parent_ui.exercise_overlay.set_exercise(display_title, video, why)
        self.parent_ui.stack.setCurrentWidget(self.parent_ui.exercise_overlay)

        # Start behavior with callback
        self.parent_ui.start_behavior(
            behavior_file,
            on_finished=self.on_behavior_finished
        )
        # self.parent_ui.move_to_home()


        # behavior_path = os.path.join(self.behavior_folder, selected_behavior)
        # behavior_motion = self.load_behavior(behavior_path)
        # for frame in behavior_motion:
        #     # Process Audio if available.
        #     if frame.get("AudioClip","") != "":
        #         # Use "AudioClip" if provided; otherwise fall back to the "Expression" or a default.
        #         #audio_clip = keyframe.get("AudioClip", keyframe.get("Expression", "default_audio"))
        #         audio_clip = frame.get("AudioClip")
        #         print("Processing audio keyframe – playing:", audio_clip)
        #         self.audio_manager.process_audio_call(audio_clip)
        #     # Process Emote if available.
        #     if frame.get("Expression","") != "":
        #         expression = frame.get("Expression", "Neutral")
        #         emote_value = self.emote_mapping.get(expression, 0)
        #         self.send_emote(emote_value)
        #     # Process Joint Commands if available.
        #     if frame["HasJoints"] == "True":
        #         joint_ids = [self.get_joint_id(j['Joint']) for j in frame['JointAngles']]
        #         angles = [j['Angle'] for j in frame['JointAngles']]
        #         move_time = frame["JointMoveTime"]
        #         self.send_joint_command(joint_ids, angles, move_time)
        #     self.delay(frame["WaitTime"] / 1000)

    def show_rating_page(self):
        """Navigate to the rating page."""
        self.parent_ui.stack.setCurrentWidget(self.parent_ui.rating_page)

    def on_behavior_finished(self):
        """Called when a behavior completes — re-enable buttons and go home."""
        self.set_buttons_enabled(True)

        self.parent_ui.start_behavior("Home.json", on_finished=self._go_to_rating)

    def _go_to_rating(self):
        """Called once Home.json finishes — safe to show the rating page."""
        self.parent_ui.stack.setCurrentWidget(self.parent_ui.rating_page)


    def closeEvent(self, event):
        self.close_connection()
        event.accept()