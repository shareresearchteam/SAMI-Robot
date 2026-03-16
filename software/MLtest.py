
import time
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QComboBox, QLabel
from PyQt5.QtCore import QTimer
from SAMIControl import SAMIControl
import serial
import random
from MLpresencemodel import PresenceModel, parse_sensor_line
from collections import deque


class SAMIControlUI(SAMIControl, QWidget):
    def __init__(self, 
                arduino_port='/dev/ttyUSB0', 
                sensor_port='/dev/ttyACM0',
                baud_rate=115200,
                joint_config_file='Joint_config.json',
                behavior_folder='behaviors',
                emote_file='Emote.json',
                audio_folder='audio',
                starting_voice='Matt'):
        SAMIControl.__init__(self, arduino_port, baud_rate, joint_config_file,behavior_folder, emote_file, audio_folder, starting_voice)
        QWidget.__init__(self)
        with open(joint_config_file, 'r') as f:
            self.full_joint_config = json.load(f)['JointConfig']
        self.full_joint_map = {joint['JointName']: joint for joint in self.full_joint_config}
        self.behavior_folder = behavior_folder if os.path.exists(behavior_folder) else 'behaviors'
        
        # sensor log
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)
        self.event_log_file = os.path.join(self.log_dir, "sensor_events.log")

        self.last_sensor_state = None

        self.confidence_window = deque(maxlen=8)  # recent confidence probabilities
        self.ewma = 0.0        # exponentially weighted moving average of presence (0.0–1.0)
        self.ewma_alpha = 0.3  # higher = more reactive, lower = smoother

        self.presence_start_time = None
        
        self.initUI()

        self.sensor_port = sensor_port
        self.sensor_baud = baud_rate
        self.sensor_ser = None
        self.initialize_sensor_connection()

        # put paths to correct files here
        self.presence_model = PresenceModel(
            model_path="/path/to/xgboost_best_model.json",
            scaler_path="/path/to/scaler_best_model.pkl",
            metadata_path="/path/to/best_model_metadata.pkl"
        )

        self.person_present = False   # current state
        self.behavior_active = False  # prevent re-trigger 


        self.initialize_serial_connection()

    def delay(self, t):
        time.sleep(t)

    def initUI(self): # read from sensor box 
        self.sensor_timer = QTimer(self)
        self.sensor_timer.timeout.connect(self.read_sensor_data) 
        self.sensor_timer.start(100)

    def load_behavior(self, behavior_file):
        with open(behavior_file, 'r') as file:
            return json.load(file)['Keyframes']

    def handle_send_command(self):
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
        joint_ids = [joint['JointID'] for joint in self.full_joint_config]
        home_angles = [joint['HomeAngle'] for joint in self.full_joint_config]
        self.send_joint_command(joint_ids, home_angles, 10)

    def get_behavior_files(self):
        return [f for f in os.listdir(self.behavior_folder) if f.endswith('.json')]

    def perform_behavior(self):
        selected_behavior = self.behavior_dropdown.currentText()
        self.start_behavior(selected_behavior)

    def closeEvent(self, event):
        self.close_connection()
        event.accept()

    def initialize_sensor_connection(self):
        try:
            #self.sensor_ser = serial.Serial(self.sensor_port, self.sensor_baud, timeout=1)
            self.sensor_ser = serial.Serial(self.sensor_port,self.sensor_baud,timeout=0)
            print(f"Connected to sensor Arduino on {self.sensor_port}")
        except serial.SerialException as e:
            print(f"Failed to connect to sensor Arduino on {self.sensor_port}: {e}")
            self.sensor_ser = None

    def log_event(self, message):
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
        try:
            with open(self.event_log_file, "a") as f:
                f.write(f"{timestamp} {message}\n")
        except Exception as e:
            print(f"Logging error: {e}")

    def on_person_detected(self, probability):
        if not self.behavior_active:
            self.behavior_active = True
            print("Started Wave")
            self.start_behavior("Wave.json")
            # after wave return home, then reset flag
            QTimer.singleShot(6000, self.return_home)

    def return_home(self):
        print("Returning to Home")
        self.start_behavior("Home.json")
        QTimer.singleShot(2000, self.reset_behavior_flag)  # reset after home completes



    def reset_behavior_flag(self):
        self.behavior_active = False


    
    def read_sensor_data(self):
        if self.sensor_ser is None:
            return

        try:
            while self.sensor_ser.in_waiting:
                line = self.sensor_ser.readline().decode('utf-8').strip()
                if not line:
                    continue

                sensor_data = parse_sensor_line(line)
                if sensor_data is None:
                    continue

                prediction, probability = self.presence_model.predict(sensor_data)

                # update EWMA: positive readings contribute their probability, negative readings contribute 0
                new_value = probability if prediction == 1 else 0.0
                self.ewma = self.ewma_alpha * new_value + (1 - self.ewma_alpha) * self.ewma

                # print results
                print(f"pred={prediction} | prob={probability:.2%} | ewma={self.ewma:.2%}")

                # if ewma is above threshold and no previous presence:
                if self.ewma >= 0.75 and not self.person_present:
                    self.person_present = True
                    self.presence_start_time = time.time()
                    self.log_event("PERSON ARRIVED")
                    self.on_person_detected(self.ewma)
                    self.start_behavior("presence.json")

                # if ewma drops below lower threshold, person has left
                if self.ewma < 0.6 and self.person_present:
                    duration = time.time() - self.presence_start_time
                    self.log_event(f"PERSON LEFT (presence duration {duration:.1f} seconds)")
                    self.presence_start_time = None
                    self.person_present = False
                    self.start_behavior("nopresence.json")

        except Exception as e:
            print(f"Sensor read error: {e}")



def main():
    app = QApplication([])
    window = SAMIControlUI(audio_folder="audio", starting_voice="Matt",arduino_port="/dev/ttyUSB0",sensor_port="/dev/ttyACM0")
    app.exec_()

if __name__ == "__main__":
    main()
