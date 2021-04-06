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

def fftnoise(f):
    f = np.array(f, dtype='complex')
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1:Np+1] *= phases
    f[-1:-1-Np:-1] = np.conj(f[1:Np+1])
    return np.fft.ifft(f).real

def band_limited_noise(min_freq, max_freq, samples=1024, samplerate=1):
    freqs = np.abs(np.fft.fftfreq(samples, 1/samplerate))
    f = np.zeros(samples)
    idx = np.where(np.logical_and(freqs>=min_freq, freqs<=max_freq))[0]
    f[idx] = 1
    return fftnoise(f)


# Preamplifier design
def preamp(sig, gain = 1):
    return sig*gain

# Low pass Butterworth filter
def lowpass(sig,fc,fs,order=1):
    coeffs = signal.butter(order, 2*fc/fs)
    return signal.lfilter(coeffs[0],coeffs[1],signal)

# Lock in detector
def lock_in(sig,ref,time,ref_freq,sigma=0,ref_shifted=None,gain=1):
    fs = len(time)/(max(time)-min(time))
    T = len(time)/fs
    
    if sigma == 0:
        X = np.sum(sig*ref/fs)*2/T
        Y = np.sum(sig*ref_shifted/fs)*2/T

        R   = (X**2+Y**2)**0.5
        phi = np.arctan(Y/X)

        return gain*(R*np.cos(2*np.pi*ref_freq*time+phi))*np.sign(ref)

    else:
        F = fft.fft(sig - np.mean(sig))
        F_freq = fft.fftfreq(len(F),d=1/fs)
        G  = (np.exp(-(F_freq-ref_freq)**2/sigma**2)+np.exp(-(F_freq+ref_freq)**2/sigma**2))

        FF = fft.ifft(F*G)
        FFF = FF.real
        return gain*FFF*np.sign(ref)

    

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
    "Npts"            : 100000,                # Number of sampling points
    "t_min"           : 0,                     # Minimum Time in s
    "t_max"           : 100,                   # Maximum Time in s
    "ANG_amplitude"   : 0.1,                   # Amplitude of roration angle
    "ANG_frequency"   : 3,                     # Frequency of rotation angle
    "ANG_phase"       : 0,                     # Phase of rotation angle
    "ANG_offset"      : np.pi*45/180,          # Offset of rotation angle
    "BG_amplitude"    : 0.03,                  # Amplitude of Background signal
    "BG_frequency"    : 3,                     # Frequency of Background signal
    "BG_phase"        : np.pi/2,               # Phase of Background signal
    "polariser_angle" : 0,                     # Polariser Angle
    "sig_amplitude"   : 1,                     # Conversion from angle to signal amplitude
    "noise_amplitude" : 0.01,                  # Amplitude of white noise
    "noise_min_freq"  : 0,                     # Minimum Frequency for noise
    "noise_max_freq"  : 0,                     # Maximum Frequency for noise
    "Noise_fs"        : 1,                     # Noise Sample Rate
    "preamp_gain"     : 1,                     # Gain of preamplifier
    "lpf_fc"          : 1,                     # Low pass filter cuttoff frequency in Hz
    "ref_phase"       : 0,                     # Phase of reference signal
    "lock_in_gain"    : 1,                     # Lock in gain
    "lock_in_std"     : 2,                     # Lock in standard deviation
    "time_constant"   : 1,                     # Low pass filter amplifier time constant
}

# Generate Signal
def get_signal(pars=params):
    # Get the time series
    time    = np.linspace(pars["t_min"],pars["t_max"],pars["Npts"])
    fs = len(time)/(max(time)-min(time))

    # Set an arbitrary polarisation angle for the light before the polariser
    ang     = oscillator(time,pars["ANG_frequency"],pars["ANG_amplitude"],pars["ANG_phase"],pars["ANG_offset"])

    # Obtain some noise
    noise_freq  = pars["noise_amplitude"]*band_limited_noise(pars["noise_min_freq"],pars["noise_max_freq"], samples=pars["Npts"], samplerate=pars["Noise_fs"])
    noise_white = white_noise(time,pars["noise_amplitude"])
    noise       = noise_freq+noise_white

    # Create a background signal 
    bg_sig = oscillator(time,pars["BG_frequency"],pars["BG_amplitude"],pars['BG_phase']*np.sin(4*pars["ANG_offset"]) - np.pi/2)

    # Get the signal from the optical sensor after it has passed from the polariser and pre amplifier (also add some noise)
    sig_raw = polariser(ang,pars["polariser_angle"],pars["sig_amplitude"]) + noise + bg_sig
    sig_pre = preamp(sig_raw,pars["preamp_gain"])

    # Generate the reference signal at the same frequency
    ref     = oscillator(time,pars["ANG_frequency"],1,pars["ref_phase"])
    ref_sh  = oscillator(time,pars["ANG_frequency"],1,pars["ref_phase"]+np.pi)

    # Pass the signal through the lock in amplifier
    sig_loc = lock_in(sig_pre,ref,time,pars["ANG_frequency"],sigma=pars["lock_in_std"],gain=pars["lock_in_gain"])
    # sig_loc = lock_in(sig_pre,ref,time,pars["ANG_frequency"],sigma=0,ref_shifted=ref_sh,gain=pars["lock_in_gain"])

    # Pass it thorugh the low pass filter amplifier
    sig_lpa = np.mean(sig_loc)*np.ones(time.shape)

    return time,ang,ref,sig_raw,sig_pre,sig_loc,sig_lpa

# time,ang,ref,sig_raw,sig_pre,sig_loc,sig_lpa = get_signal(params)