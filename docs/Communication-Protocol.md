---
layout: default
id: comm-protocol
title: Serial Communication Packet Architecture
sidebar_label: Communication Protocol
previous_page: behavior-guide
next_page: angle-ranges
---
# Serial Communication Packet Architecture
Each serial packet sent or recieved includes static starting and ending bytes to denote when a packet is complete, and the content between these bytes is our message.
 - Packet start byte char: <
 - Packet end byte char: >

Each message begins with a message topic, which is a single char byte defining the type and structure of content the rest of the message will include. The robot uses one set of message topics, and the sensor box uses a different set of message topics.

The list of existing robot message topics is:
 - J - [Joint Message](#joint-message)
 - E - [Emote Message](#emote-message)
 - P - [Power Message](#power-message)

The list of existing sensor box message topics is:
 - B - [Button Message](#button-message)


These existing message types, corresponding message topics, and remaining content structure are each presented individually below.

#### Joint Message
Joint messages are defined with the message topic byte 'J', followed by the time it should take for the joints to reach the requested position (in seconds) followed then by a list of paired bytes that denote the joint servo id, and the angle

So, a message telling two servos, with ids 1 and 5 to go to 90 degrees in 2 seconds would be 8 bytes and look like:
```
<J2190590>
```

The maximum length of a joint message, if you set all motors, would be:
```
   start byte + message type + time + (jointID * number of motors) + (jointID * number of motors) + stop byte
```

For the standard system, which has 21 motors, this would be 46 bytes maximum.

#### Emote Message
Emote messages are defined with the message topic byte 'E', followed by the id for the emote they want to display, as ordered by the NeoEyes library.

So neutral expression would be 4 bytes and look like: ```<E0>```

#### Power Message
Power messages tell us whether to turn the relays on or off, and which relays. We can also send back power messages to the PC if the Arduino automatically cuts a relay because of a motor going over temperature.

Power messages are defined with the message topic byte 'P', followed by a 1 (on) or 0 (off), and which relays to turn on. The relay markers are:
 - T - Neck and torso motor control
 - A - Arms motor control
 - L - Legs motor control
 - E - Everything, aka all of the relays.

The power message is 5, 6, or 7 bytes. A message saying to turn on power to the neck and torso would look like:
```
<P1T>
```

If you wanted to turn off all relays, you could do so either by sending 'E': 
```
<P0E>
```

Or by sending 'TAL' (order invariant, so TLA, ATL, ALT, LTA, or LAT are all acceptable options).
```
<P0TAL>
```

#### Button Message
Button messages send a single integer value corresponding the 0, 1, or 2, which in turn are the first, second, or third button on the sensor box being pressed, beginning from the left hand side when facing towards the front of the box.

