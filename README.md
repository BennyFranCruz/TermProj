# TermProj

## By: Benny Cruz, Arfan Ansar, Noah Johnson

### Introduction:

The purpose of our device is a heat seeking self aiming turret. The goal is to be able to quickly turn and face an opponent at an unknown location and fire nerf darts at them. Our Device uses a modified D-Dart tempest foam dart blaster, and two motors controlled by the Nucleo microcontroller through this we Apply automatic target acquisition, aiming, and firing control to a projectile launcher. The launcher is autonomous in that it detects and tracks a target and launches a projectile without user intervention.

Our device is intended to be used by our team members. Because of this decision, the ergonomic requirements for its operation were much more relaxed. We did not need to design for operation by users who are not fully familiar with the system,  

Description: 

### Hardware Design Overview:

Our initial design revolved around the goal of yaw and pitch aiming capability. We knew we wanted to use the tub motors due to our access and familiarity with them. Along with this, we knew we wanted to use a nerf gun that required as little modification as possible for integration. This meant through correct blaser selection we would ideally not need to design any loading or firing mechanisms ourselves. This design choise was made in order to simplify the design proccess 

Initial Design for our model:

![image](https://user-images.githubusercontent.com/123694704/222578896-4dc89d2b-2bda-4261-94ee-272f30845584.png)

As the design proccess continued, we selected a blaster that could be automatically fired through simply shorting two wires. This meant that our design would ultimately just need to be capable of aiming and shorting the wires. We knew the shorting could be done electronically, and so this removed the complexity of having a mechanical firing method. Ultimately, this also meant we only needed two tub motors for the whole design, with no other mechanically driven elements. 

For both axis of aiming we used a simple gear system with a drive gear connected to the motors and a driven gear on each axis. This allowed fine control due to reduction gear ratios. 

Completed CAD Design:



Week 8 Progress: One axis motion

![image](https://user-images.githubusercontent.com/123694704/222578552-e666e68b-2c39-4478-9a21-504892391d58.png)

After week 8, we desided to have the camera be mounted seperatly for the rest of the assembly. By having it near the middle of the table, we hoped to have a clearer difelity in the heat captures it could make of opponents. There was concerns that noise along such long wires would become an issue, However this turned out to not be the case. This change did, however, introduce repeatability problems in the system. If the camera was not precisly positioned realative to the main assembly, our amining corrections would be innacurate. To accomplish position repeatability we attached two strings between the assemblies, one connected to each side of the device and the camera mount. The two strings were the exact length of the table and placed the camera at the edge of the far side of the table. By ensuring both strings are taught it enabled the same placement of the camera every set up. 

Overall, the assembly was sturdy and held up well to use. Though there was some slop in the aiming axis, this did not affect our accuracy enough to be a problem.

Completed design:

### Software Design Overview:

Our software design included three tasks. In order of priority the taskes were Yaw Motor Control, Pitch Motor Control, and the main task. 
The thought process behind this was whenever an X or Y goal value was changed we would immediatly want the first priority to be setting the device to that location. Our Yaw and Pitch Motor controlls both ran porportional controllers based on desired encoder values. These encoder values are found in our main task and are shared between the three tasks. The Yaw and Pitch Motor controls are almost identical but each set up and operate on different tub motors. 

The main task is the brains of the operation. In this task it initilizes our camera, zeros the encoders. It then commits our first action which is setting the Yaw goal to 100,000 which flips the device around. By setting this Yaw goal, the Yaw Motor Control is called and does this action. The next part of our main task is aiming the device. 

The heat seeking aiming portion of our project was accomplished using the Infared MLX90640 and Camera Driver provided to the class. 
The I2C connected device returns an array of values that correspond with pixel values produced by the camera with a width of 32 and a height of 24. 

The goal of our software was to take this array at to find the hottest three by three section which would correspond to the location of the person. 
We decided on a three x three square averaging algorithm to ensure that the software would not set the aim point to be at an outlyer of points but rather a concentrated area of heat. The exact value of three by three was decided based on the distance each pixel represents in the real world. This value was found by setting up the camera in its desired location and taking the picture of a known length object across where the opoonent would stand. Using this method we found each pixel was 1.5 inches in length. Based on this value we deduced a 4.5x4.5 inch block of area was sufficient for our averaging. 

The averaging algorithm itself was double for loop, one incrementing the rows and one incrementing the columns. The nested row incrementation took the values of the corresponding three columns.

This took the first 1x3 of data. The row is then incremented and the data taken again. Doing this three times creates a value for the 3x3. This value is then compared to the current max value and if larger than that value the row and column location is stored in a tuple to be used later. 
The outer while loop then increments by three in order to not take overlapping data. By not taking overlapping data it increased the speed of our process to be an average of 270ms per processing. 

After the max value and its corresponding location is found, this value must then be converted into an encoder positon for the proportional controller to be run on. 
These values were found by taking the mutliplying an offset by the value subracted by 16. The offset was found by reading the encoder values of the motor while it turns a specific amount of degrees. This encoder value per degree is then translated into a value per pixel based on the geometry of our camera position to the person.

Using these mathematical formulas and some trail and error we found an offset of 550 per pixel to work effectively. The other part of the formula is based on the center pixel of the camera being pixel 16 due to its 32 pixel length. Since we are moving from center with the pixels increasing from 0 to 32 starting from the far left to right of the picture, it is essential to subtract 16 from the column value to deduce the amount of pixels offset the desired location is. This offset also accuretly makes the motor move either left or right based on the negative or positive position. 

With an accurate encoder position, our porportional controller can be ran on this value to quickly move the barrel to be centered on the target using the Yaw and Pitch Motor control tasks. 

The final state of our main task file is the firing state. Due to our hardware design described above, a simple turning of a pin high to enable the relay is all that is necessary to fire the device. By setting the time high to a specific value we can determine the amount of "bullets" fired by our device to to its semi-automatic nature. 

Doxygen Link...

### Results:

We tested our system by...

Our system performed well in these tests...

### What was Learned/Recommendations:

The 3-D printed portion of our hardware design worked very well. Through CAD simulations and system modeling we were able to deduce proper gear ratios to move the device easily and effectivly. These gears were 3-D printed on campus and worked extremely well with no issues when installed. By creating gear inserts for the motors, it ensured our gears did not wear quickly and integrated smoothly. 

One of our major issues was the accuracy of the projectile launcher itself. Being a kids toy with no barrel, accuracy was the not the number one priority of the manufacturer. This made it hard to consistently hit a target despite the tracking and motor control being very well executed. The device also had a complicated design with the rotating holster that made the hardware design tricky and limited our options of mounting. 

Picking a projectile launcher was the most crucial part of this project. It is hard to know what exact design specificiations you want when you initilly order this part yet it is an extremely important part of the system that is hard to change later. We would recommend testing accuracy as well as researching weight and size of the launcher before purchasing. 

###For Doxy main page
Finite State Machine:

![image](https://user-images.githubusercontent.com/123694704/222577944-6a93ee3a-615a-4e62-8a17-e6fa583c91a9.png)
