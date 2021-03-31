# Waveform Simulator after passing through the signal processing
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import scipy.constants as const
import scipy.signal as signal
import numpy.fft as fft
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
def lock_in(sig,ref,ref_shifted,ref_freq,time,gain=1):
    fs = len(time)/(max(time)-min(time))
    T = len(time)/fs
    
    X = np.sum(sig*ref/fs)*2/T
    Y = np.sum(sig*ref_shifted/fs)*2/T

    R   = (X**2+Y**2)**0.5
    phi = np.arctan(Y/X)


    return gain*(R*np.cos(2*np.pi*ref_freq*time+phi))*np.sign(ref)

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
params = {
    "Npts"            : 10000,                 # Number of sampling points
    "t_min"           : 0,                     # Minimum Time in s
    "t_max"           : 3,                     # Maximum Time in s
    "ANG_amplitude"   : 0.1,                   # Amplitude of roration angle
    "ANG_frequency"   : 2,                     # Frequency of rotation angle
    "ANG_phase"       : 0,                     # Phase of rotation angle
    "ANG_offset"      : np.pi/4,                     # Offset of rotation angle
    "polariser_angle" : 0,                     # Polariser Angle
    "sig_amplitude"   : 1,                     # Conversion from angle to signal amplitude
    "noise_amplitude" : 0.1,                   # Amplitude of white noise
    "preamp_gain"     : 1,                     # Gain of preamplifier
    "lpf_fc"          : 1,                     # Low pass filter cuttoff frequency in Hz
    "ref_phase"       : 0,                     # Phase of reference signal
    "lock_in_gain"    : 1,                     # Lock in gain
    "time_constant"   : 1,                     # Low pass filter amplifier time constant
}

# Generate Signal
def get_signal(pars):
    time    = np.linspace(pars["t_min"],pars["t_max"],pars["Npts"])
    ang     = oscillator(time,pars["ANG_frequency"],pars["ANG_amplitude"],pars["ANG_phase"],pars["ANG_offset"])
    sig_raw = polariser(ang,pars["polariser_angle"],pars["sig_amplitude"]) # + white_noise(time,noise_amplitude)
    sig_pre = preamp(sig_raw,pars["preamp_gain"])

    ref     = oscillator(time,pars["ANG_frequency"],1,pars["ref_phase"])
    ref_sh  = oscillator(time,pars["ANG_frequency"],1,pars["ref_phase"]+np.pi)

    sig_loc = lock_in(sig_pre,ref,ref_sh,pars["ANG_frequency"],time,pars["lock_in_gain"])
    sig_lpa = np.mean(sig_loc)*np.ones(time.shape)

    return time,ang,ref,sig_raw,sig_pre,sig_loc,sig_lpa

time,ang,ref,sig_raw,sig_pre,sig_loc,sig_lpa = get_signal(params)

fig = plt.figure(figsize=(10,6),dpi=120)
ax = fig.add_subplot(111)

l,= ax.plot(time,sig_loc,label='Lock-in')

def on_theta(text):
    theta = float(text)
    params['ANG_offset'] = np.pi/180*theta
    time,ang,ref,sig_raw,sig_pre,sig_loc,sig_lpa = get_signal(params)
    l.set_ydata(sig_loc)
    plt.draw()

def on_phase(text):
    phase = float(text)
    params['ref_phase'] = np.pi/180*phase
    time,ang,ref,sig_raw,sig_pre,sig_loc,sig_lpa = get_signal(params)
    l.set_ydata(sig_loc)
    plt.draw()

theta_box = plt.axes([0.1, 0.0, 0.1, 0.075])
theta_text_box = TextBox(theta_box, 'Theta', initial='0')
theta_text_box.on_submit(on_theta)

phase_box = plt.axes([0.5, 0.0, 0.1, 0.075])
phase_text_box = TextBox(phase_box, 'Phase', initial='0')
phase_text_box.on_submit(on_phase)

# ax.plot(time,ang,label='Angle')
# ax.plot(time,ref,label='Reference')
# ax.plot(time,sig_pre,label='Preamp')


plt.legend(frameon=False)
plt.show()