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
from MethodsFMH import CalculateParameters, CreateInterpolatedBurstCWT, CalculateMeanBurstsParameters


from perFreq import energy, CompareBE
import pywt

def EMG_Pre_P(emg):
	#filter
	emg = (emg - np.mean(emg))
	EMGFilt  = filter.bandpass(emg, f1=5, f2=500, fs=1000)
	EMGM = abs(EMGFilt)

	return EMGFilt, EMGM

def ACC_Pre_P(acc):
	acc = smooth(acc, window_len=100)

	return acc


def Segmentation(acc, emg):
	pks = detect_peaks(acc, mph=0.5*max(acc), mpd = 500)

	#Choose 10 first - 11 firstpks
	first = pks[:12]
	#and 10 last
	end = pks[-13:]

	#Find bigger gap between events:
	a = first[np.argmax(np.diff(first))]
	b = end[np.argmax(np.diff(end))]
	a_L = max(np.diff(first))
	b_L = max(np.diff(end))
	I_Bursts = []
	E_Bursts = []
	x_a = np.linspace(0, 100, a_L)
	x_b = np.linspace(0, 100, b_L)

	for i in range(1, len(first)):
		q = first[i-1]
		w = first[i]
		sig_temp = emg[q:w]

		if(len(sig_temp) < a_L):
			xp = np.linspace(0, 100, len(sig_temp))
			sig_temp = np.interp(x_a, xp, sig_temp)

		I_Bursts.append(sig_temp)

	for i in range(1, len(end)):
		q = end[i-1]
		w = end[i]
		sig_temp = emg[q:w]

		if(len(sig_temp) < b_L):
			xp = np.linspace(0, 100, len(sig_temp))
			sig_temp = np.interp(x_b, xp, sig_temp)

		E_Bursts.append(sig_temp)

	return I_Bursts, E_Bursts, first, end

def SegmentationCoefs(coefs, begin, end):
	CoefM1 = []
	CoefM2 = []
	a_L = max(np.diff(begin))
	b_L = max(np.diff(end))
	x_a = np.linspace(0, 100, a_L)
	x_b = np.linspace(0, 100, b_L)

	for i in range(0, len(coefs)):
		CoefTemp = coefs[i]
		CoefBegin = []
		CoefEnd = []
		for j in range(1, len(begin)):
			q = begin[j - 1]
			w = begin[j]
			sig_temp = CoefTemp[q:w]

			if (len(sig_temp) < a_L):
				xp = np.linspace(0, 100, len(sig_temp))
				sig_temp = np.interp(x_a, xp, sig_temp)

			CoefBegin.append(sig_temp)

		for j in range(1, len(end)):
			q = end[j - 1]
			w = end[j]
			sig_temp = CoefTemp[q:w]

			if (len(sig_temp) < b_L):
				xp = np.linspace(0, 100, len(sig_temp))
				sig_temp = np.interp(x_b, xp, sig_temp)

			CoefEnd.append(sig_temp)

		CoefM1.append(np.mean(CoefBegin, axis=0))
		CoefM2.append(np.mean(CoefEnd, axis=0))

	print(CoefM2)
	maxT =  np.maximum(np.abs(CoefM1).max(), np.abs(CoefM2).max())

	fig1 = plt.figure()
	ax1 = plt.subplot(2, 1, 1)
	ax1.imshow(CoefM1, cmap=cm.hot, aspect='auto', vmax=maxT, vmin=0)
	ax2 = plt.subplot(2, 1, 2)
	ax2.imshow(CoefM2, cmap=cm.hot, aspect='auto', vmax=maxT, vmin=0)
	plt.show()

def freq2scale(wavelet, frequency):

	return pywt.central_frequency(wavelet=wavelet)/frequency




#load signal #2
signals = np.loadtxt("Signals2/#3_EMG.txt")
start = 9093
end = 273433

#rectus femoralis
emg1 = signals[9093:273433, 3]
# emg1 = signals[9093:100000, 3]
#X
accx = signals[9093:273433, 8]
# accx = signals[9093:100000, 8]
accy = signals[9093:273433, 9]
accz = signals[9093:273433, 10]

#Pre-processing
EMG, EMG_M = EMG_Pre_P(emg1)
ACCX = ACC_Pre_P(accx)
ACCX = (ACCX - np.mean(ACCX))/max(ACCX)




#Segmentation
# CalculateEveryBurst(pks, cwt_map)
# Begin, End, Bindex, Eindex = Segmentation(ACCX, EMG)
pks = detect_peaks(ACCX, mph=0.5 * max(ACCX), mpd=500)


freqs = np.arange(5, 250, 2)
scales = 1000*freq2scale('morl', freqs)


# print(scales)
# scales = np.logspace(np.log10(3.28282828),np.log10(162.5), 200)
# scales = np.arange(1.56, 30, 1)
# print(1000*pywt.scale2frequency('morl', scale))
# print(scale)
#Wavelet
#Test with CWT and Complex Morlet wavelet:

coef, freqs=pywt.cwt(EMG, scales, 'morl', sampling_period=1/1000)

MeanBursts = CreateInterpolatedBurstCWT(coef, pks)
CalculateMeanBurstsParameters(MeanBursts)

# Thresholds= StartThresholdOtsu(coef, 100)





# # print(freqs)
# # #

#
# #Begin
# a = np.mean(Begin, axis=0)
# plt.plot(a)
# plt.show()
#
# #End
# b = np.mean(End, axis=0)
# plt.plot(b)
# plt.show()

# Wavelet
CoefBegin = np.zeros((len(scales), len(Begin[0])))

#Test with CWT and Complex Morlet wavelet:
SegmentationCoefs(coef, Bindex, Eindex)
# for i in range(0, len(Begin)):
# 	coef1, freqs1=pywt.cwt(Begin[i], scale, 'morl', sampling_period=1/1000)
# 	CoefBegin.append(coef1**2)
#
# for j in range(0, len(End)):
# 	coef2, freqs2 = pywt.cwt(End[j], scale, 'morl', sampling_period=1/1000)
# 	CoefEnd.append(coef2**2)
#
# CoefBStd = np.std(CoefBegin, axis=0)
# CoefEStd = np.std(CoefEnd, axis =0)
# CoefBegin = np.mean(CoefBegin, axis=0)
# CoefEnd = np.mean(CoefEnd, axis =0)
#
# # sss = pywt.threshold(CoefBegin, 0.5*CoefBegin.max(), 'hard')
#
# print(np.shape(CoefEnd))
# print(np.shape(CoefBStd))
#
# maxT = np.maximum(abs(CoefBegin).max(), abs(CoefEnd).max())
# maxT2 = np.maximum(abs(CoefEStd).max(), abs(CoefBStd).max())
#
# fig1 = plt.figure()
# ax1 = plt.subplot(2,1,1)
# ax1.imshow(CoefBegin, cmap=cm.hot, aspect='auto', vmax=maxT, vmin=0)
# ax2 = plt.subplot(2,1,2)
# ax2.imshow(CoefEnd, cmap=cm.hot, aspect='auto', vmax=maxT, vmin=0)
#
# fig2 = plt.figure()
# ax3 = plt.subplot(2,1,1)
# ax3.imshow(CoefBStd, cmap=cm.hot, aspect='auto', vmax=maxT, vmin=0)
# ax4 = plt.subplot(2,1,2)
# ax4.imshow(CoefEStd, cmap=cm.hot, aspect='auto', vmax=maxT, vmin=0)
#
# plt.show()
