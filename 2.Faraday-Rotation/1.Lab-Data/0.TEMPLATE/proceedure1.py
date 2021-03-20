from oscillovisa import *
from clilib import *
from csvlib import *
import numpy as np
import time
from tqdm import tqdm

# Set the run Variables
VERBOSE = False
WAIT_TIME = 1
MOTOR_SPEED = 20 
directory = './DATA/'
min_angle = 0
max_angle = 90
Nangles = 20

# GET Arduino and Oscilloscope
arduino = get_arduino(VERBOSE=VERBOSE)
oscilloscope = get_intstrunment(VERBOSE=VERBOSE)

angle = np.linspace(min_angle,max_angle,Nangles,dtype=int)
V = []
V_std = []

# Set the speed
set_speed(MOTOR_SPEED,arduino,VERBOSE=VERBOSE)

# For all angles
for a in tqdm(angle):
    # Set the polariser
    move_to_angle(a,arduino,VERBOSE=VERBOSE)

    # Wait
    time.sleep(WAIT_TIME)

    # Get the measuremets
    amplitude = get_data(oscilloscope,channel=3)
    V.append(np.mean(amplitude[0]))
    V_std.append(np.std(amplitude[0]))
    
    # Save the data to CSV
    get_data_csv(oscilloscope,channels=[1,2,3],directory=directory,filename='Angle-'+str(a)+'.csv')
    plot_oscilloscope(oscilloscope,channels=[1,2,3],VERBOSE=VERBOSE,PLOT=False,save_image=True,filename=directory+'Angle-'+str(a))

# Output the values
V = np.array(V)
V_std = np.array(V_std)
create_csv(name='Voltage-Amplitude.csv',directory=directory,titles=['Angle','Voltage','Voltage_std'],data=[angle,V,V_std])