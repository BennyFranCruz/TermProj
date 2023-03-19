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
The second issue we faced was ensuring the camera was properly lined up directly in front of 

### Software Design Overview:

...

The heat seeking portion of our project was accomplished using the Infared MLX90640 and Camera Driver provided to the class. 
The I2C connected device returns an array of values that correspond with pixel values produced by the camera with a width of 32 and a height of 24. 


The goal of our software was to take this array at to find the hottest three by three section which would correspond to the location of the person. 
We decided on a three x three square averaging algorithm to ensure that the software would not set the aim point to be at an outlyer of points but rather a concentrated area of heat. The exact value of three by three was decided based on the distance each pixel represents in the real world when the camera is set

Doxygen Link...

### Results:

We tested our system by...

Our system performed well in these tests...

### What was Learned/Recommendations:

What worked well...

What didn't work well...

### Additional Links:

CAD Drawings Link...

