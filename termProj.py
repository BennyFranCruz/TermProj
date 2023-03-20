"""!
@file termProj.py
    This file contains the main code for our term project. Contained is three main tasks: The yaw
    motor control taks, the x motor control task, and the main task that controlls all the states
    necessary for our aiming and firing proccess.
    
TODO: Party cause its the end of the quarter!

@author Mech-07 and JR Ridgely
@date   19-Marth-2023
@copyright (c) 2023 by Mech-07 and JR Ridgely and released under GNU Public License v3
"""

import encoder_reader
import motor_driver
import porportional_controller
import task_share
import cotask
import utime
from machine import Pin, I2C
import Cam

import gc
import pyb 



def YawMotorControlTask(shares):
    """!
    Task initializes the motor and encoder for the turrets yaw axis and runs the motor
    with a proportional controller when given a goal position
     
    @param shares A list holding the share and queue used by this task
    """
    
    #Variables that need to be shared between this task and the main task
    Y_pos, Y_vel, Y_goal = shares
    
        
    #Encoder initializing. Includes defining the timer and the pins for our encoder class
    pinB6 = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
    pinB7 = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)
    timer = pyb.Timer(4, prescaler=0, period=0xFFFF)
    ch1 = timer.channel (1, pyb.Timer.ENC_AB, pin=pinB6)
    ch2 = timer.channel (2, pyb.Timer.ENC_AB, pin=pinB7)
    
    #creating the encoder object, then calling the zero() function to zero the encoder
    encode = encoder_reader.Encoder(pinB6, pinB7, timer, ch1, ch2)
    encode.zero()
    
    #Motor driver initializing. Includes defining pin and setting up the PWM timer
    pinB4 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    pinB5 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    timer = pyb.Timer (3, freq=10000)
     
    #creating the motor object and giving the object name "moe"
    moe = motor_driver.MotorDriver(pinA10,pinB4,pinB5, timer)
    
    #creates P pontroller object and sets Ka
    controller1 = porportional_controller.PorportionalController(.08)
    
    position = 0 #Sets initial position to zer

    while True:
        oldposition = position #remembers old position
        position = encode.read() #find current position
        
                                        
        Y_vel.put(position-oldposition) #Puts the current velocity
        Y_pos.put(position)             #Puts the current pos

        control_output = controller1.run(Y_goal.get(), position) #run Pcontroller

        moe.set_duty_cycle(control_output) #set the duty cycle to value found from Pcontroller
        
        yield(0) #return nothing

def PitchMotorControlTask(shares):
    """!
    Task initializes the motor and encoder for the turrets pitch axis and runs the motor
    with a proportional controller when given a goal position
     
    @param shares A list holding the share and queue used by this task
    """
    
    #Variables that need to be shared between this task and the main task
    X_pos, X_vel, X_goal = shares
    
    #Encoder initializing. Includes defining the timer and the pins for our encoder class
    pinC6 = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
    pinC7 = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)
    timer8 = pyb.Timer(8, prescaler=0, period=0xFFFF)
    ch1 = timer8.channel (1, pyb.Timer.ENC_AB, pin=pinC6)
    ch2 = timer8.channel (2, pyb.Timer.ENC_AB, pin=pinC7)
    
    #creates encoder object, then callis the zero() function to zero the encoder
    encode2 = encoder_reader.Encoder(pinC6, pinC7, timer8, ch1, ch2)
    encode2.zero()
    
    #Motor driver initializing. Includes defining pin and setting up the PWM timer
    pinA0 = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    pinA1 = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    timer5 = pyb.Timer (5, freq=10000)
     
    #creates motor driver object
    moe2 = motor_driver.MotorDriver(pinC1,pinA0,pinA1, timer5)
    
    #creates P pontroller object and sets Ka
    controller2 = porportional_controller.PorportionalController(.05)
    
    position = 0 #Sets initial position to zero
    
    while True:   
        oldposition = position #remembers old position
        position = encode2.read() #find current position
                                        
        X_vel.put(position-oldposition) #Puts the current velocity
        X_pos.put(position)             #Puts the current position
        
        control_output = controller2.run(X_goal.get(), position) #run Pcontroller

        moe2.set_duty_cycle(control_output) #Sets duty cycle to controller output
        
        yield(0) #return nothing
        
