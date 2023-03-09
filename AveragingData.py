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
    print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")
    
    limits=(0, 99)
    scale = (limits[1] - limits[0]) / (max(image.v_ir) - min(image.v_ir))
    offset = limits[0] - min(image.v_ir)
    
    try:
        # Calculate non-overlapping 3x3 averages
        row = 12
        col = 0
        matrix = 0
        while col < 29:
            while row < 23:
                if(col%3 == 0 and col != 0 and col != 1 and col != 2):
                    if(matrix > maxVal):
                        maxVal = matrix
                        maxVal_loc = row,col
                    matrix = 0
                if col == 12:
                    break   
                matrix += int((image.v_ir[row * 32 + (31 - col)] + offset) * scale) + int((image.v_ir[row * 32 + (32 - col)] + offset) * scale) + int((image.v_ir[row * 32 + (33 - col)] + offset) * scale)
                row += 1
            row = 0
            col += 3
        print(f"{maxVal_loc}")
        print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")
        
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()