---
layout: default
id: software-architecture
title: Robot Software Architecture 
sidebar_label: Architecture
previous_page: sami-sim
next_page: behavior-guide
---
# Robot Software Architecture 

```text

┌──────────────────────────┐
│        SAMI UI           │
│    (PyQt5 Frontend)      │
└─────────────┬────────────┘
              │
              │ UI Events (buttons, sliders, behavior selection)
              V
┌──────────────────────────┐
│      SAMIControl         │
│ (Robot Controller API)   │
│ - Loads configs          │
│ - Validates angles       │
│ - Runs behaviors         │
│ - Sends serial packets   │
│ - Interfaces audio       │
└───────┬───────────┬──────┘
        │           │
Serial  │           │ Audio 
Packets │           V
        V     ┌──────────────────────┐
                         ------------------------   
┌──────────────────────┐ │  Audio Manager       │
│   Arduino Firmware   │ │ - Voice profiles     │
│ - Joint motion       │ │ - Plays WAV files    │
│ - Relay control      │ └──────────────────────┘
│ - Face/eyes emotes   │
└──────────────────────┘

Config Files (Editable by Users):
  • Joint_config.json   => Joint names, IDs, limits
  • Emote.json          => Eye/emote IDs
  • behaviors/*.json    => Motion/audio/emote sequences
  • audio/*.wav         => Voice files

```

# File Structure

## 1. SAMIControl (SAMIControl.py)
This is the **main control interface**. Everything the robot does goes through here.

### What does it do?
- Load joint and emote configuration  
- Open/close serial connection to Arduino  
- Send joint movement commands  
- Send emotes commands  
- Executes behaviors  
- Interface with the audio manager  
- Manage relay power  
- Validate angles using joint limits  


## 2. UI (SAMI_UI.py)
A **PyQt5 UI** for interacting with SAMI manually.

### What does it do?
- Dropdown for selecting joints  
- Inputs for angle and move time  
- “Send Command” button  
- “Move to Home” button  
- Behavior dropdown populated automatically from `/behaviors`  
- “Perform Behavior” button  
- Built-in serial connection handling  
- Auto-shutdown when window closes  

## 3. Audio Manager (audio_manager.py)
Handles voice playback based on behavior definitions.

### What does it do?
- Voice profiles (e.g., `"Matt"`)  
- `ClipName` => actual filename resolution  
- Synchronous and asynchronous audio playback  
- Folder-based audio organization  


## How the System Works
When the robot starts:
1) SAMIControlUI initializes the serial port
2) Loads joints from Joint_config.json
3) Loads emotes from Emote.json
4) Creates the UI (joint dropdown, behavior list)
5) SAMI is ready to interface!!!!! yayyy!!!



## Configuration Files


4.1 Joint_config.json

Defines every joint the robot exposes:
```text
{
  "JointName": "LeftShoulder",
  "JointID": 9,
  "HomeAngle": 180,
  "MinAngle": 30,
  "MaxAngle": 190
}
```
What you can change:
- Joint names (must match behavior JSON)
- Joint IDs (must match firmware)
- Home angle
- Min/max safe limits

4.2 Emote.json
Defines facial expressions used by behaviors:
```text
"Emotes": {
  "Neutral": 1,
  "Happy": 2,
  "Sad": 3
}
```
- You can add new expressions with no Python changes.
- Just ensure Arduino firmware knows the numeric ID.

4.3 behaviors/*.json

Each behavior is a list of keyframes, executed in order:
```text
{
  "HasAudio": "True",
  "HasEmote": "True",
  "HasJoints": "True",

  "AudioClip": "trivia_question_1",
  "Expression": "Happy",

  "JointAngles": {
    "LeftShoulder": 150,
    "RightShoulder": 45
  },

  "WaitTime": 1000
}
```

Keyframe options that can be customize:
- AudioClip
- Expression
- JointAngles (joint => angle)
- WaitTime (milliseconds)
- Optional booleans: HasAudio, HasEmote, HasJoints

