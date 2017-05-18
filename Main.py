import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn
from MF import PowerSpectrum, MF_calculus
from Peaks import detect_peaks
from smooth import smooth
from filter import bandpass

#load File
signal = np.loadtxt("Signals2/#2_EMG.txt")

#load channels and remove mean
emg1 = signal[:, 3]
emg1 = (emg1 - np.mean(emg1))/np.std((emg1))
emg2 = signal[:, 4]
emg2 = (emg2 - np.mean(emg2))/np.std((emg2))

plt.figure(0)
plt.plot(emg1)
plt.plot(emg2 - 2)

#filter
filtsig = bandpass(emg2, 15, 450)

# smooth ACC signal for segmentation
smSig = smooth(abs(filtsig), window_len=500)

plt.figure(1)
ax1 = plt.subplot(3,1,1)
ax1.plot(emg2/max(emg2))
ax1.plot(smSig/max(smSig))
ax2 = plt.subplot(3,1,2)
ax2.plot(emg2)
ax3 = plt.subplot(3,1,3)
ax3.plot(filtsig)
plt.show()

# find activation sites
maxPks = detect_peaks(smSig, mpd = 750)
# #minPks = detect_peaks(smSig, valley=True, show=False)
#
#
# MF
mfpre = np.array([])
#
plt.figure(1)
ax1 = plt.subplot(2,1,1)
ax1.plot(smSig*10)
ax1.plot(maxPks, smSig[maxPks], 'ro')
ax2 = plt.subplot(2,1,2)
ax2.plot(filtsig)
ax2.plot(maxPks, filtsig[maxPks], 'ro')
plt.title("Segmentation Plot of Cycling")
plt.xlabel("time (ms)")
plt.ylabel("Amplitude (V)")
#
#
plt.show()

# print("MAXPKSLEN : " + str(len(maxPks)))
#
for i in range(0, len(maxPks)):
    #calculate PSD
    f, Pxx = PowerSpectrum(filtsig[maxPks[i]-256:maxPks[i]+ 256], fs=1000)
    Mf = MF_calculus(Pxx)
    mfpre = np.append(mfpre, f[Mf])


plt.figure(2)
plt.suptitle("File: Arm Stressing")
ax1 = plt.subplot(3,1,1)
ax1.plot(emg2)
ax1.plot(smSig)
ax1.plot(maxPks, smSig[maxPks], 'ro')
ax1.set_xlim([0, len(filtsig)])
ax1.set_xlabel("time (ms)")
ax1.set_ylabel("Amplitude (V)")

ax2 = plt.subplot(3,1,2)
ax2.plot(filtsig)
ax2.plot(maxPks, filtsig[maxPks], 'ro')
ax2.set_xlim([0,len(filtsig)])

ax2.set_xlabel("time (ms)")
ax2.set_ylabel("Amplitude (V)")

ax3 = plt.subplot(3,1,3)
ax3.plot(maxPks, mfpre)
ax3.plot(maxPks, mfpre, 'ro')
ax3.set_xlim([0,len(filtsig)])

ax3.set_xlabel("time (ms)")
ax3.set_ylabel("MF (Hz)")

plt.show()