import encoder_reader
import motor_driver
import porportional_controller
import task_share
import cotask
import mma845x

import Cam

import gc
import pyb 

def initilize():
    
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

def YawMotorControlTask(shares):
    """!
    Task sets up a second motor and encoder and runs a proportional
    controller with a set position on this motor. 
    @param shares A list holding the share and queue used by this task
    """
    
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
    
    position = 0
    t=0
    
    while True:
        oldposition = position #remembers old position
        position = encode.read() #find current position
                                        #Gets the current pos goal
        Y_vel.put(position-oldposition) #Puts the current velocity
        Y_pos.put(position)

        
        control_output = controller1.run(Y_goal.get(), position) #run Pcontroller
        
        #Printing Position Logic
        #if t > 30:
            #print(position)
            #t = 0
        #t+= 1

        moe.set_duty_cycle(control_output) #set the duty cycle to value found from Pcontroller
        
        yield(0) #return nothing

def PitchMotorControlTask(shares):
    """!
    Task sets up a second motor and encoder and runs a proportional
    controller with a set position on this motor. 
    @param shares A list holding the share and queue used by this task
    """
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
    
    position = 0
    t = 0
    
    while True:   
        oldposition = position #remembers old position
        position = encode2.read() #find current position
                                        #Gets the current pos goal
        X_vel.put(position-oldposition) #Puts the current velocity
        X_pos.put(position)

        
        control_output = controller2.run(X_goal.get(), position) #run Pcontroller
        
        #From all the way up, max pos is 18000
        
         #Printing Position Logic
        
        #if t > 10:
            #print(position)
            #t = 0
        #t+= 1

        moe2.set_duty_cycle(control_output) #Sets duty cycle to controller output
        
        yield(0) #return nothing
        
def MainTask(shares):
    """!
    Task controls all rotate, aim, fire sequence
    @param shares A list holding the share and queue used by this task
    """
    Y_pos, Y_vel, Y_goal, X_pos, X_vel, X_goal = shares
    
    
    
    "Turn 180 State"
    
    Y_goal.put(0)#-100000)
        
    while abs(Y_goal.get() - Y_pos.get()) > 200 and Y_vel !=0:
        
        X_goal.put(0)#5700)
        Y_goal.put(0)#-100000)
        yield(0)

    
    "TEMP Scan With Camera State"
    "This state will output pixel loccation of aim target"
    T = 0
    while T < 100:
        print("scanning")
        T += 1
        yield(0)
        
    "Aim State"
    
    #Funct that converts pixel target to values for aim goals goes her
    
    Y_CameraGoal = 0 #-100000 + 23000
    X_CameraGoal = 0 #5700 - 1500 #Temp Aim goals
    
    Y_goal.put(Y_CameraGoal)
    X_goal.put(X_CameraGoal)
    
    while abs(Y_goal.get() - Y_pos.get()) > 200 and Y_vel !=0:
        
        Y_goal.put(Y_CameraGoal)
        X_goal.put(X_CameraGoal)
        yield(0)  
    
    "Fire State"
    while True:
        #Logic for Firing goes here
        print("fire!")
        yield(0)
    
# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

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
    
    
    
    