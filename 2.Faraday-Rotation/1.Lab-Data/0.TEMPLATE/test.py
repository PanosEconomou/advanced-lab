from oscillovisa import *
from controller_CLI import *
import serial 
import time

arduino = serial.Serial(port='/dev/cu.usbmodem14101',baudrate=115200,timeout=0.1)
time.sleep(2)

while True:
    cmd = 100128
    arduino.write(str(cmd).encode()+b'\n')
    time.sleep(0.01)
    print(arduino.readline())
    time.sleep(0.01)

arduino.close()

# inst = get_intstrunment()
# plot_oscilloscope(inst,dpi=70,channels=[1,2,3,4])
# # get_data_csv(inst)