def MainTask(shares):
    """!
    Task controls the rotate, aim, and fire sequence
    
    @param shares A list holding the share and queue used by this task
    """
    
    #initializes a time that is used for timing the 5 seconds between round starting and
    #opponents freezing
    inittime = utime.ticks_ms()
    
    #shared variables between all tasks
    Y_pos, Y_vel, Y_goal, X_pos, X_vel, X_goal = shares
    
    #fire activation pin instalizing
    pinB4 = pyb.Pin(pyb.Pin.board.PB0, pyb.Pin.OUT_PP)
    pinB4.value(0)
        
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

    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
    print(f"I2C Scan: {scanhex}")
        
    # Create the camera object and set it up in default mode
    gc.collect()
    camera = Cam.MLX_Cam(i2c_bus)
    gc.collect()
    col = 32 #Set col length
    row = 24 #Set Row Length 
    gc.collect()

    #logging initial time
    inittime = utime.ticks_ms()
    
    #TURN 180 DEG STATE
    
    #setting position goal of 180 degrees
    Y_goal.put(-100000)
    
    #While loop will stay in the controll loop untill the yaw axis is in the correct position and no longer moving
    while abs(Y_goal.get() - Y_pos.get()) > 200 and Y_vel !=0: 
        
        X_goal.put(4500)
        Y_goal.put(-100000)
        yield(0)
    
    #After the position is correct, the assem will be in a hold state untill 5 seconds passes
    while (utime.ticks_ms() - inittime < 4800):
        yield(0)

    #CAMERA CAPTURE STATE:
    
    #Following is the logic for the camera image capture. This state is held for only one iteration
    try:
        image = camera.get_image()
        maxVal = 0
        # Calculate non-overlapping 3x3 averages
        row = 12
        col = 0
        matrix = 0
        limits=(0, 99)
        scale = (limits[1] - limits[0]) / (max(image) - min(image))
        offset = limits[0] - min(image)
        while col < 29:
            while row < 23:
                #print(row)
                if(row%3 == 0 and row != 0 and row != 1 and row != 2):
                    #print(matrix)
                    if(matrix > maxVal):
                        #print(maxVal)
                        maxVal = matrix
                        maxVal_loc = row,col
                    matrix = 0 
                matrix += int((image[row * 32 + (31 - col)] + offset) * scale) + int((image[row * 32 + (32 - col)] + offset) * scale) + int((image[row * 32 + (33 - col)] + offset) * scale)
                #print(matrix)
                row += 1
            matrix = 0
            row = 12
            col += 3
        
        
    except KeyboardInterrupt:
        pass
    yield(0)
    
    #AIM STATE
    
    #Use maxVal_loc tuple to conver to pixel location 
    encode_pos = 550 * (maxVal_loc[1] - 16)

    #Funct that converts pixel target to values for aim goals.
    #Through testing we dicovered that the pitch target did not need to be adjusted and could be held at a static position
    Y_CameraGoal = -encode_pos - 100000 
    X_CameraGoal = 4500
    
    #putting new orientation goals into the shares
    Y_goal.put(Y_CameraGoal)
    X_goal.put(X_CameraGoal)
    
    #Use Yaw Motor Control to move to correct position. Will stay in this state untill goal position is held
    while abs(Y_goal.get() - Y_pos.get()) > 200 and Y_vel !=0:
        
        Y_goal.put(Y_CameraGoal)
        X_goal.put(X_CameraGoal)
        
        yield(0)  
    
    #FIRE STATE
        
    #Fire pin is set to high for a given number of iterations, this time relates to roughlt 3 shots
    c = 0
    while c < 80:
        pinB4.value(1)
        
        c += 1
        yield(0)
    
    #End State
    
    #This state is the finished state. The assembly should make no further actions
    while True:
        pinB4.value(0)
    
# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":

    # Create a share and a queue to test function and diagnostic printouts
    Y_pos = task_share.Share('q', thread_protect=False, name="Y Pos")
    Y_vel = task_share.Share('q', thread_protect=False, name="Y Vel")
    Y_goal = task_share.Share('q', thread_protect=False, name="Y Goal")
    
    X_pos = task_share.Share('q', thread_protect=False, name="X Pos")
    X_vel = task_share.Share('q', thread_protect=False, name="X Vel")
    X_goal = task_share.Share('q', thread_protect=False, name="X Goal")
    
    
    
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    
    task1 = cotask.Task(YawMotorControlTask, name="Task_1", priority=1, period=25,
                        profile=True, trace=False, shares=(Y_pos, Y_vel, Y_goal))
    task2 = cotask.Task(PitchMotorControlTask, name="Task_2", priority=2, period=25,
                        profile=True, trace=False, shares=(X_pos, X_vel, X_goal))
    task3 = cotask.Task(MainTask, name="Task_3", priority=3, period=10,
                        profile=True, trace=False, shares=(Y_pos, Y_vel, Y_goal, X_pos, X_vel, X_goal))
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()
    
    
    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    
    #set up UART and send the data to the computer 
    u2 = pyb.UART(2, baudrate=115200, timeout= 50)
    
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break
    
    
    
    