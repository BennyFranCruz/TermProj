import gc
import utime as time
import Cam
from ulab import numpy as np
import pyb
from machine import Pin, I2C

def main():
    # The following import is only used to check if we have an STM32 board such
    # as a Pyboard or Nucleo; if not, use a different library
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
    camera = Cam.MLX_Cam(i2c_bus)
    gc.collect()
    data_list = []
    data = []
    maxVal = 0
    begintime = time.ticks_ms()
    image = camera.get_image()
    try:
        #parse through data and create 2-d array with bottom 12 lines of data
        i = 0
        for line in camera.get_csv(image.v_ir, limits=(0, 99)):
            if(i < 12):
                line = line.split(',')
                if(',' in line):
                    line.remove(',')
                line = [int(x) for x in line]
                data_list.append(line)
                line = []
            i += 1
        #print(data_list)
        # Calculate non-overlapping 3x3 averages
        #averages = np.zeros((11, 4))  # initialize output array
        i = 0
        j = 0
        while i < 29:
            while j < 12:
                if(j%3 == 0 and j != 0):
                    average = (matrix / 9) # calculate mean and store in output array
                    print(average)
                    matrix = 0
                    if(average > maxVal):
                        maxVal = average
                        maxVal_loc = i,j
                        matrix = 0
                #print(j)
                matrix = data_list[j][i] + data_list[j][i+1] + data_list[j][i+2]  # extract non-overlapping 3x3 submatrix
                j += 1
            j = 0
            i += 3
        
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()