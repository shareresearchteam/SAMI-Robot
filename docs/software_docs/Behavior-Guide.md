---
layout: default
id: behavior-guide
title: Guide to Custom Robot Behaviors
sidebar_label: Behavior Guide
previous_page: software-architecture
next_page: comm-protocol
---
# Guide to Custom Robot Behaviors
Reuseable behaviors can be designed for use with the robot, and several premade ones have been provided [here](../../software/behaviors/). These behaviors are written as .json files, and the parameters and options are described below.

Each behavior requires a name, as well as a series of keyframes. The name provides an easy way to reference it, and is used for calling behaviors when designing [interactions]().

The keyframes are run sequentially, following the information provided in each keyframe. They can be thought of as similar to animation keyframes.

## Keyframes
Each keyframe can (but is not required to) include an expression for the eyes, a new set of joint positions, as well as the ability to play audio. Additionally, each keyframe can include a waittime, which is how long to delay before sending the next keyframe. The specific keys and their values used in each keyframe are shown in the table below.

**NOTE:** The first keyframe in a behavior will by default set any unspecified joints to their home angle. It will not do this for subsequent keyframes.

**NOTE:** The wait time has no safety protections, so if you repeatedly send joints in quick succession you could damage the motors.

| Key Name      | Type    | Default | Notes                                                          |
| ------------- | ------- | ------- | -------------------------------------------------------------- |
| Expression    | String  | ""      | See specifics [here](#emotes).                                 |
| WaitTime      | Integer | 1000    | Time in milliseconds to wait before sending the next keyframe. |
| JointMoveTime | Integer | 10      | See specifics [here](#joint-pose).                             |
| JointAngles   | Array   | None    | See specifics [here](#joint-pose).                             |
| AudioClip     | Object  | None    | See specifics [here](#audio-groups).                           |

### Emotes
The different pre-built eye expressions are called Emotes. Within each keyframe, an emote can be assigned by providing the keyword "Expression" with a string value matching one of the pre-built emotes. The available emotes are listed below, which maps to the [emote configuration information](./Software.md) and the inbuilt behaviors in the [NeoEyes Arduino library](../../Arduino/NeoEyes/).

| Emote       | ID | Appearance                                               |
| ----------- | -- | -------------------------------------------------------- |
| Off         | 0  | <img src="../res/emotes/Off.jpeg" width="30%"/>          |
| Neutral     | 1  | <img src="../res/emotes/Neutral.jpeg" width="30%"/>      |
| Happy       | 2  | <img src="../res/emotes/Happy.jpeg" width="30%"/>        |
| Sad         | 3  | <img src="../res/emotes/Sad.jpeg" width="30%"/>          |
| Angry       | 4  | <img src="../res/emotes/Angry.jpeg" width="30%"/>        |
| Confused    | 5  | <img src="../res/emotes/Confused.jpeg" width="30%"/>     |
| Closed      | 6  | <img src="../res/emotes/Closed.jpeg" width="30%"/>       |
| Sleepy      | 7  | <img src="../res/emotes/Sleepy.jpeg" width="30%"/>       |
| Dead        | 8  | <img src="../res/emotes/Dead.jpeg" width="30%"/>         |
| slightRight | 9  | <img src="../res/emotes/slightRight.jpeg" width="30%"/>  |
| Right       | 10 | <img src="../res/emotes/Right.jpeg" width="30%"/>        |
| slightLeft  | 11 | <img src="../res/emotes/slightLeft.jpeg" width="30%"/>   |
| Left        | 12 | <img src="../res/emotes/Left.jpeg" width="30%"/>         |
| slightUp    | 13 | <img src="../res/emotes/slightUp.jpeg" width="30%"/>     |
| Up          | 14 | <img src="../res/emotes/Up.jpeg" width="30%"/>           |
| slightDown  | 15 | <img src="../res/emotes/slightDown.jpeg" width="30%"/>   |
| Down        | 16 | <img src="../res/emotes/Down.jpeg" width="30%"/>         |



### Joint Pose
Each joint pose needs a time to move the joints (i.e. a proxy for movement speed) as set in JointMoveTime as well as a list of joint name-angle pairs specified in JointAngles.

JointMoveTime is an integer value that is sent to the motors, telling them how long it should take to move to the new angle. This is used to define motor speed. The integer value represents tenths of a second, where 1 is equal to 0.1 seconds. The acceptable range of values is 1-255, equivalent to a single byte unsigned integer.

JointAngles is a list of joint-angle pairs. For each pair, the "Joint" key expects a string name as the value, which identifies the specific joint motor to move (these names should match those provided in the [joint config file](./Software.md)). The "Angle" key expects an integer value between 0 and 240, which is the angular position to move the joint to.


### Audio Clips
Pre-made audio files can be included as part of behaviors. These audio files can be a stand-alone audio clip, or picked from a group of clips.It can be played asynchronously, or pause the behavior until it is completed. It can also be played with a specific probability as well, which means the audio will trigger with the defined probability percentage of the time. 

For audio to play, as minimum, the unique portion of the file name must be provided (see the naming guide [here](#audio-file-naming-structure)). The other options will use their default values if not provided. The input key names and expected values are shown in the table below.

| Key Name       | Type    | Default | Notes                                                                                      |
| -------------- | ------- | ------- | ------------------------------------------------------------------------------------------ |
| ClipName       | String  | ""      | Please see [naming structure](#audio-file-naming-structure).                               |
| IsGroup        | Boolean | "False" | Input as a string. See specifics [here](#audio-groups).                                    |
| IsCallResponse | Boolean | "False" | Input as a string. See specifics [here](#call-response-and-linked-audio).                  |
| IsVoice        | Boolean | "True"  | Input as a string. See specifics [here](#voice-types).                                     |
| Async          | Boolean | "True"  | Input as a string. If true, audio will play as behavior continues.                         |
| Probability    | Float   | 1       | Range is from 0 to 1, which maps with play range: never to always.                         |
| Encoding       | String  | None    | Will use encoding type provided to controller if none here. Specify as ending, i.e. ".mp3" |



#### Audio File Naming Structure
Each audio file is assumed to be a '.mp3' file at minimum, and will append this to the end of the string provided as ClipName. Depending on the option values set with the ClipName, the software will expect different naming components also attached to the file. The different audio options and how they modify the name are presented below.


##### Audio Groups
If IsGroup is set to True, then ClipName is treated as the name of the group, rather than the name of a stand alone audio file. In this case, the code will pull, at random, one of the files that starts with this name to play. This is done by looking for all files that start with this ClipName, and truncating that list to those files to unique instances of ClipName_ID, where ID is the unique clip identifier within the group. This identifier should only contain alphanumeric characters. For example, if we had an audio group named 'HoldMusic', all of the files in that group would begin with 'HoldMusic_' and each clip would have an identifier unique within the HoldMusic group, such as 0,1,2,etc.

*Note:* If the audio group also has unique [voice types](#voice-types), then the same cue, but with different voice types, should have the same identifier within the audio group.

*Note:* If the audio group is made up of [call-response](#call-response-and-linked-audio) audio files, then the call and response files that go together should have the same identifier within the audio group.

##### Call-Response and Linked Audio
Sometimes you might have audio that has a distinct follow-up response that should always be linked to that particular initial audio cue. A good example of this is trivia, where the first part of the audio is the question, and then, after waiting for responses, the system should play the answer to that specific trivia question.

In that situation, IsCallResponse should be set to True. The paired audio files will have the same ClipName, but should have an additional naming component depending an if they are the pre or post audio file to play. For example, say we want to tell a "Why did the chicken cross the road?" joke with a specific response. We could use the ClipName "chicken" and we would have two files, where the initial question part to play first has a starting audio file name of "chicken_pre" and the joke punchline follow up audio has a starting file name of "chicken_post".

*Note:* If using this with audio groups each call/response would be two files that are structured with GroupName_id_ and then the pre or post. So, a trivia question/answer in a bank of audio could look like "trivia_0_pre" and "trivia_0_post".


##### Voice Types
If IsVoice is set to True, then the audio file matches a particular voice or speaking style the robot will use. This was included so that the user may use the same code and behavior basis for a robot, but easily change the robot character by simply selecting a different voice. The original spoken audio files were pre-generated using Amazon Polly's 'Matt' and 'Joanna' voices for the same spoken statement, and this allowed all files to be in the same location for both voices.

If IsVoice is set to True, the audio manager will append the string provided on initialization as 'starting_voice' or the string set as 'selected_voice' to the end of the file. This will always be attached *last* after all other naming options are added. For example, if the selected_voice is set to "Matt" and IsVoice is true, the file name will always end as "_Matt.mp3".



## Starter Behaviors
We also provide a collection of pre-built behaviors to get you started with the system. The behaviors themselves are provided with the [software files](https://github.com/shareresearchteam/SAMI-Robot/tree/main/software). Some of the behaviors were provided by the students and their projects as part of their Oregon State University robotics course work. The related projects are linked in the notes. Each behavior is also shown below as an easy reference.

| Name               | Behavior                                             | Notes     |
| ------------------ | ---------------------------------------------------- | --------- |
| Afraid1            | <img src="../res/behaviors/Afraid1.gif"/>            |  |
| Afraid2            | <img src="../res/behaviors/Afraid2.gif"/>            |  |
| Afraid3            | <img src="../res/behaviors/Afraid3.gif"/>            |  |
| Angry1             | <img src="../res/behaviors/Angry1.gif"/>             |  |
| Angry2             | <img src="../res/behaviors/Angry2.gif"/>             |  |
| Angry3             | <img src="../res/behaviors/Angry3.gif"/>             |  |
| Bored1             | <img src="../res/behaviors/Bored1.gif"/>             |  |
| Bored2             | <img src="../res/behaviors/Bored2.gif"/>             |  |
| Bored3             | <img src="../res/behaviors/Bored3.gif"/>             |  |
| Happy1             | <img src="../res/behaviors/Happy1.gif"/>             |  |
| Happy2             | <img src="../res/behaviors/Happy2.gif"/>             |  |
| Happy3             | <img src="../res/behaviors/Happy3.gif"/>             |  |
| Neutral1           | <img src="../res/behaviors/Neutral1.gif"/>           |  |
| Neutral2           | <img src="../res/behaviors/Neutral2.gif"/>           |  |
| Neutral3           | <img src="../res/behaviors/Neutral3.gif"/>           |  |
| Relaxed1           | <img src="../res/behaviors/Relaxed1.gif"/>           |  |
| Relaxed2           | <img src="../res/behaviors/Relaxed2.gif"/>           |  |
| Relaxed3           | <img src="../res/behaviors/Relaxed3.gif"/>           |  |
| Silly1             | <img src="../res/behaviors/Silly1.gif"/>             |  |
| Silly2             | <img src="../res/behaviors/Silly2.gif"/>             |  |
| Silly3             | <img src="../res/behaviors/Silly3.gif"/>             |  |
| Sleepy1            | <img src="../res/behaviors/Sleepy1.gif"/>            |  |
| Sleepy2            | <img src="../res/behaviors/Sleepy2.gif"/>            |  |
| Sleepy3            | <img src="../res/behaviors/Sleepy3.gif"/>            |  |
| Surprise1          | <img src="../res/behaviors/Surprise1.gif"/>          |  |
| Surprise2          | <img src="../res/behaviors/Surprise2.gif"/>          |  |
| Surprise3          | <img src="../res/behaviors/Surprise3.gif"/>          |  |
| Yes                | <img src="../res/behaviors/Yes.gif"/>                |  |
| No                 | <img src="../res/behaviors/No.gif"/>                 |  |
| Wave               | <img src="../res/behaviors/Wave.gif"/>               |  |
| Home               | <img src="../res/behaviors/Home.gif"/>               |  |
| LegKickies         | <img src="../res/behaviors/LegKickies.gif"/>         |  |
| EmpatheticQuestion | <img src="../res/behaviors/EmpatheticQuestion.gif"/> |  |
| TorsoRotate        | <img src="../res/behaviors/TorsoRotate.gif"/>        |  |
| Quizzical          | <img src="../res/behaviors/Quizzical.gif"/>          |  |
| CastSpell          | <img src="../res/behaviors/CastSpell.gif"/>          | From [here](https://github.com/aschn464/CSI_SAMI) |       
| Cowering           | <img src="../res/behaviors/Cowering.gif"/>           | From [here](https://github.com/aschn464/CSI_SAMI) |
| GestureFar         | <img src="../res/behaviors/GestureFar.gif"/>         | From [here](https://github.com/aschn464/CSI_SAMI) |
| Give               | <img src="../res/behaviors/Give.gif"/>               | From [here](https://github.com/aschn464/CSI_SAMI) |
| PointForward       | <img src="../res/behaviors/PointForward.gif"/>       | From [here](https://github.com/aschn464/CSI_SAMI) |
| PointLeft          | <img src="../res/behaviors/PointLeft.gif"/>          | From [here](https://github.com/aschn464/CSI_SAMI) |
| PointRight         | <img src="../res/behaviors/PointRight.gif"/>         | From [here](https://github.com/aschn464/CSI_SAMI) |
| ShowBig            | <img src="../res/behaviors/ShowBig.gif"/>            | From [here](https://github.com/aschn464/CSI_SAMI) |
| Shrug              | <img src="../res/behaviors/Shrug.gif"/>              | From [here](https://github.com/aschn464/CSI_SAMI) |
| Explaining         | <img src="../res/behaviors/Explaining.gif"/>         | From [here](https://github.com/aschn464/CSI_SAMI) |
| Listening          | <img src="../res/behaviors/Listening.gif"/>          | From [here](https://github.com/aschn464/CSI_SAMI) |
| Thinking           | <img src="../res/behaviors/Thinking.gif"/>           | From [here](https://github.com/aschn464/CSI_SAMI) |
