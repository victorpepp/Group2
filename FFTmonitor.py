# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
import scipy.signal as sgn


"""
functions space
"""
#create a sin function signal with 3 base frequencies and its 3 first harmonics
def signalgenerator(frequencies, Fs, noise = True, signal = 0):
    
    for freq in frequencies:
        #base frequencies
        wave = (amplitude) * np.sin(2.0*np.pi*freq*t)
        
        #1st harmonics
        harmonic1 = (amplitude/2) * np.sin(2.0*np.pi*2*freq*t)
        
        signal += wave + harmonic1

    #creates noise
    # 0 is the mean of the normal distribution you are choosing from
    # 1 is the standard deviation of the normal distribution
    # last one is the number of elements you get in array noise
    
    if noise is True:
        noise = np.random.normal(0,1,Fs)
        signal += noise

    return signal

# Given 2 frequency values, creates a plot of the FFT in the interval
# delimited by them
def freqZoom(yf, xf, lowFreq, highFreq, limit = False):
    
    N = np.int(np.prod(yf.shape))
    ax = plt.figure().add_subplot(111)  
    ax.plot(xf[int(lowFreq):int(highFreq) + 1], 2.0/N * np.abs(yf[int(lowFreq):int(highFreq) + 1]))
    ax.grid()
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Amplitude')
    ax.set_xlim([int(lowFreq), int(highFreq)])
    message = "Ok"
    if limit != False:     
        ax.hlines(limit, int(lowFreq), int(highFreq) + 1, color = 'r')
        if np.max(2.0/N * np.abs(yf[int(lowFreq):int(highFreq) + 1])) >= limit:
            message = "Danger"
    ax.set_title("%.1f Hz to %.1f Hz - %s"%(lowFreq,highFreq,message))

#TODO: add a feature that monitor the amplitudes within the interval of freqZoom


"""
values space
"""
amplitude = 1.0

#in Hz

frequencies = [1000.0, 755.0, 355.0]

t = np.arange(0.0,1,25e-6)

#TODO: whats the best step for t variable so that we can have a good measuement?(considering the amount of harmonics)

"""
process
"""

N = np.int(np.prod(t.shape))# list length
Fs = 1/(t[1]-t[0]) 	# sample frequency
T = 1/Fs;
print("# Samples:", N)

signal = signalgenerator(frequencies, Fs)

"""
plots
"""

#Plot xy
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
ax1.plot(t, signal)
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel('Amplitude')
ax1.grid()
ax1.axis([0.0,0.1,-10*amplitude,10*amplitude])
ax1.set_title("Time Domain")

#FFT
fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
xf = np.linspace(0.0, 1.0/(2*T), N/2)
yf = fft(signal)
ax2.plot(xf, 2.0/N * np.abs(yf[0:np.int(N/2)]))
ax2.grid()
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Amplitude')
ax2.set_title("Frequency Domain")

freqZoom(yf,xf,0,1500, 0.8)
freqZoom(yf,xf,355,1000)


plt.show()
