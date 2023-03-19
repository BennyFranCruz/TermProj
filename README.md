# TermProj

## By: Benny Cruz, Arfan Ansar, Noah Johnson

### Introduction:

The purpose of our project...

Our device is intended to be used by...

Description: Apply automatic target acquisition, aiming, and 
firing control to a projectile launcher. The launcher must be 
autonomous in that it detects and tracks a target and launches 
a projectile without user intervention.

### Hardware Design Overview:

Initial Design for our model:

![image](https://user-images.githubusercontent.com/123694704/222578896-4dc89d2b-2bda-4261-94ee-272f30845584.png)

Finite State Machine:

![image](https://user-images.githubusercontent.com/123694704/222577944-6a93ee3a-615a-4e62-8a17-e6fa583c91a9.png)

Week 8 Progress: One axis motion

![image](https://user-images.githubusercontent.com/123694704/222578552-e666e68b-2c39-4478-9a21-504892391d58.png)

The camera set up was set at eight feet away from the edge of the table which allowed it to be much closer to the opponent then if we kept it mounted on the physical device. This set up provided itself with two initial issues. 
The first issue was worry of I2C capabilities to transmit data accuretly and quickly along such long wires. However this turned out to not be an issue and required no solution as it worked with the wires used very well and very quickly. When timing the camera capture it took a mere 350ms when using the raw camera input. When comparing this time to the motor actuation, it is minimal and unconsiquential.
The second issue we faced was ensuring the camera was properly lined up directly in front of the barrel of the device. To accomplish this we attached two strings, one connected to each side of the device and the camera mount. The two strings were the exact length of the table and placed the camera at the edge of the far side of the table. By ensuring both strings are taught it enabled the same placement of the camera every set up. 

### Software Design Overview:

...

The heat seeking portion of our project was accomplished using the Infared MLX90640 and Camera Driver provided to the class. 
The I2C connected device returns an array of values that correspond with pixel values produced by the camera with a width of 32 and a height of 24. 


The goal of our software was to take this array at to find the hottest three by three section which would correspond to the location of the person. 
We decided on a three x three square averaging algorithm to ensure that the software would not set the aim point to be at an outlyer of points but rather a concentrated area of heat. The exact value of three by three was decided based on the distance each pixel represents in the real world. This value was found by setting up the camera in its desired location and taking the picture of a known length object across where the opoonent would stand. Using this method we found each pixel was 1.5 inches in length. Based on this value we deduced a 4.5x4.5 inch block of area was sufficient for our averaging. 

The averaging algorithm itself was double for loop, one incrementing the rows and one incrementing the columns. The nested row incrementation took the values of the corresponding three columns using the following code. 
matrix += int((image[row * 32 + (31 - col)] + offset) * scale) + int((image[row * 32 + (32 - col)] + offset) * scale) + int((image[row * 32 + (33 - col)] + offset) * scale)
This took the first 1x3 of data. The row is then incremented and the data taken again. Doing this three times creates a value for the 3x3. This value is then compared to the current max value and if larger than that value the row and column location is stored in a tuple to be used later. 
The outer while loop then increments by three in order to not take overlapping data. By not taking overlapping data it increased the speed of our process to be an average of 270ms per processing. 

Doxygen Link...

### Results:

We tested our system by...

Our system performed well in these tests...

### What was Learned/Recommendations:

What worked well...

What didn't work well...

### Additional Links:

CAD Drawings Link...

