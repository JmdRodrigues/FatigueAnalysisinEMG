import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn
from MF import PowerSpectrum, MF_calculus
from Peaks import detect_peaks
from smooth import smooth
from novainstrumentation import filter
from matplotlib import cm
from perFreq import energy, CompareBE
import pywt

# #load File
signals = np.loadtxt("Signals2/#3_EMG.txt")
signal = np.zeros(np.shape(signals))
print(signal)
for i in range(3, 8):
	signal[:, i] = (signals[:, i] - np.mean(signals[:, i]))/np.std(signals[:, i])
	signal[:, i] = filter.bandpass(signal[:, i], 15, 450)

#rectus femoralis
emg1 = signal[:, 3]
#vastus lateralis
emg2 = signal[:, 4]
#vastus medialis
emg3 = signal[:, 5]
#semitendinous
emg4 = signal[:, 6]
#biceps femoris
emg5 = signal[:, 7]

#X
accx = signals[:, 8]
accx = filter.lowpass((accx - np.mean(accx)), f=10, fs=1000)
accx=accx/max(accx)
#Y
accy = signals[:, 9]
#Z
accz = signals[:, 10]


# plt.plot(signal[:, 8:11])
# plt.show()

#Test with CWT and Complex Morlet wavelet:
coef, freqs=pywt.cwt(emg1, np.arange(1.6, 30, 0.5), 'morl', sampling_period=1/1000)

# plt.plot(coef[-20])
# plt.plot(coef[1])
# plt.show()
print(freqs)
# ax1 = plt.subplot(2,1,1)
# print(freqs)
# energy(coef, freqs)
# CompareBE(emg2, coef, 10)

# for i in range(0, len(freqs)):
# 	coefM[i, :] = smooth(abs(coef[i, :]), window_len=500)


ax1 = plt.subplot(2,1,2)
ax1.imshow(abs(coef), cmap=cm.hot, aspect='auto', vmax=0.8*abs(coef).max(), vmin=0)
ax2 = plt.subplot(2,1,1)
ax2.plot(abs(emg1))
ax2.plot(accx)
# ax2 = plt.subplot(2,1,2)
# ax2.imshow(coef[:, -20000:-10000], cmap=cm.coolwarm, aspect='auto', vmax=abs(coef).max(), vmin=-abs(coef).max())
# plt.xlim((0, 500))
plt.show()

# x = np.linspace(0, len(emg2)/1000, len(emg2))
# X, Y = np.meshgrid(x, freqs)
# #
# fig = plt.figure()
# ax = Axes3D(fig)
# surf = ax.plot_surface(X=X, Y=Y, Z=coef, cmap=cm.RdYlGn, antialiased=False)
# plt.show()
# plt.plot(coef[-1])
# plt.plot(emg2)
# plt.show()
