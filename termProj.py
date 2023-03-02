import encoder_reader
import motor_driver
import proportional_controller
import task_share
import cotask
import mma845x

import Cam

def initilize():
    ''' Function initilizes both motors and encoders
        Function initilizes

    '''
    #Encoder initializing. Includes defining the timer and the pins for our encoder class
    pinB6 = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
    pinB7 = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)
    timer = pyb.Timer(4, prescaler=0, period=0xFFFF)
    ch1 = timer.channel (1, pyb.Timer.ENC_AB, pin=pinB6)
    ch2 = timer.channel (2, pyb.Timer.ENC_AB, pin=pinB7)
    
    #calling the encoder class, then calling the zero() function to zero the encoder
    encode = encoder_reader.Encoder(pinB6, pinB7, timer, ch1, ch2)
    encode.zero()
    
    #Motor driver initializing. Includes defining pin and setting up the PWM timer
    pinB4 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    pinB5 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    timer = pyb.Timer (3, freq=10000)
    
    moe = motor_driver.MotorDriver(pinA10,pinB4,pinB5, timer)
    
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
    
    
    # The following import is only used to check if we have an STM32 board such
    # as a Pyboard or Nucleo; if not, use a different library
    # the following code also initilizes the camera
    try:
        from pyb import info

    # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
    except ImportError:
        # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
        i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))

    # OK, we do have an STM32, so just use the default pin assignments for I2C1
    else:
        i2c_bus = I2C(1)

    print("MXL90640 Easy(ish) Driver Test")

    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
    print(f"I2C Scan: {scanhex}")
        
    # Create the camera object and set it up in default mode
    gc.collect()
    camera = MLX_Cam(i2c_bus)
    gc.collect()
    col = 32
    row = 24
    
def main():
    
    