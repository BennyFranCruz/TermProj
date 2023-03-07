"""!
@file encoder_reader.py
This file contains code which defines our encoder reader class. It includes an init function, a read function,
and a zero function. When utilized, this code should be able to properly read the motor encoder and give back
sensical values that do not overflow when the hardware does. 

TODO: Clean up code and check functions

@author Mech-07
@date   1-Feb-2023
@copyright (c) 2023 by Mech-07 and released under GNU Public License v3
"""
 
import utime
import pyb

class Encoder:
    
    def __init__ (self, in1pin, in2pin, timer, ch1, ch2):
        """!
        Initializes the class and defines its internal variables
        @param   self   essential def for class creation
        @param   in1pin defines one of the two encoder output pins
        @param   in2pin defines the second encoder output pin
        @param   timer  defines the timer and its settings that will be used for reading the encoder
        @param   ch1    defines the a channel that will be used with the timer
        @param   ch2    defines the 2nd channel that will be used with the timer
        @returns None
        """
        
        self.tim   = timer
        self.pin1  = in1pin
        self.pin2  = in2pin
        self.temp1 = 0
        self.position = 0
        self.ch1 = ch1
        self.ch2 = ch2
        
    def read(self):
        """!
        Reads the encoder and returns motor position as an int. Should be accurate and not overflow when hardware does
        @param   self essential def for class creation
        @returns position of motor
        """
        period=0xFFFF
        temp2 = self.tim.counter()
        delta = temp2 - self.temp1
        self.temp1 = temp2
        if(delta > ((period + 1)/2)):
            delta -= period + 1
        elif(delta < (((-1 * period) + 1)/2)):
            delta += period + 1 
        self.position += delta
        return self.position
        
    def zero(self):
        """!
        Sets encoder position to zero
        @param   self  essential param for class creation
        @returns none
        """
        self.position = 0
      