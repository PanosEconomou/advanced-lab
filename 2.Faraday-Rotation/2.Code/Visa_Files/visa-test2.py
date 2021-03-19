import pyvisa 
import numpy as np 
import matplotlib.pyplot as plt

# Connect to the Oscilloscope   ########################################
rm = pyvisa.ResourceManager()
print(rm.list_resources())
inst = rm.open_resource(rm.list_resources()[0])
print(inst.query("*IDN?"))


# Set up the waveform collection #######################################
inst.write(':WAVEFORM:SOURCE CHAN1')            # Source is Channel 1
inst.write(':WAVEFORM:POINTS 10000')            # Set the number of data points to collect
inst.write(':WAVEFORM:FORMAT ASCII')            # Set the format of the output data

# Collect the waveform parameters from the preamble
preamble = [float(i) for i in inst.query(':WAVEFORM:PREAMBLE?').split(',')]     
Npts = int(preamble[2])-1

dt = preamble[4]
t0 = preamble[5]+dt
t = np.linspace(t0,t0*Npts,Npts)

dy = preamble[7]
y0 = preamble[8]


# Obtain the actual data
values = [float(i) for i in inst.query(':WAV:DATA?').split(',')[1:]]

# PLOT ##################################
plt.plot(t,values)
plt.show()


# print(values)