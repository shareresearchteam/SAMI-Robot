---
layout: default
id: sami-sim
title: SAMI ROS-Based Simulator
sidebar_label: SAMI Simulator
previous_page: software-setup
next_page: software-architecture
---
# SAMI ROS-Based Simulator Overview
The simulator is implemented within a ROS 2 environment and uses RViz as the physics-based simulation platform for validating SAMI’s JSON-defined behavior files. Its primary purpose is to provide a controlled and safe testing environment where behaviors can be evaluated before deployment on the physical robot, reducing the risk of hardware damage. The simulator parses the JSON behavior descriptions and executes the corresponding actions through the ROS 2 simulation stack in RViz. In addition, the system includes a graphical user interface (GUI) that enables users to interact with and manipulate SAMI within the simulated environment. While the GUI supports user interaction and debugging, the core function of the simulator is the verification and testing of JSON-specified robot behaviors. 

# SAMI ROS 2 Simulation Workspace (`sami_ws`)

The sami_ws workspace allows you to simulate the **SAMI** robot in RViz and run joint animations using pre-recorded JSON behavior files.

---

## 0. Initial Setup

If you're using a clean VM with ROS 2 Jazzy, start by installing dependencies and cloning the workspace:

```bash
git clone https://github.com/jlruballos/sami_ws.git
sudo apt install ros-jazzy-joint-state-publisher-gui
sudo apt install ros-jazzy-xacro
```

Then:

```bash
cd ~/sami_ws
```

---

## 1. Build the Workspace

In your terminal:

```bash
colcon build
```

Then, source the workspace:

```bash
source install/setup.bash
```

---

## 2. Launch the SAMI Robot in RViz

To visualize the robot:

```bash
ros2 launch sami_sim display.launch.py
```

You should see **SAMI** loaded in RViz with a joint control panel on the left.

---

## 3. Run the Behavior Playback

> **Important:** Before running the script, **close** the Joint State Publisher GUI to avoid conflicts.

Open a **new terminal**, then:

```bash
cd ~/sami_ws
source install/setup.bash
ros2 run sami_sim json_joint_publisher.py
```

This will play the behavior file specified by the `behavior` variable inside the script (default: `TEST.json`).

---

## 4. Using Custom Behavior Files

To change which behavior file is played:

1. Place your `.json` file in the `sami_sim/behaviors/` directory.
2. Open `json_joint_publisher.py`.
3. Modify this line near the top:

```python
behavior = 'TEST.json'
```
4. Rebuild your workspace and re-run the script:

```bash
colcon build
source install/setup.bash
ros2 run sami_sim json_joint_publisher.py
```

---

## Summary

| Task                         | Command                                                    |
| ---------------------------- | ---------------------------------------------------------- |
| Initial setup (new VM)       | `git clone ... && sudo apt install ...`                    |
| Navigate to workspace        | `cd ~/sami_ws`                                             |
| Build workspace              | `colcon build`                                             |
| Source environment           | `source install/setup.bash`                                |
| Launch RViz + robot          | `ros2 launch sami_sim display.launch.py`                   |
| Run behavior playback        | `ros2 run sami_sim json_joint_publisher.py`                |
| Use custom behavior file     | Edit `behavior = 'YourFile.json'` in `json_joint_publisher.py` |

---

# Robot Joint Configuration

## Joint Table

| **Joint Name**     | **Joint ID** | **Home Angle** | **Home Min Angle** | **Home Max Angle** | **Min Angle** | **Max Angle** | **Positive Direction** |
|--------------------|--------------|----------------|---------------------|---------------------|---------------|---------------|-------------------------|
| **Left Side**       |              |                |                     |                     |               |               |                         |
| LeftChest          | 8            | 115            | 30                  | 180                 | 0             | 180           | CCW                     |
| LeftShoulder       | 9            | 180            | 30                  | 195                 | 0             | 195           | CW                      |
| LeftBicep          | 10           | 115            | 20                  | 180                 | 0             | 180           | CCW                     |
| LeftElbow          | 11           | 105            | 60                  | 180                 | 0             | 180           | CCW                     |
| LeftGripper        | 21           | 15             |                     |                     |               |               |                         |
| LeftHip            | 15           | 96             | 10                  | 96                  | 10            | 196           | CCW                     |
| LeftKnee           | 16           | 80             | 0                   | 85                  | 0             | 180           | CCW                     |
| LeftAnkle          | 17           | 90             | 55                  | 120                 | 50            | 120           | CCW                     |
| **Right Side**      |              |                |                     |                     |               |               |                         |
| RightChest         | 4            | 135            | 60                  | 180                 | 0             | 180           | CCW                     |
| RightShoulder      | 5            | 85             | 70                  | 240                 | 0             | 240           | CW                      |
| RightBicep         | 6            | 115            | 115                 | 180                 | 0             | 180           | CW                      |
| RightElbow         | 7            | 90             | 20                  | 155                 | 0             | 180           | CW                      |
| RightGripper       | 20           | 15             |                     |                     |               |               |                         |
| RightHip           | 13           | 84             | 84                  | 170                 | 84            | 170           | CCW                     |
| RightKnee          | 14           | 90             | 90                  | 180                 | 0             | 180           | CCW                     |
| RightAnkle         | 15           | 80             | 50                  | 120                 | 50            | 120           | CCW                     |
| **Head**            |              |                |                     |                     |               |               |                         |
| HeadNod            | 2            | 125            | 110                 | 155                 | 110           | 155           | CCW                     |
| HeadTurn           | 3            | 120            | 70                  | 160                 | 70            | 160           | CCW                     |
| HeadTilt           | 1            | 125            | 100                 | 145                 | 100           | 145           | CCW                     |
| **Torso**           |              |                |                     |                     |               |               |                         |
| TorsoBow           | 19           | 125            | 100                 | 150                 | 100           | 150           | CW                      |
| TorsoTilt          | 18           | 115            | 80                  | 160                 | 80            | 160           | CCW                     |

> **Note:** Angles are in degrees. Empty fields indicates information still needs to be tested. Please be careful when applying these limits errors/typos are possible. If any errors are found please let us know, 
