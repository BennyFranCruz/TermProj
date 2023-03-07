"""!
@file motor_driver.py
This file contains code which defines our motor driver class. This includes an initialization function and
a set duty cycles function. When this class is set up and called, it alows the program using it to control the pwm
signal to a connected motor

TODO: Clean up code

@author Mech-07
@date   1-Feb-2023
@copyright (c) 2023 by Mech-07 and released under GNU Public License v3
"""

import pyb
import utime

class MotorDriver:   
    
    def __init__(self, en_pin, in1pin, in2pin, timer):
        """!
        Initializes the class and deifnes its internal variables.
        @param   self   essential def for class creation
        @param   en_pin defines the enable pins location
        @param   in1pin defines one of the two motor input pins
        @param   in2pin defines the second motor input pin
        @param   timer  defines the timer its settings that will be used for PWM control 
        @returns None
        """
        
        self.tim   = timer
        self.enpin = en_pin
        self.pin1  = in1pin
        self.pin2  = in2pin
        self.ch1 = self.tim.channel (1, pyb.Timer.PWM, pin=self.pin1)
        self.ch2 = self.tim.channel (2, pyb.Timer.PWM, pin=self.pin2)
        self.enpin.value(0)
    
    
    def set_duty_cycle(self, level):
        
        """!
        Sets the level of the pwm input to a motor. If entered as negative, the motor will spin the other direction
        @param   level The pwm signal as a percent to be sent to the motor
        @returns none
        """
        #this logic ensures that if a negative number is inputed into the function, the motor will reverse direction.
        if(level < 0):
            self.pin1 = self.ch1.pulse_width_percent(0)
            self.pin2 = self.ch2.pulse_width_percent(abs(level))
        elif(level > 0):
            self.pin2 = self.ch2.pulse_width_percent(0)
            self.pin1 = self.ch1.pulse_width_percent(abs(level))
        else:
            self.pin1 = self.ch1.pulse_width_percent(0)
            self.pin2 = self.ch2.pulse_width_percent(0)
        
        self.enpin.value(1)

        