import gc
import utime as time
import Cam
import numpy as np

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
    try:
        #parse through data and create 2-d array with bottom 12 lines of data
        i = 0
        for line in camera.Cam.get_csv(image.v_ir, limits=(0, 99)):
            if(i < 12):
                data.append(line)
            i += 1
            data_list.append(data)
            data = []
        # Calculate non-overlapping 3x3 averages
        averages = np.zeros(((data_list.shape[0]-2)//2, (data_list.shape[1]-2)//2))  # initialize output array
        for i in range(averages.shape[0]):
            for j in range(averages.shape[1]):
                matrix = data_list[i*2:i*2+3, j*2:j*2+3]  # extract non-overlapping 3x3 submatrix
                averages[i,j] = np.mean(sub_matrix)  # calculate mean and store in output array
                if(averages[i,j] > maxVal):
                    maxVal = averages[i,j] 
        print(averages)
        
    except KeyboardInterrupt:
        break