# This is a library to interface with an osscilloscope and get data through VISA

import numpy as np
import pyvisa 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import serial 
import time
from csvlib import *

# GET INSTRUNMENT ############################
def get_intstrunment(ADDRESS=None,VERBOSE=False):
    '''
    Get's the right parameters and returns an oscilloscope instrunment
    
    ADDRESS (None): When given, the selected instrinmnet is connected
    VERBOSE (False): When True prints the list of visa addresses, and the name of the connected instrunment

    Returns ------------
    inst: A pyvisa object for the instrunment
    '''

    rm = pyvisa.ResourceManager()
    if type(ADDRESS) == type(None):
        inst = rm.open_resource(rm.list_resources()[0])
    else:
        inst = rm.open_resource(ADDRESS)
    
    if VERBOSE: print(rm.list_resources_info())
    if VERBOSE: print(inst.query("*IDN?"))

    return inst


# GET DATA ##################################

def get_data(inst,channel=1,points=1000, acquire=True, VERBOSE=False):
    '''
    Given an instrunment object it reads the waveform data and returns a time series of the voltage.

    inst: [REQUIRED] the instrunment object
    channel (1): int denotes the oscilloscope channel
    points (1000): Number of points to get data from
    acquire (True): If false, the oscilloscope does not aquire new data
    VERBOSE (False): When True prints the preable

    Returns --------------
    
    '''

    # Acquire if Needed
    if acquire: inst.write(':DIGitize')

    # Write the appropriate variables for data collection
    inst.write(':WAVEFORM:SOURCE CHAN'+str(int(channel)))  # Source is Channel 1
    inst.write(':WAVEFORM:POINTS '+str(int(points)))       # Set the number of data points to collect
    inst.write(':WAVEFORM:FORMAT ASCII')                   # Set the format of the output data

    # Get the preamble and decipher
    preamble = [float(i) for i in inst.query(':WAVEFORM:PREAMBLE?').split(',')]

    Npts = int(preamble[2])-1

    dt = preamble[4]
    t0 = preamble[5]+dt
    t = np.linspace(t0,t0*Npts,Npts)

    dy = preamble[7]
    y0 = preamble[8]

    if VERBOSE: print("Reading from Channel "+str(int(channel))
        +"\n\tNpts: %d\n\tdt %.3e\n\tt0 %.3e\n\tdy %.3e\n\ty0 %.3e"%(Npts,dt,t0,dy,y0))
    

    # Get the actual voltage values
    values = np.array([float(i) for i in inst.query(':WAV:DATA?').split(',')[1:]])

    # Return everything
    return values,t,[Npts,dt,t0,dy,y0]


# PLOT OSCILLOSCOPE SCREEN ######################
def plot_oscilloscope(inst,channels=[1,2,3,4],points=1000,dpi=200,VERBOSE=False):
    '''
    Plots the Oscilloscope Screen
    
    inst: [REQUIRED] the instrunment object
    channels ([1,2,3,4]): List of channels to plot
    points (1000): Number of points to get data from
    dpi (200): The dpi of the image
    VERBOSE (False): When True prints the preable
    '''
    # Create Figure
    fig = plt.figure(figsize = (16,4*len(channels)),dpi=dpi,constrained_layout=True)
    # fig.suptitle('Oscilloscope Values')

    # Create Grid
    gs = fig.add_gridspec(len(channels), 1)

    colors = ['y','g','b','r']

    # Aquire data from the instrunment
    inst.write(':DIGitize')

    # Add the plots
    for i,channel in enumerate(channels):
        ax = fig.add_subplot(gs[i,0])
        ax.set_title('Channel %d'%channel)
        ax.set_ylabel(r'$V_{%d}$ [V]'%channel)
        ax.set_xlabel('Time [s]')

        v,t,_ = get_data(inst,channel=channel,points=points,acquire=False,VERBOSE=VERBOSE)

        ax.plot(t,v,c=colors[i],label='Channel %d'%channel)
        plt.legend(frameon=False)

    plt.show()

# OUTPUT TO CSV ##################################
def get_data_csv(inst,channels=[0,1,2,3,4],directory='./',filename=None,points=10000,VERBOSE=False):
    '''
    Export Oscilloscpe data to CSV
    
    inst: [REQUIRED] the instrunment object
    channels ([1,2,3,4]): List of channels to plot
    points (1000): Number of points to get data from
    filename (None): The filenmae of the CSV (if None it defaults to simestamp)
    directory (./): The directory to save the file
    VERBOSE (False): When True prints the preable
    '''

    if type(filename) == type(None):
        filename = '__time__.csv'

    titles = []
    DATA = []

    # Acquire new data
    inst.write(':DIGitize')

    for i,channel in enumerate(channels):
        v,t,_ = get_data(inst,channel=channel,points=points,acquire=False,VERBOSE=VERBOSE)

        titles.append('Channel %d Time'%channel)
        titles.append('Channel %d Voltage'%channel)
        DATA.append(t)
        DATA.append(v)

    create_csv(name=filename,directory=directory,titles=titles,data=DATA)


# GET ARDUINO ####################################
def get_arduino(ADDRESS='/dev/cu.usbmodem14101',VERBOSE=False):

    '''
    Returns a serial object that damps data to an arduino.

    ADDRESS (/dev/cu.usbmodem14101): USB Port for arduino
    VERBOSE (False): When True prints a confirmation message
    '''

    arduino = serial.Serial(port=ADDRESS,baudrate=115200,timeout=0.1)
    time.sleep(2)

    if VERBOSE: print("Successfully connected Arduino from port: "+ADDRESS)

    return arduino
