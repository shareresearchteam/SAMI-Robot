# ==============================================================================
# SAMI_UI.py — Main UI entry point for the SAMI robot control interface.
#
# Defines the ExercisePage, ExerciseOverlay, and the main SAMIControlUI window
# that ties all pages together with a QStackedWidget. Supports both a full
# presentation UI and a legacy debug UI via the USE_NEW_UI flag.
# ==============================================================================

import sys
import time
import os
import json
import csv
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ── PyQt6 imports ─────────────────────────────────────────────────────────────
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget,
    QVBoxLayout, QGridLayout,
    QLabel, QPushButton,
)
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QTimer

# ── Project imports ───────────────────────────────────────────────────────────
from SAMIControl import SAMIControl
from styles.theme import (
    BG_APP, TEXT_PRIMARY, TEXT_ON_BUTTON,
    FONT_SUBTITLE, FONT_BUTTON,
)
from components.home_button import HomeButton
from components.button import Button
from components.page_title import PageTitle
from components.action_button import ActionButton
from pages.HomePage import HomePage
from pages.RatingPage import RatingPage
from pages.trivia_page import TriviaLandingPage, TriviaQuestionPage, TriviaAnswerPage, TriviaScorePage
from pages.data_page.DataPage import DataPage
from pages.data_page.SensorDataPage import SensorDataPage
from pages.data_page.RatingDataPage import RatingDataPage
from pages.DevPage import DevPage

# ── UI mode toggle ───────────────────────────────────────────────────────────
# Set to True  → full presentation UI  (pages, stack, trivia, etc.)
# Set to False → legacy debug UI       (joint dropdowns, raw commands)
USE_NEW_UI = True


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
                min_width=400, min_height=200, font_size=32,
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


# ==============================================================================
# Exercise Overlay
# ==============================================================================

class ExerciseOverlay(QWidget):
    """
    Shown while SAMI performs an exercise.
    Displays the exercise GIF, the exercise title, and a short
    explanation of why the movement is beneficial.
    Call set_exercise() before switching to this page.
    """

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # ── Animated GIF ──────────────────────────────────────────────────
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gif_label.setSizePolicy(
            self.gif_label.sizePolicy().horizontalPolicy(),
            __import__('PyQt6.QtWidgets', fromlist=['QSizePolicy']).QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.gif_label, stretch=3)

        # ── Status label ─────────────────────────────────────────────────
        self.status_label = QLabel("SAMI is moving...")
        self.status_label.setStyleSheet(
            f"color: {TEXT_ON_BUTTON}; font-size: {FONT_SUBTITLE}px; font-weight: bold;"
        )
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label, stretch=1)

        # ── Why-this-exercise label ──────────────────────────────────────
        self.why_label = QLabel()
        self.why_label.setWordWrap(True)
        self.why_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.why_label.setStyleSheet(
            f"color: {TEXT_PRIMARY}; font-size: {FONT_BUTTON}px; font-style: italic;"
        )
        layout.addWidget(self.why_label, stretch=1)

        self._movie = None

    def set_exercise(self, title: str, video_path: str | None, why: str):
        """Update overlay content before it is shown."""
        self.status_label.setText(f"SAMI is performing: {title}")

        # ── Load and start the GIF ───────────────────────────────────────
        if video_path:
            self._movie = QMovie(video_path)
            self.gif_label.setMovie(self._movie)
            self._movie.start()
            self.gif_label.setVisible(True)
        else:
            self.gif_label.setVisible(False)

        self.why_label.setText(why)


# ==============================================================================
# SAMIControlUI  —  Main application window
# ==============================================================================

