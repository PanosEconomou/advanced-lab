# Waveform Simulator after passing through the signal processing
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
import scipy.signal as signal
from tqdm import tqdm

#####################################################################################
# Here we define the relevevant components of the signal processing circuit
#####################################################################################

# Preamplifier design
def preamp(sig, gain = 1):
    return sig*gain

# Low pass Butterworth filter
def lowpass(sig,fc,fs,order=1):
    coeffs = signal.butter(order, 2*fc/fs)
    return signal.lfilter(coeffs[0],coeffs[1],signal)

# Lock in detector
def lock_in(sig,ref,gain=1,theta_0=0):
    return gain*(sig-theta_0)*(ref)

# low pass amplifier
def lowpass_amp(sig,time_constant,fs,gain=1):
    return gain*lowpass(sig,1/(2*np.pi*time_constant),fs,order=1)

# Oscillator signal
def oscillator(time,frequency,amplitude,phase=0,offset=0):
    return amplitude*np.cos(2*np.pi*frequency*time + phase) + offset

# White noise generator
def white_noise(time,amplitude=1):
    return np.random.normal(0,amplitude,time.shape)

# Polariser transfer function
def polariser(sig,delta_theta=0,amplitude=1):
    return amplitude*np.cos(sig+delta_theta)**2



#####################################################################################
# Here we perform the simulation of the signal
#####################################################################################

# Relevant Constants
Npts            = 10000                 # Number of sampling points
t_min           = 0                     # Minimum Time in s
t_max           = 3                     # Maximum Time in s
fs              = Npts/(t_max-t_min)    # Sampling Frequency
ANG_amplitude   = 0.1                   # Amplitude of roration angle
ANG_frequency   = 2                     # Frequency of rotation angle
ANG_phase       = 0                     # Phase of rotation angle
ANG_offset      = 0                     # Offset of rotation angle
polariser_angle = 0                     # Polariser Angle
sig_amplitude   = 1                     # Conversion from angle to signal amplitude
noise_amplitude = 0.1                   # Amplitude of white noise
preamp_gain     = 1                     # Gain of preamplifier
lpf_fc          = 1                     # Low pass filter cuttoff frequency in Hz
ref_phase       = 0                     # Phase of reference signal
lock_in_gain    = 1                     # Lock in gain
time_constant   = 1                     # Low pass filter amplifier time constant



# Generate Signal
time    = np.linspace(t_min,t_max,Npts)
ang     = oscillator(time,ANG_frequency,ANG_amplitude,ANG_phase,ANG_offset)
sig_raw = polariser(ang,polariser_angle,sig_amplitude) # + white_noise(time,noise_amplitude)
sig_pre = preamp(sig_raw,preamp_gain)

ref     = oscillator(time,ANG_frequency,1,ref_phase)

sig_loc = lock_in(sig_pre,ref,lock_in_gain)
sig_lpa = np.mean(sig_loc)*np.ones(time.shape)

thetas = np.linspace(0,2*np.pi,100)
voltage = []
for theta in thetas:
    ang     = oscillator(time,ANG_frequency,ANG_amplitude,ANG_phase,theta)
    sig_raw = polariser(ang,polariser_angle,sig_amplitude) # + white_noise(time,noise_amplitude)
    sig_pre = preamp(sig_raw,preamp_gain)

    ref     = oscillator(time,ANG_frequency,1,ref_phase)

    sig_loc = lock_in(sig_pre,ref,lock_in_gain,theta_0=polariser(preamp(theta)))
    voltage.append(np.mean(sig_loc))

voltage=np.array(voltage)
plt.plot(thetas,voltage)

# plt.plot(time,ang)
# plt.plot(time,ref)
# plt.plot(time,sig_pre)
# plt.plot(time,sig_loc)
# plt.plot(time,sig_lpa)

plt.show()