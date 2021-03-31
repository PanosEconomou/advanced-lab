from oscillovisa import *
from clilib import *
from csvlib import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from tqdm import tqdm

# Set the run Variables
VERBOSE = False
WAIT_TIME = 0.01
MOTOR_SPEED = 20 
directory = './DC_VERDET_ROD/'
min_angle = 0
max_angle = 360
Nangles = 360

# GET Arduino and Oscilloscope
arduino = get_arduino(VERBOSE=VERBOSE)
oscilloscope = get_intstrunment(VERBOSE=VERBOSE)

angle = np.linspace(min_angle,max_angle,Nangles,dtype=int)
V = []
V_std = []
a_data = []

# Set the speed
set_angle(0,arduino,VERBOSE=VERBOSE)
set_speed(MOTOR_SPEED,arduino,VERBOSE=VERBOSE)

# Relevant Realtime Plotting Variables
fig = plt.figure(figsize = (10,7),dpi=70)
ax = fig.add_subplot()

ln, = plt.plot([], [],'+',c='darkblue',label='Raw Data')

# Initialises the plot
def init():
    ax.set_xlabel(r'Angle $\Delta \phi$ [degrees]')
    ax.set_ylabel(r'Voltage V [V]')
    ax.set_title('Voltage VS Angle')
    ax.legend(frameon=False)
    return ln,

# The actual Experimental Proceedure
# For all angles
def get_measurement(a):
    global V,V_std
    # Set the polariser
    move_to_angle(a,arduino,VERBOSE=VERBOSE)

    # Wait
    time.sleep(WAIT_TIME)

    # Get the measuremets
    amplitude = get_data(oscilloscope,channel=2)
    V.append(np.mean(amplitude[0]))
    V_std.append(np.std(amplitude[0]))
    
    # Save the data to CSV
    get_data_csv(oscilloscope,channels=[1,2],directory=directory,filename='Angle-'+str(a)+'.csv')
    # plot_oscilloscope(oscilloscope,channels=[1,2,3],VERBOSE=VERBOSE,PLOT=False,save_image=True,filename=directory+'Angle-'+str(a))

    # # Relevant Plotting stuff
    # a_data.append(a)
    # dV = max(V)-min(V)
    # da = max(a_data)-min(a_data)
    # if dV!=0 and da!=0:
    #     ax.set_xlim(min(a_data)-0.1*da, max(a_data)+0.1*da)
    #     ax.set_ylim(min(V)-0.1*dV, max(V)+0.1*dV)

    # ln.set_data(a_data, V)
    # return ln,

# Output the values to CSV 
def on_close(event):
    global V,V_std
    print('Done with experiment, exporting CSV')
    V = np.array(V)
    V_std = np.array(V_std)
    create_csv(name='Voltage-Amplitude.csv',directory=directory,titles=['Angle','Voltage','Voltage_std'],data=[angle,V,V_std],VERBOSE=True)

    
# Perform the Run
for a in tqdm(angle):
    get_measurement(a)

init()
dV = max(V)-min(V)
da = max(angle)-min(angle)
if dV!=0 and da!=0:
    ax.set_xlim(min(angle)-0.1*da, max(angle)+0.1*da)
    ax.set_ylim(min(V)-0.1*dV, max(V)+0.1*dV)

ln.set_data(angle, V)

on_close(None)

plt.savefig(directory+'Voltage-VS-Angle',dpi = 300)
plt.show()

# ani = FuncAnimation(fig, get_measurement, frames=tqdm(angle),interval=10,init_func=init, blit=False,repeat=False)
# plt.show()