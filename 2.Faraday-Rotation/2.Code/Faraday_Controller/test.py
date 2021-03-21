from oscillovisa import *
from clilib import *
import serial 
import time
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

# arduino = serial.Serial(port='/dev/cu.usbmodem14101',baudrate=115200,timeout=0.1)
# # oscilloscope = get_intstrunment(VERBOSE=VERBOSE)
# # time.sleep(2)

# # while True:
# #     cmd = 100128
# #     send_command(cmd,arduino,VERBOSE=False)
# #     read_monitor(arduino)
# #     # print(arduino.readline())
# #     time.sleep(0.01)

# # arduino.close()

# inst = get_intstrunment(VERBOSE=True)
# plot_oscilloscope(inst,dpi=70,VERBOSE=True)
# # get_data_csv(inst)


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize = (10,7),dpi=100)
ax = fig.add_subplot()
ax.set_xlabel(r'Angle $\Delta \phi$ [degrees]')
ax.set_ylabel(r'Voltage V [V]')
ax.set_title('Voltage VS Angle')

xdata, ydata, std = [], [], []
ln, = plt.plot([], [],'+',c='darkblue',label='Raw Data')

def init():
    ax.legend(frameon=False)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    std.append(np.random.random()*0.2)

    dx = max(xdata)-min(xdata)
    dy = max(ydata)-min(ydata)
    if dx!=0 and dy!=0:
        ax.set_xlim(min(xdata)-0.1*dx, max(xdata)+0.1*dx)
        ax.set_ylim(min(ydata)-0.1*dy, max(ydata)+0.1*dy)

    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=tqdm(np.linspace(0, 2*np.pi, 50)),interval=10,init_func=init, blit=False)
plt.show()