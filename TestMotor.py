import gc
import pyb
import cotask
import task_share

import utime

import motor_driver    #Classes we have written for driving the motor and reading the encoder
import encoder_reader
import porportional_controller

def main():
    """!
    Task sets up a second motor and encoder and runs a proportional
    controller with a set position on this motor. 
    @param shares A list holding the share and queue used by this task
    """ 
    pinC6 = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
    pinC7 = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)
    timer8 = pyb.Timer(8, prescaler=0, period=0xFFFF)
    ch1 = timer8.channel (1, pyb.Timer.ENC_AB, pin=pinC6)
    ch2 = timer8.channel (2, pyb.Timer.ENC_AB, pin=pinC7)
    
    #calling the encoder class, then calling the zero() function to zero the encoder
    encode2 = encoder_reader.Encoder(pinC6, pinC7, timer8, ch1, ch2)
    encode2.zero()
    
    #Motor driver initializing. Includes defining pin and setting up the PWM timer
    pinA0 = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    pinA1 = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    timer5 = pyb.Timer (5, freq=10000)
     
    #calling the motor driver class and giving the object name "moe"
    moe2 = motor_driver.MotorDriver(pinC1,pinA0,pinA1, timer5)
    
    controller2 = porportional_controller.PorportionalController(.01)
    
    while True:
        position2 = encode2.read() #find current position
        control_output2 = controller2.run(-44227, position2) #run controller 
        print(position2)
        #print(control_output2)
        moe2.set_duty_cycle(control_output2)
        #print(control_output2)
if __name__ == "__main__":
    main()