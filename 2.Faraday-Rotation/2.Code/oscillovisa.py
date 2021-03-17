# This is a library to interface with an osscilloscope and get data through VISA

import numpy as np
import pyvisa 

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

def get_data(inst,channel=1,points=1000, VERBOSE=False):
    '''
    Given an instrunment object it reads the waveform data and returns a time series of the voltage.

    inst: [REQUIRED] the instrunment object
    channel (1): int denotes the oscilloscope channel
    points (1000): Number of points to get data from
    VERBOSE (False): When True prints the preable

    Returns --------------
    
    '''

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
    values = [float(i) for i in inst.query(':WAV:DATA?').split(',')[1:]]

    # Return everything
    return values,t,[Npts,dt,t0,dy,y0]