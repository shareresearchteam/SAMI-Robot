---
layout: default
id: robot-assembly
title: Robot Assembly Guide
sidebar_label: Robot Assembly
---
# Robot Assembly Guide
This section describes the part fabrication and hardware assembly process for the actual robot.
1. [3D Printing & Orientations](#3d-printing--orientations)
2. [Setting Up the Control Board](#setting-up-the-control-board)
3. [Initializing Servo IDs and Positions](#initializing-servo-ids-and-positions)
4. [Overall Assembly Information]()
5. [Neck and Torso Assembly](#neck-and-torso-assembly)
6. [Arm Assembly](#arm-assembly)
7. [Lower Body Assembly](#lower-body-assembly)
8. [Chair Assembly](#chair-modification-and-assembly)
9. [Final Assembly](#final-assembly)

The layout of the parts for the robot, with names that are used within these instructions.

<img src="res/sami_labeled.jpg"  width="50%"/>

## 3D Printing & Orientations
*If using Prusa i3 printers with Prusa Slicer,* all parts should be printed at 0.3mm resolution ("draft quality" on Prusa Slicer), with 15% gyroid infill, and organic supports enabled (where necessary), **except for the chest piece,** which should be printed at 0.2mm resolution, with 15% gyroid infill, and normal grid-style supports instead. Alternatively, the **finger hinges** should be printed using PETG filament with 0% gyroid infill and a brim.

**The hands** used for this robot have been sized down by 42.5% with minimal changes to the bolt holes from the [original prosthetic model](), but the mechanism funtionality remains the same.

Print orientations are shown below for each part, along with the part names that are used throughout this documentation.

### Headshell
<img src="res/Headshell.png"  width="50%"/>

### Chest and Headshell Panel
<img src="res/Chest_HeadshellSidePanel.png"  width="50%"/>

### Head/Neck Connectors and Spine
<img src="res/HeadnNeck_Connector_Spine.png"  width="50%"/>

### Shoulders and Upper Arms
<img src="res/Shoulders_Biceps.png"  width="50%"/>

### Hands and Lower Arms
<img src="res/Hands_Lower Arms.png"  width="50%"/>

### Finger Hinges
<img src="res/FFX_Finger_Hinge_Plate.png"  width="50%"/>

### Hips and Upper Legs
<img src="res/Hip_UpperLegs.png"  width="50%"/>

### Lower Legs and Feet
   <img src="res/LowerLegs_Feet.png"  width="50%"/>

## Setting Up the Control Board
Before getting into initializing the robot setup, we'll begin by connecting power to the [motor control PCB](./Electrical-Assembly.md).

1. Connect the red fork of the 12V power cable (shorter cable with large connector) to the V+ label on the 12V power supply.
2. Connect the black fork for the 12V power cable to the V- label on the 12V power supply.
3. Connect the red fork of the 5V power cable (longer cable with small connector) to the V- label on the 5V power supply.
4. Connect the black fork of the 5V power cable to the V- label on the 5V power supply.
5. Connect red, yellow, and black cables to back of power switch.

   <img src="res/switch_wiring.JPG" width="50%"/>

6. Connect other ends to locations on both th 5V and 12V power supplies:
   - Red to L
   - Yellow to N (neutral)
   - Black to GND

   <img src="res/Switch_Key.jpeg"  width="50%"/>

7. Plug power cord to switch, then to a nearby power outlet.

Reference image:

   <img src="res/PowerSupplys_Front.jpeg"  width="50%"/>

## Initializing Servo IDs and Positions
You will need to communicate with the motors as part of the assembly process. This process can be completed using the [assembled motor control PCB](#setting-up-the-control-board), or the [HiWonder motor debugging board](https://www.hiwonder.com/products/hiwonder-ttl-usb-debugging-board).

In either case, you will be initializing each motor by connecting and communicating with it individually (*not* chaining the motors). The below initialization instructions assume you are initializing the motors using the robot motor control PCB.

Before assembling the robot, it is necessary to assign unique motor IDs for each joint motor. You can set these IDs with the [SetServoID Arduino code project](../Arduino/SetServoID/) using the motor control PCB for the robot. Any ID numbers may be chosen, but the default configuration file, and these assembly instructions, will use the joint names and IDs as listed in the table below.

|     Joint Name       | ID | Assembly Pose (Angle) |
|----------------------|----| -------------------- |
| Head Tilt            | 01 | 125 |
| Head Nod             | 02 | 125 |
| Head Turn            | 03 | 120 |
| Right Chest          | 04 | 135 |
| Right Shoulder       | 05 | 85  |
| Right Bicep          | 06 | 115 |
| Right Elbow          | 07 | 90  |
| Left Chest           | 08 | 115 |
| Left Shoulder        | 09 | 180 |
| Left Bicep           | 10 | 115 |
| Left Elbow           | 11 | 105 |
| Right Hip            | 12 | 84  |
| Right Knee           | 13 | 90  |
| Right Ankle          | 14 | 80  |
| Left Hip             | 15 | 96  |
| Left Knee            | 16 | 80  |
| Left Ankle           | 17 | 90  |
| Torso Tilt           | 18 | 115 |
| Torso Bow            | 19 | 125 |
| Right Gripper        | 20 | 0   |
| Left Gripper         | 21 | 0   |

During assembly of the robot, it will be necessary to set each motor to a known rotation and then assemble the parts to match that orientation. These positions are *not operational home*, but are instead an easy reference position for use in assembly. The robot assembly pose, along with each joint name, motor ID, and the motor angle corresponding to the current pose, are shown in the image below. 

<img src="res/assembly_orientation.png" width="50%"/>

To simplify assembly, the initialization steps for each motor are:

1. Connect to board "Arduino Mega or Mega 2560" on Arduino IDE.
2. Set the motor ID of the servo with the [SetServoID Arduino code project](../Arduino/SetServoID/). Change the code to the motor ID you want to set.
3. Set the motor to it's assembly home position using the [SetServoPosition Arduino code project](../Arduino/SetServoPosition/). Change the code so that you are only running **1 motor (the ID you just set) and 1 angle (the home angle you want to set)**.
4. While the servo is in the home position, attach the servo horn such that the dimple on the horn is facing towards the servo body as shown below.

   <img src="res/Servo_Horn_Orientation.jpg" width="50%"/>
   
5. Cut power to the servo and screw down the aligned horn using the black center screw from the servo accessory bag.

## Notes On Assembly Process
Some components are sensitive, or could be easily damaged during assembly. To help mitigate this, these notes are provided as important notes to keep in mind during the process.

### Screwing Threading Plastic and Metal
The entire system is largely assembled with machine screws through 3D printed parts, with either lock nuts or captured square nuts as backing. To aid with alignment and minimize cross-threading the nuts or other components, it's recommended to first screw the machine screws all the way into the 3D printed hole, to thread the plastic and clear any debris from the 3D printing process, before unscrewing the screws, and then assembling the full joint with any nuts, servos, or motor horns screwed in once the plastic holes have been cleared and the screw screws easily into the plastic hole.

Additionally, when screwing to the metal servo horns, it is very easy to misalign your screw and cross thread the screw onto the servo horn. Clearing plastic holes first should allow you to easily hand thread the screw through the plastic into the horn, and simply finish tightening the fully inserted screw down with a hex screwdriver.

### Servo Horn Alignment
Once a motor has been set to the default position, you can attach the metal horn with the small indent facing towards the motor body (see below image) as a useful visual reference to assist in verifying that the servo does not get misaligned or shifted during the assembly process.

<img src="res/Servo_Horn_Orientation.jpg" width="50%"/>


### Servo JST Cables
The JST cables that come with the servos are a very tight fit into the servo recepticals. We recommend only partially inserting them for initial assembly and testing. These partially inserted connectors will still make electrical contact for continuity testing and motor operation, while still providing more space for pliers to pull the header out without touching the wires themselves. Once operation is confirmed, the connectors can easily be pressed the rest of the way in.

Additionally, despite how tight the connectors are into the recepticals, be very careful when disconnecting them to not pull on the cable wires themselves, as this could damage the individual wires or pull them out of the JST header.

## Lower Body Assembly
When assembling the lower body it is best to start with the feet and then work your way up to the upper legs. This ensures that you will have everything aligned and allows you to plug to corresponding JST cables as you go.

The first and foremost step that is **highly** recommended is pre-setting all of the Lower Body motors before beginning the assembly. 

The HiWonder HTS-20H servos involved in this assembly would be:
 - Right Hip
 - Right Knee
 - Right Ankle
 - Left Hip
 - Left Knee
 - Left Ankle
 
All correlated motor IDs are listed above in [Initializing Servo IDs and Positions](#initializing-servo-ids-and-positions), as well as instructions for how to set the IDs and their home positions. It is also recommended that you check the servo horn orientation during this time, following the alignment found in [Servo Horn Alignment](#servo-horn-alignment).

### Feet
Next up is the feet. The feet are a fairly quick and simple set-up that will require:
 - a M3 hex screwdriver
 - 8x silver servo M3 screws
 - 2x servo horns
 - 2x black rubber spacers from the motor package
 - 2x black M3 screws from the motor package
 - 2x JST cables
 - Motor ID 14
 - Motor ID 17
 
Pre-threading the plastic screw holes with the silver M3 screws before assembly. 
<!--Then attach the servos by aligning them upright to the sky. Add the rubber spacers onto the screw notches that will attach to the lower legs as this will help stabilize our screws in the frame (see figure below). Lastly, attach the JST cables into the space on the back of the servos. The final product should look like the figure below.-->

1. Attach servo horns onto motors 14 and 17 using 2 black M3 screws.
2. Insert motors upright into the Feet.
3. Secure motors with 8 silver M3 screws.
4. Attach JST cables onto back connection points of motors. 

Final product:

<img src="res/Feet_Angled.jpeg"  width="50%"/>
<img src="res/Feet_Top.jpeg"  width="50%"/>

### Lower Legs
Following the set-up of the feet are the lower legs of the robot. Repeat these steps for both the right and left lower legs.

Each lower leg will require:
 - a M3 hex screwdriver
 - Knee Servo Motor
 - 2x black M3 screw from the motor package
 - 4x rubber spacers included in the motor package
 - 2x metal servo horn
 - 8x silver servo horn M3 screws
 - 4x tapered M3 x 18 mm screws
 - 4x M3 hex nuts
 - 2x JST cables
 - Motor ID 16
 - Motor ID 13

As done the same with the feet, pre-thread all the screw holes on the lower legs before beginning assembly. 
<!--Setting the lower legs in place on top of the ankle motors, begin screwing the legs in place using the tapered screws and hex nuts. We are now half-way through the step. The half-way product should look like the second figure below.-->

1. Attach lower legs to motors 14 and 17 using 4 tapered M3 x 18 mm screws.
2. Secure motors with 4 M3 hexagonal nuts.

Reference figures:

<img src="res/LowerLegs_Side.jpeg"  width="50%"/>
<img src="res/LowerLegs_Back.jpeg"  width="50%"/>

<!--Next, attach the Ankle JST cables to the bottom of the Knee motors, and a new JST cable onto the right side of the Left Knee motor. The Right Knee motor will have a new JST cable onto the left side. Finally, orient the Knee motors correctly onto the lower legs which should follow a 90 degree angle (the robot is sitting). Add rubber spacers onto the lower screw notches of the motor, where the upper legs will be attached.The figures below will show the final product, with JST cable, rubber spacer, and Knee motor orientation.--> 

3. Attach Ankle JST cables to bottom of motors 13 and 16, and new JST cables onto the sides. (Right side of motor 16, Left side of motor 13)
4. Orient motors 13 and 16 at ~90 degree angle on lower legs. Attach with 8 silver M3 screws.
5. Add rubber spacers onto upper notches of motors 13 and 16.

Final product:

<img src="res/LowerLegs_Angled.jpeg"  width="50%"/>

### Upper Legs
Continuing now to the upper legs. The upper legs will require:
 - a hex screwdriver for tapered M3 screws
 - 4x tapered M3 x 18 mm screws
 - 4x M3 hex nuts
 
Following the similar process from the other limbs, pre-thread all the screw holes before beginning assembly. 
<!--Next, you can attach the lower end of the upper legs by attaching it to the motors on the upper part of the lower legs (using the tapered screws). Keep in mind that the JST cable for the Knee motors will need to run through the skeleton of the upper leg (see reference below). The final product should resemble the figure below.-->
1. Attach lower end of upper legs to motors 13 and 16 using 4 tapered M3 x 18 mm screws.
2. Secure motors with 4 M3 hexagonal nuts.

Final product, Left Leg:

<img src="res/CompleteLeftLeg_Side.jpeg" width="50%"/>
<img src="res/CompleteLeftLeg_Back.jpeg"  width="50%"/>

Final product, Right Leg:

<img src="res/CompleteRightLeg_Side.jpeg"  width="50%"/>
<img src="res/CompleteRightLeg_Back.jpeg"  width="50%"/>
*Note that the cable path is incorrect in this figure, you should use the JST connection on the other side of the motor that will keep the JST cable from being pinched from ankle movement.*

### Hips
Finally, we reach the end of the Lower Body Assembly. The hips will require:
 - a M3 hex screwdriver
 - 2x metal servo horns
 - 8x silver servo horn M3 screws
 - 2x black M3 screws from the motor package
 - 4x rubber spacers from the motor package
 - 4x M3 x 25 mm hex screws
 - 4x M3 square nuts
 - 2x  extended JST cables
 - Motor ID 12
 - Motor ID 15
 
As usual, pre-thread all the screw holes, **especially**, where the motors are attached to the hips. 

1. Add rubber spacers onto the screw notches of the motor.
2. Place motor 12 on the right side of the hips. Press it down until the screw holes are aligned. See the figures below:

    <img src="res/Hips_Side.jpeg"  width="50%"/>
    <img src="res/RightHip_Back.jpeg"  width="50%"/>
    
4. Use 2 M3 x 25 mm screws to begin securing the motor. Stop screwing the motors to leave space for the square nuts.
5. Insert 2 square nuts into the spaces located on the bottom of the hip. Tilt the piece to align the screws with the square nuts. Then fully screw in the motor.
6. Place motor 15 on the left side. Press it down until the screw holes are aligned. See the figure below:
   
    <img src="res/LeftHip_Back.jpeg"  width="50%"/>

7. Use 2 M3 x 30 mm screws to begin securing the motor. Stop screwing the motors to leave space for the square nuts.
8. Insert 2 square nuts into the spaces located on the bottom of the hip. Tilt the piece to align the screws with the square nuts. Then fully screw in the motor.

<!--Next, add the rubber spacers onto the screw notches of the motor (pictured below) and following comes the trickiest part of the Lower Body Assembly. Place the motors inside their corresponding slots in the hips (following correct orientation) and firmly press them down until you can see the rubber spacer peek out a little underneath. This does not mean you are trying your best to push the motor down so much that you damage material, but pressing it down enough that it stops moving and the screw holes are aligned. You can check this by screwing in one of the M3 x 30 mm screws and seeing if you feel a lot of resistance. There will exist some resistance (due to the spacers), but not enough that it feels like you will snap the hip upon using a hex screwdriver. 

After you have your motors settled with the screw holes aligned, make sure one of the screws is fitted far enough you can see it beginning to reach the square gap but not sitting in it at all (pictured below). Now, flip the 3D printed piece upside down so you are seeing the flat printed bottom. Insert a M3 square nut into one of the rectangular slots and align it with your incoming screw. **This step will take the most adjusting!** Try to continue screwing in the M3 x 25 mm into the piece and seeing if it captures the M3 square nut correctly. If it is meeting a lot of resistance or won't continue screwing, **retry**. Otherwise you might snap some material off. Tip: try tilting the hips at an angle if the M3 square nut is falling through too much, or if a bottom layer exists (usually from the 3D printing process), drop the nut from the top and fit it appropriately in its slot.-->

Following this step you can attach the servo horn onto the motor and JST cables protruding from the **back** connection of the Hip motors. The final product should look like the figure below:

Final product:

   <img src="res/Hips_Angled.jpeg"  width="50%"/>
   <img src="res/Hips_Top.jpeg"  width="50%"/>

After, you can attach the lower limbs to the hip by screwing the Upper Legs into place on the Hips' servo horns (using the silver M3 screws). The final assembly should look like the figures below:

   <img src="res/FullLegAssembly_Front.jpeg"  width="50%"/>

*In this figure, the JST cables connected to the Hips are wired incorrectly. You should use the back JST connection to attach your Hip cables. Also, your robot should only have the leg portion in this photo, ignore the additional components.*

## Neck and Torso Assembly
When assembling the neck and torso for the robot, it is best to begin with the chest, then spine, and ending with the neck. Throughout this assembly you will need to attach the motors and JST cables onto certain pieces before moving on.

The first step that is **highly** recommended is pre-setting the IDs of all of the Neck and Torso motors before beginning the assembly. 

The HiWonder HTS-20H servos involved in this assembly would be: 
 - Right Chest motor
 - Left Chest motor
 - Head Nod motor
 - Head Tilt motor
 - Head Turn motor 

The two HiWonder HTS-35H servo are also part of this section of the assembly, and are used for the torso motors.
 - Torso Bow motor
 - Torso Tilt motor
 
All correlated motor IDs are listed above in [Initializing Servo IDs and Positions](#initializing-servo-ids-and-positions), as well as instructions for how to set the IDs and their home positions. It is also recommended that you check the servo horn orientation during this time, following the alignment found in [Servo Horn Alignment](#servo-horn-alignment).

### Chest Assembly
The chest will require:
 - A P1 philips screwdriver
 - A M2.5 allen key
 - 12x black rubber spacers from the motor package
 - 12x silver servo horn M3 screws
 - 3x JST cables
 - 12x M3 x 16 mm hex screws
 - 8x M3 hex nuts
 - 4x M3 square nuts
 - Motor ID 4
 - Motor ID 8
 - the Shoulder Connector pieces
 - the Chest piece

As recommended in the assembly notes, it is best to pre-thread the screw holes on the 3D printed parts. You should also have already Initialized the motor IDs and home positions with attached servo horns as described in the [initialization instructions](#initializing-servo-ids-and-positions)

Right Shoulder Chest
1. Insert the black rubber spacers into the screw slots for each of motor 4.
2. Insert motor 4 into the right shoulder slot on the chest piece. The servo should be oriented so the servo horn is closer to the back of the chest rather than the front as seen in the side photo below. Note the location of the dimple on the servo horn.

   <img src="res/Chest_Side.jpeg"  width="50%"/>
   
3. Use 4 of the M3x16 screws and 4 of the hex nuts to screw motor 4 to the chest.
4. Use 4 of the silver M3 screws to attach motor 4's servo horn to the righst side Shoulder Connector piece. It should be attached to the horn mount in the middle of the part, and the two sides of the part should be dipping "down" when attached as shown below. 

   <img src="res/Chest_RShoulderConnector_Side.jpeg"  width="50%"/>
   
5. Attach the JST cable to the jst connector on the motor facing the back of the chest piece.

Left Shoulder Chest

6. Insert the black rubber spacers into the screw slots for each of motor 8
7. Insert motor 8 into the left shoulder slot on the chest piece. The servo should be oriented so the servo horn is closer to the back of the chest rather than the front.

   <img src="res/Chest_LSide.jpeg"  width="50%"/>

8. Use 4 of the M3x16 screws and 4 of the M3 hex nuts to screw motor 8 to the chest.
9. Use 4 of the silver M3 screws to attach motor 4's servo horn to the right side Shoulder Connector piece. It should be attached to the horn mount in the middle of the part, and the two sides of the part should be dipping "down" when attached as shown below.

   <img src="res/Chest_LShoulderConnectors_Side.jpeg"  width="50%"/>
   
10. Attach the JST cable to the JST connector on the motor facing the back of the chest piece.

With both motors installed and JST cables connected, the chest from behind should look like 

   <img src="res/Chest_ShoulderConnectors_Front.jpeg"  width="50%"/>
   <img src="res/Chest_ChestConnector_Back.jpeg"  width="50%"/> 

<!--The chest assembly will be fairly simple as you’ll be attaching the Right Chest, Left Chest, and Neck motors, then at the end, adding the Chest Connector piece that you just put together. The most difficult part of this assembly will be adding the Chest Connector piece onto the Chest.

For the Right and Left Chest motors add the black rubber spacers to all screw notches available, then attach them to their respective sides with the servo horn pins pointing away from the front of the chest. Next, use the M3 x 14 mm hex screws and hex nuts to attach the motors to the chest frame. After the motors have been attached, you can add JST cables to the connection points located on the back of the chest frame. The progress so far should look like the figures below:

<img src="res/Chest_Back.jpeg"  width="50%"/>
<img src="res/Chest_Side.jpeg"  width="50%"/>

Now, you can add the motors’ servo horns with the black M3 screws, then the Shoulder Connector pieces. You’ll want the orientation of the Shoulder Connector pieces to match the placement of the Chest motors. You can attach the Shoulder Connector pieces using the silver M3 screws. The final product should look like the figures below:

<img src="res/Chest_ShoulderConnectors_Front.jpeg"  width="50%"/>
<img src="res/Chest_ShoulderConnectors_Side.jpeg"  width="50%"/>-->

### Chest Connector Assembly
The Chest Connector assembly will require:
 - a M3 hex screwdriver
 - 8x rubber spacers from the motor packages
 - 2x black M3 screws from the motor packages
 - 8x square M3 nuts
 - 8x M3 x 16 mm hex screws
 - 2x servo horns
 - 8x servo horn M3 screws
 - 2x JST cables
 - Motor ID 19
 - Motor ID 18
 
As recommended with every step, it is best to pre-thread the screw holes on the 3D printed parts.

Chest Bow

1. Insert the black rubber spacers into all four of the screw slots on motor 19

   <img src="res/Connectors_SidebySide.jpeg"  width="50%"/>
**Use the connector on the right for Chest Assembly.**

2. Insert motor 19 into the slot that will *not* have another motor behind it. Make sure the servo horn and shaft are aligned to the plastic pin on the opposite side as shown in the image below.

   <img src="res/ChestConnector_1Motor_Top.jpeg"  width="50%"/> 
   
3. Insert four of the M3 square nuts into the square nut slots around the motor and screw them down using the M3 x 16 mm screws.

Chest tilt

4. Insert the black rubber spacers into all four of the screw slots on motor 18
5. Insert motor 18 into the remaining motor slot, making sure the servo horn and shaft are aligned to the plastic pin on the opposite side as shown below.

   <img src="res/ChestConnector_2Motors_Top.jpeg"  width="50%"/> 
   
6. Insert four of the M3 square nuts into the square nut slots around the motor and screw them down using the M3 x 16 mm screws.

Attaching to the Chest

7. Begin by slotting motor 18 into the chest upside down, with the servo horn facing the front plate, as shown below. *Do not screw in the servo horn yet.*

   <img src="res/Chest_ChestConnector_Angled.jpeg"  width="50%"/>
   <img src="res/Chest_ChestConnector_Front1.jpeg"  width="50%"/>
   
8. Rotate the chest connector assembly until it is right side up inside the chest, as shown below.

   <img src="res/Chest_ChestConnector_Front2.jpeg"  width="50%"/>
   
9. Attach the servo horn to the chest using four of the silver M3 motor screws.


<!--Begin by attaching the Chest Connector motors in the connector piece. Be aware of where you place certain motors as you’ll want your ID to match the movement that it will make on the robot. For example, Motor #18 will make a side-to-side movement while Motor #19 will be in charge of the up-down movement. 

The placement of these motors can be a little tricky, so a visual will be provided below to help orient them correctly along with the JST connections. A good rule of thumb for this connector piece is to have the motor shaft in-line with the pins located on the 3D printed piece. The figures below shows correct placement and JST cable paths:

<img src="res/ChestConnector_Angled.jpeg" width="50%"/>
<img src="res/ChestConnector_Angled2.jpeg" width="50%"/>
<img src="res/ChestConnector_Bottom.jpeg" width="50%"/>

Now, add all the rubber spacers onto the screw notches of the motors and begin adding the screws until you barely reach the M3 square nut opening. Place the M3 square nuts in their corresponding spaces and continue tightening the screws completely. You might have to tilt the 3D printed piece a bit to keep the square nuts in their place.

After finishing the connector piece you can attach the servo horns using the black M3 screws. These servo horns will attach the piece to both the spine and the chest piece. Now begins the tricky part, attaching the Chest Connector to the chest piece.

To make this as simple as possible, begin by attaching the front motor (the one that will attach to the chest piece) first. You will want to attach this upside down to its placement, then rotate it into its correct position after fitting the Chest Connector in correctly. A correct placement means that both the servo horn and the pin (on the back of the chest piece) are both slotted into their designed positions. The figures below show the assembly process and final product:

<img src="res/Chest_ChestConnector_Angled.jpeg"  width="50%"/>
<img src="res/Chest_ChestConnector_Front1.jpeg"  width="50%"/>
<img src="res/Chest_ChestConnector_Front2.jpeg"  width="50%"/>-->

### Spine Assembly
The Spine assembly will require:
 - a M3 hex screwdriver
 - 4x silver servo horn M3 screws from the motor package
 - 8x hex nuts
 - 8x M3 x 14 mm hex screws

As recommended with every step, it is best to pre-thread the screw holes on the 3D printed parts.

<!--To begin assembling, attach the frame of the spine to the hips. It is important that you attach the spine by the screw attachments that don’t include the servo horn location. It is also recommended that you screw in the spine with four screws in a diamond shape (the only screw holes that M3 screws will fit). This will give you a stable base for you to attach the rest of the torso on. This step should not impede instructions provided later for the Lower Body Assembly.-->

1. Attach bottom frame of spine to hips using 4 M3 x 14 mm screws and 4 hex nuts. Screw in diamond shape.

The figure below shows screw placement:

   <img src="res/Spine_Front.jpeg"  width="50%"/>
   <img src="res/Spine_Back.jpeg"  width="50%"/>

Following the attachment to the hips is attaching the Chest Assembly to the Spine. 
<!--There should be a servo horn left on the Chest Connector that is orientated in the same direction as the available horn slot on the Spine. Attach the Chest to the Spine using this connection point with the silver M3 screws.-->
The final product should look like the figures below:

2. Slot the spine over motor 19, with the servo horn over the bulge, and the flat plane of the spine aligned with the back of the chest piece. The figure below is only meant to show correct orientation.

   <img src="res/Spine_ChestConnector_Top.jpeg" width="50%"/>
   
3. Screw in motor 19 by attaching four silver M3 motor screws to the servo horn through the holes in the spine.

Final product: 

   <img src="res/Spine_Chest_Angled.jpeg"  width="50%"/>
   <img src="res/Spine_Chest_Front.jpeg"  width="50%"/>
   <img src="res/Spine_Chest_Angled2.jpeg"  width="50%"/>

### Neck Assembly
The neck will require:
 - a M3 hex screwdriver
 - 1 servo horn
 - 1 black M3 screw from the motor package
 - 4x black rubber spacers from the motor package
 - 4x silver servo horn M3 screws
 - 1 JST cable
 - 4x M3 x 16 mm hex screws
 - 4x M3 square nuts
 - Motor ID 3

As recommended with every step, it is best to pre-thread the screw holes on the 3D printed parts.

<!--First, add the black rubber spacers to all screw notches of the Neck motor. Next, you’ll want to add 4 square nuts to the spaces available on the empty motor space on the top of the chest piece. Using the M3 x 16 mm screws, attach the Neck motor. Next, add a servo horn using the silver M3 screws to the placement located on the bottom of the Neck piece. It will be easier to add the servo horn to the piece first than attaching it to the motor. After attaching the servo horn onto the Neck piece, you can add the Neck piece onto the Neck motor and secure it with a black M3 screw.

At this step you can also add a JST Cable to the port opening located on the back of the chest frame. The final product should look like the figures below:-->
1. Insert the black rubber spacers into the screw slots for each of motor 3
2. Insert 2 of the M3 square nuts into the slots in on the inside of the neck of the chest piece, as shown below.

    <img src="res/Neck_Noscrews_Top.jpeg"  width="50%"/>
    
3. Insert motor 3 into the neck of the chest piece. The servo should be oriented so the servo horn is closer to the back of the chest rather than the front.
4. Insert the remaining 2 M3 square nuts into the slots on the back of the neck of the chest piece.
5. Use the remaining 4 M3x16 hex screws to screw down motor 3 to the chest, making sure to screw into the square nuts.
   
   <img src="res/Neck_Side.jpeg"  width="50%"/>
   <img src="res/Neck_Top.jpeg"  width="50%"/>

6. Attach the neck piece to the servo horn with 4 silver M3 screws, matching the orientation shown below.

   <img src="res/NeckPiece_Front.jpeg"  width="50%"/>
   <img src="res/NeckPiece_Side.jpeg"  width="50%"/>
    
7. Attach the JST cable to the jst connector on the motor facing the back of the chest piece.

### Neck Connector Assembly
The Neck Connector will require:
 - a M3 hex screwdriver
 - 2x servo horns
 - 8x servo horn M3 screws
 - 2x black M3 screws from the motor packages
 - 8x black rubber spacers from the motor packages
 - 3x JST cables
 - 8x M3 x 16 mm hex screws
 - 8x square nuts
 - Motor ID 2
 - Motor ID 1

As recommended with every step, it is best to pre-thread the screw holes on the 3D printed parts.

<!--Begin by adding the rubber spacers to all screw notches on your Neck Connector motors, then you can begin attaching the motors in the connector piece using the M3 x 16 mm screws. Be aware of where you place certain motors as you’ll want your ID to match the movement that it will make on the robot. For example, Motor #1 will make a side-to-side movement while Motor #2 will be in charge of the up-down movement. After adding the motors you can attach their servo horns using the black M3 screws.

The placement of these motors can be a little tricky, so a visual will be provided below to help orient them correctly along with the JST connections. A good rule of thumb for this connector piece is to have the motor shaft in-line with the pins located on the 3D printed piece. The figures below shows correct orientation and JST cable paths:-->

Neck Bow

1. Insert the black rubber spacers into all four of the screw slots on motor 2

   <img src="res/Connectors_SidebySide.jpeg"  width="50%"/>
**Use the connector on the left for Neck Assembly.**

2. Insert motor 2 into the slot that will *not* have another motor behind it. Make sure the servo horn and shaft are aligned to the plastic pin on the opposite side as shown in the image below.

   <img src="res/NeckConnector_1Motor_Top.jpeg" width="50%"/>
   
3. Insert four of the M3 square nuts into the square nut slots around the motor and screw them down using the M3 x 16 mm screws.
4. Attach a JST cable to bottom connection point of motor 2.

Neck Tilt

5. Insert the black rubber spacers into all four of the screw slots on motor 1
6. Insert motor 1 into the remaining motor slot, making sure the servo horn and shaft are aligned to the plastic pin on the opposite side as shown below.

   <img src="res/NeckConnector_2Motor_Top.jpeg" width="50%"/>
   
7. Insert four of the M3 square nuts into the square nut slots around the motor and screw them down using the M3 x 16 mm screws.
8. Attach JST cable from motor 2 to top connection point of motor 1.
9. Attach additional JST cables to both sides of motor 1.

<!--<img src="res/NeckConnector_Top.jpeg"  width="50%"/>
<img src="res/NeckConnector_Side.jpeg"  width="50%"/>
<img src="res/NeckConnector_Angled.jpeg"  width="50%"/>-->

### Head Assembly
The Head Assembly will require:
 - a M3 hex screwdriver
 - 8x silver servo horn M3 screws from the motor package
 - 2x M3 x 20 mm screws
 - 2x M3 square nuts 

As recommended with every step, it is best to pre-thread the screw holes on the 3D printed parts.

<!--You will first want to attach the Neck Connector piece to the Neck piece that should be attached to the Chest piece at this point. Motor #1 should be attached to the servo horn placement on the Neck piece, and secured with the silver M3 screws. Next, you’ll want to use the piece that looks like U (this piece will help us attach the headshell later) and attach it to Motor #2 located on the Neck Connector piece.--> 
1. Attach Neck Connector to motor 1 and secure with 4 silver M3 screws. Follow images below for correct orientation.
2. Attach U-shaped piece to motor 2 using 4 silver M3 screws.

   <img src="res/Neck_NeckConnector_Side.jpeg"  width="50%"/>
   <img src="res/Neck_NeckConnector_Front.jpeg"  width="50%"/>

<!--Next, insert the square nuts into the square slots on the U-shaped piece. Be sure to use a tool to push them as far in as they can go. You can check if they are in the right place by peering through the screw hole to see if the holes line up. See the figure below for a clearer visual (at this step the LED panel can be added, but optional):-->
3. Insert 2 square nuts into the slots on U-shaped piece. Use a small tool to push them as far in as they can go. LED panel can also be added at this step (press-fit attachment).

   <img src="res/Neck_NeckConnector_Side2.jpeg"  width="50%"/>

<!--After, you can place the headshell on top of this U-shaped piece by aligning the cylinder extrusions of the headshell with the cylinder-shaped gaps on the U piece. The two should fit snug and you should be able to press the headshell down to secure the fit. You can then complete the headshell’s attachment by screwing in the M3 x 20 mm screws until they reach past the square nuts. The final product should look like the figures below:-->
4. Place headshell on top of U-shaped piece by aligning cylinder shaped press-fits.
5. Secure in headshell with 2 M3 x 20 mm screws.

   <img src="res/Headshell_Side.jpeg"  width="50%"/>
   <img src="res/Headshell_Top.jpeg"  width="50%"/>

## Arm Assembly
When assembling the arms for the robot, it is best to begin with the bicep, then shoulder, and ending with the forearms. This is due to the slight complexity behind the arm assembly. You will need to attach the motors and JST cables onto certain pieces before moving on.

The first step that is **highly** recommended is pre-setting all of the Arm motors before beginning the assembly. 

The HiWonder HTS-20H servos involved in this assembly would be:  
- Right Shoulder
- Right Bicep
- Right Elbow
- Left Shoulder
- Left Bicep
- Left Elbow 

The forearms will require one Actuonix PQ12 Micro Linear Actuator each. 

All correlated motor IDs are listed above in [Initializing Servo IDs and Positions](#initializing-servo-ids-and-positions), as well as instructions for how to set the IDs and their home positions. It is also recommended that you check the servo horn orientation during this time, following the alignment found here [Servo Horn Alignment](#servo-horn-alignment).

### Biceps
The biceps will require:
 - a M3 hex screwdriver
 - 2x servo horns
 - 2x black M3 screws from the motor package
 - 4x black rubber spacers from the motor package
 - 4x JST cables
 - 4x M3 x 18 mm tapered screws
 - 4x M3 x 25 mm hex screws
 - 4x M3 square nuts
 - 4x M3 hex nuts
 - Motor ID 10
 - Motor ID 6
 - Motor ID 7
 - Motor ID 11
 
As recommended with every step within the assembly, it is best to pre-thread the screw holes on the 3D printed parts.

<!--Beginning with the top motor placement on the bicep, attach 2 JST cables onto the back and right side of the Right Bicep motor (switching the right side to left for the Left Bicep motor). After completing this step, add the square nuts to their corresponding spaces on the inside of the Biceps. If you look at the screw hole from a top view, you shouldn’t be able to see the M3 square nuts. If you can, this means that the screw holes from the Bicep pieces and the nuts are not aligned correctly. After aligning the nuts correctly, place the motors into the top motor space which should give you a prescribed alignment. Screw the motors in place using the M3 x 25 mm screws. The placement should mimic the figure below:-->
1. Attach 2 JST cables onto the back and right side of motor 10, and 2 cables onto the back and left side of motor 6.
2. Insert 4 square nuts into the slots located on the inside of the Biceps. Align them so you can't see them from the top.
3. Insert motors 10 and 6 into the Bicep pieces, secure them with 4 M3 x 25 mm screws.

Bicep references with JST cables:

<img src="res/Biceps_Back.jpeg"  width="50%"/>
<img src="res/Biceps_Top.jpeg"  width="50%"/>

<!--Next, add 2 rubber spacers to the screw holes opposite to where the servo attaches on the lower Bicep motors. Then, attach the lower Bicep motors to the lower motor placement available using the tapered M3 x 18 mm screws with their servo horns already included (using the black M3 screws). The motors should be aligned where the screw holes with the rubber spacers match up with the screw holes on the 3D printed piece. The end result should allow for the servo horn of the lower Bicep motors to be attached to the Forearms. Lastly, connect the JST cables located on the right or left side of the upper Bicep motors to the back available connection of the lower Bicep motors. The figures below will include highlighted JST cable paths.
The final products should look like the figure below:-->

4. Add 4 rubber spacers onto the top screw notches of motors 7 and 11.
5. Attach the motors onto the lower placement of the Bicep pieces using 4 M3 x 18 mm tapered screws. Secure them with 4 M3 hex nuts.
6. Connect the side JST cables of the upper motors to the back connection of the lower motors.

Final products (Right motor and Left motor):

<img src="res/CompleteBiceps_Front.jpeg"  width="50%"/>
<img src="res/CompleteBiceps_Side.jpeg"  width="50%"/>

### Shoulders
The Shoulders will require:
 - a M3 hex screwdriver
 - 8x silver servo horn M3 screws
 - 2x black M3 screws from the motor package
 - 4x black rubber spacers from the motor package
 - 4x JST cables
 - 4x servo horns
 - 4x M3 x 16 mm hex screws
 - 4x M3 square nuts
 - Motor ID 4
 - Motor ID 9
 
As recommended with every step, it is best to pre-thread all screw holes. This is especially important for the Shoulders due to the uniqueness of its screw placements. 

<!--Before placing the Shoulder motors in the 3D printed piece, attach servo horns on the bottom of the 3D piece using the silver M3 screws. This will be the servo horns meant to connect to the upper motors of the Bicep assembly that you just completed. Make sure to align the horns correctly according to the upper Bicep motors. To make this step easier, feel free to attach the servo horns onto the upper Bicep motors, **don’t screw them down yet**. Then, screw the Shoulder piece onto the horn. The outcome should look like the figure below:-->

1. Attach servo horns using 8 silver M3 screws onto the bottoms of the Shoulder pieces. Point the servo horn dimple toward the front of the piece.

Outcome of servo horn attachment:

   <img src="res/Shoulder_Screw_Top.jpeg"  width="50%"/>
   <img src="res/Bicep_Shoulder_Front.jpeg"  width="50%"/>

<!--Next, add rubber spacers to the screw holes closest to the servo horn attachment on the Shoulder motors. Put the Shoulder motors into the 3D printed piece with the label facing outward and the servo horn attachment orientated on the top. You can then screw the motors in place using the M3 x 14 mm hex screws and adding the M3 square nuts into their corresponding slots. It might take a bit of fussing to get the M3 square nuts aligned correctly with the screws. You can tilt the piece to help make this a bit easier.--> 

2. Add 4 rubber spacers onto motors 5 and 9, only on the top screw notches.
3. Insert motors 5 and 9 into the shoulders, screw them in place using 4 M3 x 14 mm hex screws and 4 M3 square nuts.

<!--After screwing the motor in place, you can screw on the servo horns and attach the JST cables (connected to the back of the upper Bicep motors) to the outer sides of the Shoulder motors. Right side for the Right Shoulder, and left side for the Left Shoulder. Additionally, attach JST cables to the inside of the Shoulder motors, which will later connect to the upper Chest motors. The figures below will include highlighted JST cable paths.-->

4. Attach servo horns and JST cables from the back of the upper Bicep motors to the outer sides of the Shoulder motors. Right side for Right Shoulder, Left side for Left Shoulder.
5. Attach 2 more JST cables to the inside of the Shoulder motors.

Final product:

   <img src="res/LRShoulder_Bicep_Front.jpeg"  width="50%"/>
   <img src="res/LRShoulder_Bicep_Back.jpeg"  width="50%"/>

### Forearms
The Forearms will require:
 - a M3 hex screwdriver
 - 8x silver M3 screws

Pre-thread all screw holes before assembly.

1. Attach Forearms to respective Biceps using 4 silver M3 screws each.

Final assembly (ignore color differences, pieces were printed incorrectly):

   <img src="res/LRArmAssembly_Side.jpeg"  width="50%"/>

### Hands Construction & Assembly
Before beginning assembly, please be sure to double check that the hinges match the size-dependent and axial orientation on the fingers, with the fingers aligned to their corresponding palm (*Figures 1-3*). This assembly will require:
 - TPU finger hinges
 - Resin printed fingers
 - 0.38 mm (0.015 in) fishing line
 - 4 2.5 mm self-tapping screws (from the motor package)
 - pair of thin nose pliers
 - scissors
 - small files
 - 2 Actuonix PQ12 Micro Linear Actuators
 - 2 U-shaped metal pieces (from linear actuator box)
 - 2 M3 x 12 mm screws
 - 2 lock nuts
 - 2 square-shaped nuts
 - 2 eyebolts
 - 2 M3 small screws (from linear actuator box)
 - 2 M3 medium length screws (from linear actuator box)

<!--It is **highly** recommended to fit the largest hinges into the palm first. While the hinges should be printed as a more "spongey" material, you may need to use a pair of pliers to manually squeeze the larger side of the hinge into its gap in the palm. You can also use a file or a craft knife to trim a little from the opening sides. After fitting the palm hinges, all fingers can be assembled separately from the hand. They should perfectly slide into the finger hinge slots (following size contraints but axial orientation shouldn't matter).--> 
<!--Stringing the fishing line through the hands should be the **last step** (with fingers not yet assembled to the palm). Begin by measuring the amount you think you might need for your project by fitting the line through the bottom of the hand and up through the 3D piece (**do not cut yet**). Then, continue stringing your fishing line up the holes in the fingers and upon reaching the tip of the top finger, restring back through the second hole and leaving enough to tie it off (*Figure 4*). To get an accurate length of fishing line you will need, attach the finger to the palm and measure how much you think you will need at the bottom of the hand (leaving adequate space at the top to tie off your line). After ensuring you have the right length, you can cut off your line from its container and use pliers to tie a double knot at the top of the finger.-->

1. Fit the largest hinges into the 4 largest slots on the palm using the side with the hole in it. The material is "spongey", you can use pair of pliers to push it in. If necessary, shave the area use a small file or craft night.
2. Fit two small hinges into the thumb slot using the same process mentioned in step 1. If necessary, shave the area use a small file or craft night.
3. Slide first finger hinges in place following size constraints and hand orientation.
4. Repeat process using smaller hinges and finger components, referencing the figures below as needed.
5. Cut ~30 mm of fishing line per finger, ~25 mm for the thumb.
6. Fit fishing line through the bottom of the heand up through one set of finger components.
7. Restring fishing line back through the top finger component. Leave enough room to tie off later.
8. Ensure that the length is adequate enough to later attach to the forearm. If so, tie off the top of the finger using pliers to get a tight knot (may need to make more than one knot). Use Figure 4 as a reference.

<img src="res/Finger_Hand_Reference_Sheet.jpg"  width="50%"/>

*Figure 1*: Composition and BOM of Flexy-Hand 2 ([Flexy-Hand 2](https://www.thingiverse.com/thing:380665))


<img src="res/Finger_Plate_Layout_display_large.jpg"  width="50%"/>

*Figure 2*: Finger plate with labeled orientation ([Flexy-Hand 2](https://www.thingiverse.com/thing:380665))


<img src="res/Base_Hinge_Orientation_display_large.jpg" width="50%"/>

*Figure 3*: Hinge orientation for all fingers ([Flexy-Hand 2](https://www.thingiverse.com/thing:380665))


<img src="res/Tendon_Tieoff_at_Base_of_Fingertip_display_large.jpg"  width="50%"/>

*Figure 4*: Tendon knot placement for all fingers ([Flexy-Hand 2](https://www.thingiverse.com/thing:380665))

<img src="res/Fishermans-knot-all-steps.jpg"  width="50%"/>

*Figure 5*: Fisherman's Knot instructional image

#### Continued...
9. Set up linear actuators to board and move them to max length before assembly. Follow Arduino code provided in [LinearActuatorSet](../Arduino/LinearActuatorSet/).

   <img src="res/ArduinoCircuit_Front.jpeg"  width="50%"/>

10. Attach eyebolts to middle screw hole of U-shaped metal piece using the smallest M3 screws from the linear actuator package.

   <img src="res/Eyebolt_Top.jpeg"  width="50%"/>

11. Attach linear actuators to Forearm piece using M3 x 12 mm screws and square nuts (see Final product reference).
12. Tie all 5 fishing lines to eyebolt using a 'Fisherman's Knot'. Use Figure 5 as a reference.

   <img src="res/Hand_Eyebolt_Top.jpeg"  width="50%"/>

12. Attach hands to the forearms using the 2.5 mm self-tapping screws.
13. Attach other 2 screw holes of U-shaped metal piece to linear actuator using the medium length M3 screws and lock nuts. *Note: This image is only meant to show how linear actuator and hand should be attached. Only attach the two once the linear actuator is screwed into the forearm.*

   <img src="res/EyeboltKnot_Side.jpeg"  width="50%"/>

Final product (Right Arm):

   <img src="res/CompleteForearm_Top.jpeg"  width="50%"/>
   <img src="res/CompleteForearm_Bottom.jpeg"  width="50%"/>


## Chair Modification and Assembly

The Ikea chair needs to be modified with screw and bolt holes to attach the robot, control PCB, two power supplies, and power switch.

Begin by first assembling the Ikea chair following their instructions.

### Power Switch

Requires:

 - Ikea chair
 - [Power switch]() and [fuse]()
 - M3x30 flathead screw x2 (Power switch screws)
 - M3 lock nut x2 (Power switch mounting)
 - [Power switch mounting template](res/chair_templates1.pdf)

1. Lay out the Power switch mounting template on the back of the plane of the chair below the seat.
2. Cut out the box in the dashed line, then fit the power switch into the cut out on the chair.

   <img src="res/power_switch_mounted.jpg" width="50%"/>

3. Drill holes through the wood using the screw holes in the switch as your location template.
4. Screw the two M3x30 flathead screws through the power switch holes and holes your drilled in chair
5. Lock down in place by tightening down the M3 lock nuts onto the end of the screws on the other side of the wood.


### 12V Supply Mounting

Requires:

 - Ikea chair
 - 12VDC Power Supply
 - M4x30 socket head screw x2 (12V to leg of chair)
 - [12V screw hole template](res/chair_templates1.pdf)

1. Lay out the 12V supply mounting template on the back leg of the chair, as shown in the image below.

   <img src="res/12v_supply_template_mount.jpg" width="50%"/>

2. Drill through the leg at the two marked holes with a bit sized for M4 screws.
3. Take a larger size drill bit, larger than the head of the socket head M4 screws and drill through from the outside just deep enough that the top of the M4 socket head would be flush with the chair.
4. Screw the M4 screws through the holes, and into the matching holes on the side of the 12V power supply, matching the orientation shown in the images below.

   <img src="res/12v_behind.jpg" width="45%"/> <img src="res/12v_front.jpg" width="45%"/>


### 5V Supply Mounting

Requires:

 - Ikea chair
 - 5VDC Power Supply
 - M3x20 screw x2 (Side of chair for 5V)
 - M3x14 screw x2 (Bottom of chair for 5V)
 - [5V screw hole template](res/chair_templates1.pdf)

1. Fold the 5V supply mounting template along the center align.
2. Attach the template to the inside underside of the chair, as shown below.

   <img src="res/5v_supply_template_mount.jpg" width="50%"/>

3. Drill through the marked holes with a bit sized for M3 screws.
4. On the outside side of the chair and on top of the seat, drill part way in with a larger size drill bit to countersink the socket cap screw heads flush with the chair surface.
5. Screw the M3x20 screws through the holes in the side and into the matching holes on the back of the 5V supply, matching the orientation shown in the image below.

   <img src="" width="50%"/>

6. Screw the M3x14 screws through the holes in the seat of the chair and into the matching holes on the side of the 5V supply.


### Motor Control PCB Mounting

Requires:

 - Ikea chair
 - Motor control PCB assembly
 - M3x??+6 standoffs x4
 - [PCB mounting template]()


### Robot Mounting

Requires:

 - Ikea chair
 - SAMI Robot
 - M10x40 screw x2 (Robot attach to chair)
 - M10 washer x2
 - M10 lock nut x2
 - [Robot attachment template]()



## Final Assembly


### Eyes Assembly

Assembly of the eyes requires:

 - 8x8 NeoPixel array x2
 - Eye Panel 3D printed piece
 - M2.5 screws and nuts for eye panel
 - Short 3-pin JST cable
 - Long 3-pin JST cable

1. Take the first LED array and screw it into the flat side of the eye panel 3D printed piece, with the jst connectors pushed through the rectangular holes, and the DOUT labeled pin aligned to the rectangular hole closer to the center of the panel.
2. Screw the second LED array and screw it to the eye panel next to the first, with the DIN labeled data pin aligned closer to the center of the panel.
3. Attach the short 3-pin JST cable from the center-aligned DOUT connector of the first LED array to the center-aligned DIN connector of the second LED array.

   <img src="res/back_of_eyepanel_wires.jpg" width="50%"/>

4. Attach the long 3-pin JST cable to the DIN connector of the first LED array.


### Connect The Remaining Cables

For the two motors in the hips, the JST cables that come with the motors will need to be lengthened to reach the motor pcb. You'll need to splice in a 12" length of wire. This can be done by soldering, or with mechanical splice connectors such as [these](https://www.amazon.com/dp/B0DGLJJRZ5).


### Flash Arduino Code

1. Install FastLED from the Arduino Library Manager (version 3.9.12)
2. Install the [NeoEyes library](../Arduino/NeoEyes/) to your Arduino Library.
3. Flash the [SAMIMovementControl](../Arduino/SAMIMovementControl/) project to the Arduino MEGA2560 attached to the motor control board.

### Test Motor movements

Test movements for the motors using the software UI


