from oscillovisa import *
from clilib import *
import serial 
import time

arduino = serial.Serial(port='/dev/cu.usbmodem14101',baudrate=115200,timeout=0.1)
# oscilloscope = get_intstrunment(VERBOSE=VERBOSE)
# time.sleep(2)

# while True:
#     cmd = 100128
#     send_command(cmd,arduino,VERBOSE=False)
#     read_monitor(arduino)
#     # print(arduino.readline())
#     time.sleep(0.01)

# arduino.close()

inst = get_intstrunment(VERBOSE=True)
plot_oscilloscope(inst,dpi=70,VERBOSE=True)
# get_data_csv(inst)