import time
import serial
import json
import threading
import queue
import os
from audio_manager import AudioManager

class SAMIControl:
    def __init__(self, 
                 arduino_port='/dev/tty.usbserial-10', 
                 baud_rate=115200,
                 joint_config_file='Joint_config.json',
                 behavior_folder='behaviors',
                 emote_file='Emote.json',
                 audio_folder='audio',
                 starting_voice='Matt',
                 audio_file_encoding='.mp3'):
        self.arduino_port = arduino_port
        self.baud_rate = baud_rate
        self.ser = None
        self.joint_map = self.load_joint_config(joint_config_file)
        self.emote_mapping = self.load_emote_mapping(emote_file)
        # Initialize the audio manager so that audio clips can be played.
        self.audio_manager = AudioManager(starting_voice, audio_folder, audio_file_encoding)
        # And save the behavior folder if it exists
        self._behavior_folder = behavior_folder if os.path.exists(behavior_folder) else ''
        self.current_behavior = ''
        self._behavior_done = True

    def load_joint_config(self, joint_config_file):
        with open(joint_config_file, 'r') as file:
            config = json.load(file)
        joint_map = {}
        self.joint_limits = {}
        for joint in config["JointConfig"]:
            joint_map[joint["JointName"]] = joint["JointID"]
            self.joint_limits[joint["JointID"]] = (joint["MinAngle"], joint["MaxAngle"])
        return joint_map

    def load_emote_mapping(self, emote_file):
        with open(emote_file, 'r') as file:
            data = json.load(file)
        return data["Emotes"]

    def initialize_serial_connection(self,relays=['E']):
        '''
        Initialize the serial connection and turn on the relays so motors have power.
        Can send arrays of options for only specific relays. So, could set ['T','A'] to power only the torso and the arms.
        E = Everything, hex value: 0x45
        T = Head and torso, hex value: 0x54
        A = Arms, hex value: 0x41
        L = Legs, hex value: 0x4C
        '''
        try:
            self.ser = serial.Serial(self.arduino_port, self.baud_rate, timeout=1)
            time.sleep(2)
            print("Serial connection established.")
            # Packet structure is < P 1 (relays) >
            packet = [0x3C, 0x50, 0x01]
            for relay in relays:
                packet.append(ord(relay))
            packet.append(0x3E)
            self.ser.write(bytearray(packet))
            print("Sent packet:", bytearray(packet))
            if self.ser.in_waiting > 0:
                msg = self.ser.readline().decode()
                print("Arduino response:", msg)
        except serial.SerialException as e:
            print("Error connecting to Arduino:", e)
    
    # Public version that checks we aren't in the middle of a behavior and then sends the pose
    def send_joint_command(self, joint_ids, joint_angles, joint_time):
        if not self._behavior_done:
            self.stop_behavior()
        self._send_joint_command(joint_ids, joint_angles, joint_time)

    # Private version that just sends without checking anything
    def _send_joint_command(self, joint_ids, joint_angles, joint_time):
        if len(joint_ids) != len(joint_angles):
            raise ValueError("Mismatch in joint IDs and angles.")
        packet = [0x3C, 0x4A, joint_time]
        for jid, angle in zip(joint_ids, joint_angles):
            if jid in self.joint_limits:
                min_angle, max_angle = self.joint_limits[jid]
                original_angle = angle
                angle = max(min(angle, max_angle), min_angle)
                if angle != original_angle:
                    print(f"[Clamp] Joint ID {jid}: Angle {original_angle} out of bounds "f"({min_angle}–{max_angle}). Clamped to {angle}.")
            packet.extend([jid, angle])
        packet.append(0x3E)
        self._send_serial_comm(bytearray(packet))
        print("Sent joint command:", bytearray(packet))

    # Public version that checks we aren't in the middle of a behavior and then sends the emote
    def send_emote(self, emote_id):
        if not self._behavior_done:
            self.stop_behavior()
        self._send_emote(emote_id)

    # Private version that just sends without checking anything
    def _send_emote(self, emote_id):
        packet = [0x3C, 0x45, emote_id, 0x3E]
        self._send_serial_comm(bytearray(packet))
        print("Sent emote command:", bytearray(packet))

    def _send_serial_comm(self, bytemessage):
        try:
            self.ser.write(bytemessage)
            print("Sent emote command:", bytemessage)
            time.sleep(1)
        except Exception as e:
            print("Error connecting to Arduino:", e)

    def close_connection(self):
        self.stop_behavior()
        if self.ser:
            self.ser.close()
            print("Serial connection closed.")

    # Handles processing for each individual keyframe
    def _process_keyframe(self):
        frame = self.q_keyframes.get()
        # Process Audio if enabled.
        if frame.get("AudioClip","") != "":
            # Use "AudioClip" if provided; otherwise fall back to the "Expression" or a default.
            #audio_clip = keyframe.get("AudioClip", keyframe.get("Expression", "default_audio"))
            audio_clip = frame.get("AudioClip")
            print("Processing audio keyframe – playing:", audio_clip)
            self.audio_manager.process_audio_call(audio_clip)
            #self.audio_manager.send_audio(audio_clip)
        # Process Emote if enabled.
        if frame.get("Expression","") != "":
            expression = frame.get("Expression", "Neutral")
            emote_value = self.emote_mapping.get(expression, 0)
            self._send_emote(emote_value)
        # Process Joint Commands if enabled.
        if frame.get("JointAngles","") != "":
            joint_ids = []
            joint_angles = []
            joint_time = frame.get("JointMoveTime", 1)
            for joint in frame["JointAngles"]:
                joint_ids.append(self.get_joint_id(joint["Joint"]))
                joint_angles.append(joint["Angle"])
            self._send_joint_command(joint_ids, joint_angles, joint_time)
        # Update our time for the next keyframe
        self.next_t = time.time() + (frame["WaitTime"]/1000)

        if self.q_keyframes.empty():
            self._behavior_done = True

            if hasattr(self, "_behavior_finished_callback") and self._behavior_finished_callback:
                from PyQt6.QtCore import QTimer
                # 🔐 Safely return to GUI thread
                QTimer.singleShot(0, self._behavior_finished_callback)

        else:
            threading.Timer(
                self.next_t - time.time(),
                self._process_keyframe
            ).start()
        # if not self._behavior_done:
        #     threading.Timer(self.next_t - time.time(), self._process_keyframe).start()


    def start_behavior(self,filename, on_finished=None):
        if not self._behavior_done:
            self.stop_behavior()
            time.sleep(1)

        with open(os.path.join(self._behavior_folder, filename), 'r') as file:
            data = json.load(file)

        self.current_behavior = data["Name"]
        self.q_keyframes = queue.SimpleQueue()

        for frame in data["Keyframes"]:
            self.q_keyframes.put_nowait(frame)

        self._behavior_done = False
        self._behavior_finished_callback = on_finished
        self._process_keyframe()
        
    def stop_behavior(self):
        self._behavior_done = True

    def run_behavior_block(self, filename):
        try:
            with open(os.path.join(self._behavior_folder, filename), 'r') as file:
                data = json.load(file)
            for keyframe in data["Keyframes"]:
                # Process Audio if enabled.
                if keyframe.get("AudioClip","") != "":
                    # Use "AudioClip" if provided; otherwise fall back to the "Expression" or a default.
                    #audio_clip = keyframe.get("AudioClip", keyframe.get("Expression", "default_audio"))
                    audio_clip = keyframe.get("AudioClip")
                    print("Processing audio keyframe – playing:", audio_clip)
                    self.audio_manager.process_audio_call(audio_clip)
                    #self.audio_manager.send_audio(audio_clip)
                # Process Emote if enabled.
                if keyframe.get("Expression","") != "":
                    expression = keyframe.get("Expression", "Neutral")
                    emote_value = self.emote_mapping.get(expression, 0)
                    self._send_emote(emote_value)
                # Process Joint Commands if enabled.
                if keyframe.get("JointAngles","") != "":
                    joint_ids = []
                    joint_angles = []
                    joint_time = keyframe.get("JointMoveTime", 1)
                    for joint in keyframe["JointAngles"]:
                        joint_ids.append(self.get_joint_id(joint["Joint"]))
                        joint_angles.append(joint["Angle"])
                    self._send_joint_command(joint_ids, joint_angles, joint_time)
                time.sleep(keyframe.get("WaitTime", 1000) / 1000)
        except:
            print("Failed to run behavior: ", filename)

    def get_joint_id(self, joint_name):
        return self.joint_map.get(joint_name, 0)

if __name__ == "__main__":
    # For testing purposes; adjust paths as necessary.
    robot = SAMIControl(arduino_port='COM8', audio_folder="audio", starting_voice="Matt")
    robot.initialize_serial_connection()
    time.sleep(1)
    # Ensure your Wave.json has at least one keyframe with HasAudio set to "True"
    robot.run_behavior_block("Wave.json")
    time.sleep(1)
    robot.close_connection()
