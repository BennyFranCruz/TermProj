"""!
@file porportional_controller.py
This file contains code which defines our porportional controller class. This class recieves
Kp as an input, then everytime it is called it will give a porportional response with
this input for a given goal position and current position.

TODO: Clean up code

@author Mech-07
@date   10-Feb-2023
@copyright (c) 2023 by Mech-07 and released under GNU Public License v3
"""

class PorportionalController:   
    
    def __init__(self, Kp):
        """!
        Initializes the class and deifnes its internal variables.
        @param   self   essential def for class creation
        @param   Kp   The controller gain for the position controller
        @returns None
        """   
        self.Kp = Kp
        
    def run(self, setpoint, currentposition):
        
        """!
        Gives a porportional control output for a given goal position and current position
        @param   setpoint   Goal location for controller
        @param   currentposition   Current position of motor
        @returns p_control_out    The controller output for the motor
        """
    
        self.p_control_out = -self.Kp*(setpoint - currentposition)
        
        #logic ensures that the pwm signal outputed is never greater than 100 or less than -100
        if self.p_control_out > 100:
            self.p_control_out = 100
        elif self.p_control_out <-100:
            self.p_control_out = -100
        
        return(self.p_control_out)
    
