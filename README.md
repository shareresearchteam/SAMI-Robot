# Social Animated Mechanical Interlocutor (SAMI) Robot [Website](https://osusharelab.com/SAMI-Robot/)
The Social Animated Mechanical Interlocutor (SAMI) robot is based on the [Aster](https://www.thingiverse.com/thing:3992150) robot, which is a modified [Poppy](https://www.thingiverse.com/thing:2280067) robot that used MG996R servo motors instead of the much more expensive dynamixels. The SAMI robot has been modified to use the HiWonder HTS serial bus servo motor series in addition to implementing additional features.

## High Level System Capabilities

### Robot
Serial USB connection to PC to send expressions/joint movement commands
Capabilities & DoF:
 1. 8x8 LED matrix eyes, with a bunch of premade expressions (but, as previously mentioned, you can send custom ones, or swap out the eyes entirely
 2. 3 DoF in neck for pan, forward tilt, and side tilt
 3. 2 DoF in chest for forward-backward and side-side lean
 4. 4 DoF for arm (two for the shoulder, one in bicep for arm rotation, one in elbow)
 5. Single tendon gripper for open/close hand (or easy swap in for static or other hand)
 6. 3 DoF for legs (one each hip, knee, ankle)
 7. Mr. Potato Head style swappable headshell parts

### Sensor Box
Serial USB connection sends messages to PC about:
 - Button presses
 - Person presence/movement (ultrasonic + PIR, we’re still fiddling with calibration, but basically to register is someone walks by or comes up to the system)
 - RFID (for specific participant recognition)

### Captions/Speakers/Video/Microphone
Captions are a mini monitor hooked up to the computer, speakers, video and microphone are a webcam or whatever hardware connected to a PC.

### Utilities/etc:
 - JSON-structured animation/behavior/interaction authoring
 - Planning to make some C libraries (with python and c# wrappers) for things like handling serial communication and running the JSON animations/etc
 - Premade eye expressions
 - Premade robot animations/behaviors

## Assembly

## Operation
High level command and operation is managed on a computer system, 
Low level communication with the robot is performed via serial over USB, using the communication packet architecture presented below. 




## Components/Packages/How TF do I organize this???
Mechanical
Electrical
Arduino Code
C Libraries
JSON behavior files
Audio files + caption text
C# testing/development UI
3D model files
URDF model

## Software & Running SAMI

To run SAMI, look at the [software README](software/README.md) for further instructions