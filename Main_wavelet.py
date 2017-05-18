import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn
from MF import PowerSpectrum, MF_calculus
from Peaks import detect_peaks
from smooth import smooth
from filter import bandpass
import pywt

# #load File
signal = np.loadtxt("Signals/botf4.txt")

# load channels and remove mean
emg1 = signal[:, 2]
emg1 = (emg1 - np.mean(emg1))/max(abs(emg1))
emg2 = signal[:, 3]
emg2 = (emg2 - np.mean(emg2))/max(abs(emg2))

#filter
filtsig = bandpass(emg2, 15, 450)

coef, freqs=pywt.cwt(filtsig, np.arange(1, 20, 1), 'morl', sampling_period=1/1000)
print(freqs)
plt.plot(coef[0])
plt.plot(coef[-1])
# plt.matshow(coef)
# plt.xlim((len(filtsig)-2000,len(filtsig)))
plt.show()

import pywt
import numpy as np
import matplotlib.pyplot as plt
x = np.arange(512)
y = np.sin(2*np.pi*x/32)
coef, freqs=pywt.cwt(y,np.arange(1,129),'gaus1')
plt.matshow(coef)
plt.show()


t = np.linspace(-1, 1, 200, endpoint=False)
sig  = np.cos(2 * np.pi * 7 * t) + np.real(np.exp(-7*(t-0.4)**2)*np.exp(1j*2*np.pi*2*(t-0.4)))
widths = np.arange(1, 4,0.01)
cwtmatr, freqs = pywt.cwt(sig, widths, 'mexh')
print(freqs)
plt.imshow(cwtmatr, extent=[-1, 1, 1, 31], cmap='PRGn', aspect='auto', vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
plt.show()