class SAMIControlUI(SAMIControl, QMainWindow):
    """
    Top-level window that combines SAMIControl (robot comms) with a
    QMainWindow (PyQt6 UI).  Manages the page stack, trivia state, and
    exercise ratings.
    """

    def __init__(self, 
                 arduino_port='/dev/tty.usbserial-10', 
                 baud_rate=115200,
                 joint_config_file='Joint_config.json',
                 behavior_folder='behaviors',
                 emote_file='Emote.json',
                 audio_folder='audio',
                 starting_voice='Matt'):
        SAMIControl.__init__(self, arduino_port, baud_rate, joint_config_file,behavior_folder, emote_file, audio_folder, starting_voice)
        # QWidget.__init__(self)
        QMainWindow.__init__(self)
        with open(joint_config_file, 'r') as f:
            self.full_joint_config = json.load(f)['JointConfig']
        self.full_joint_map = {joint['JointName']: joint for joint in self.full_joint_config}
        self.behavior_folder = behavior_folder if os.path.exists(behavior_folder) else 'behaviors'
        self.emote_mapping = self.load_emote_mapping(emote_file)

        self.selected_exercise = None
        self.last_rating = None
        self.rating_file = "data/interaction_ratings.txt"
        self.trivia_score_file = "data/trivia_scores.txt"
        self.last_trivia_score_str = ""  # e.g. "7/10", set after trivia ends

        # ── Trivia state ─────────────────────────────────────────────────
        self.trivia_questions = []
        self.trivia_index = 0
        self.trivia_score = 0
        self.trivia_last_correct = False
        self.trivia_csv = "trivia/showcase_trivia.csv"

        self.initUI()

        if arduino_port:
            try:
                self.initialize_serial_connection()
            except Exception as e:
                print(f"Could not connect to Arduino: {e} — running in UI-only mode.")

    def delay(self, t):
        """Block the current thread for *t* seconds."""
        time.sleep(t)

    # ── UI entry point ─────────────────────────────────────────────────────────
    def initUI(self):
        """Dispatch to the appropriate UI based on the USE_NEW_UI flag at the top of the file."""
        if USE_NEW_UI:
            self._initUI_new()
        else:
            self._initUI_legacy()

    # ── New presentation UI ────────────────────────────────────────────────────
    def _initUI_new(self):
        """Full presentation UI: stacked pages, trivia, exercise overlay, data pages."""
        self.setWindowTitle("SAMI UI")
        self.resize(1920, 1080)
        self.setStyleSheet(f"background-color: {BG_APP};")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_page          = HomePage(self);          self.stack.addWidget(self.home_page)
        self.exercise_page      = ExercisePage(self);      self.stack.addWidget(self.exercise_page)
        self.exercise_overlay   = ExerciseOverlay();       self.stack.addWidget(self.exercise_overlay)
        self.data_page          = DataPage(self);          self.stack.addWidget(self.data_page)
        self.sensor_data_page   = SensorDataPage(self);    self.stack.addWidget(self.sensor_data_page)
        self.rating_data_page   = RatingDataPage(self);    self.stack.addWidget(self.rating_data_page)
        self.rating_page        = RatingPage(self);        self.stack.addWidget(self.rating_page)
        self.trivia_page        = TriviaLandingPage(self);        self.stack.addWidget(self.trivia_page)
        self.trivia_question_page = TriviaQuestionPage(self); self.stack.addWidget(self.trivia_question_page)
        self.trivia_answer_page = TriviaAnswerPage(self);  self.stack.addWidget(self.trivia_answer_page)
        self.trivia_score_page  = TriviaScorePage(self);   self.stack.addWidget(self.trivia_score_page)
        self.dev_page           = DevPage(self);           self.stack.addWidget(self.dev_page)

        self.stack.setCurrentWidget(self.home_page)

    # ── Legacy debug UI ────────────────────────────────────────────────────────
    def _initUI_legacy(self):
        """Original debug UI: joint dropdowns, angle inputs, raw command buttons."""
        from PyQt6.QtWidgets import QLineEdit, QComboBox

        self.resize(600, 400)
        self.setWindowTitle("SAMI Control")

        container = QWidget()
        layout = QVBoxLayout(container)
        self.setCentralWidget(container)

        self.joint_name_dropdown = QComboBox(self)
        self.joint_name_dropdown.addItems(list(self.full_joint_map.keys()))
        layout.addWidget(self.joint_name_dropdown)

        self.angle_input = QLineEdit(self)
        self.angle_input.setPlaceholderText("Enter Angle")
        layout.addWidget(self.angle_input)

        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("Enter Move Time")
        layout.addWidget(self.time_input)

        send_button = QPushButton("Send Command", self)
        send_button.clicked.connect(self.handle_send_command)
        layout.addWidget(send_button)

        home_button = QPushButton("Home", self)
        home_button.clicked.connect(self.move_to_home)
        layout.addWidget(home_button)

        self.behavior_dropdown = QComboBox(self)
        self.behavior_dropdown.addItems(self.get_behavior_files())
        layout.addWidget(self.behavior_dropdown)

        behavior_button = QPushButton("Perform Behavior", self)
        behavior_button.clicked.connect(self.perform_behavior)
        layout.addWidget(behavior_button)


    def load_behavior(self, behavior_file):
        """Load keyframes from a behavior JSON file."""
        with open(behavior_file, 'r') as file:
            return json.load(file)['Keyframes']

    def handle_send_command(self):
        """Parse the angle/time inputs and send a single joint command."""
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
        """Send all joints to their home angles."""
        joint_ids = [joint['JointID'] for joint in self.full_joint_config]
        home_angles = [joint['HomeAngle'] for joint in self.full_joint_config]
        self.send_joint_command(joint_ids, home_angles, 10)

    def get_behavior_files(self):
        """Return a list of .json files in the behavior folder."""
        return [f for f in os.listdir(self.behavior_folder) if f.endswith('.json')]

    def perform_behavior(self):
        """Start the behavior selected in the legacy dropdown."""
        selected_behavior = self.behavior_dropdown.currentText()
        self.start_behavior(selected_behavior)
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

    def closeEvent(self, event):
        """Close the serial connection before the window is destroyed."""
        self.close_connection()
        event.accept()

    # ── Rating helpers ─────────────────────────────────────────────────────────

    def submit_rating(self, value):
        """Persist the user's interaction rating to disk, then return home."""
        import datetime

        interaction = self.selected_exercise or "Unknown"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        trivia_score = self.last_trivia_score_str or ""

        line = f"{timestamp} | {interaction} | {value} | {trivia_score}\n"

        with open(self.rating_file, "a") as f:
            f.write(line)

        self.last_rating = value

        # ── Reset trivia score context after writing ─────────────────────
        self.last_trivia_score_str = ""

        # ── Return to home page after rating ─────────────────────────────
        self.stack.setCurrentWidget(self.home_page)

    def trivia_save_score(self):
        """Log the trivia round score to trivia_scores.txt."""
        import datetime

        total = len(self.trivia_questions)
        score = self.trivia_score
        pct = int(score / total * 100) if total else 0
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        line = f"{timestamp} | {score}/{total} | {pct}%\n"

        with open(self.trivia_score_file, "a") as f:
            f.write(line)

        # ── Store for the rating page to reference ───────────────────────
        self.last_trivia_score_str = f"{score}/{total}"

    # ── Trivia helpers ─────────────────────────────────────────────────────────

    def trivia_load_questions(self, limit=None):
        """Shuffle trivia CSV and optionally cap at *limit* questions."""
        path = self.trivia_csv
        if not os.path.exists(path):
            print(f"Trivia CSV not found: {path}")
            self.trivia_questions = []
            return
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            all_questions = list(reader)
        random.shuffle(all_questions)
        if limit:
            all_questions = all_questions[:limit]
        self.trivia_questions = all_questions
        self.trivia_index = 0
        self.trivia_score = 0
        self.trivia_last_correct = False

    def trivia_current_question(self, offset=0):
        """Return the question dict at the current index (+ optional offset)."""
        idx = self.trivia_index + offset
        if 0 <= idx < len(self.trivia_questions):
            return self.trivia_questions[idx]
        return None

    def trivia_submit_answer(self, letter):
        """Check the chosen letter against the correct answer and advance."""
        q = self.trivia_current_question()
        if not q:
            return
        correct_text = q["correct_answer"].strip().lower()
        chosen_text  = q[f"option_{letter.lower()}"].strip().lower()
        self.trivia_last_correct = (chosen_text == correct_text)
        if self.trivia_last_correct:
            self.trivia_score += 1
        self.trivia_index += 1


def main():
    app = QApplication([])
    window = SAMIControlUI(audio_folder="audio", starting_voice="Matt")
    window.show()  
    app.exec()

if __name__ == "__main__":
    main()
