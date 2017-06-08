from Methods import EMG_Pre_P, freq2scale, CreateInterpolatedBurstCWT, ACC_Pre_P
from AnalysisMethods import Analysis1, Analysis2, Analysis3
from Peaks import detect_peaks
from PlottingSavers import plotEMG, plotEMG3D
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import scipy.io as sio
import pywt
import os


def extractPks(accX, fs):
	#filter acc
	acc = ACC_Pre_P(accX, fs)
	acc = (acc - np.mean(acc)) / max(acc)

	#find pks
	pks = detect_peaks(acc, mph=0.5 * max(acc), mpd=500)

	return pks

def Analysis(filename, path, signal, pks, fs, wavelet):

	#PreProcessing EMG
	emg = EMG_Pre_P(signal)

	#Calculate Scalogram
	frequencyRange = np.arange(5, 500, 4)
	scales = 1000*freq2scale(frequencyRange, wavelet)

	coef, freqs = pywt.cwt(emg, scales, wavelet, sampling_period=1 / fs)

	# Calculate meanBurstsParameters
	cwt_N = CreateInterpolatedBurstCWT(coef, pks)

	PDFName = filename + '.pdf'
	if not os.path.exists(path + "/" + PDFName[:-4]):
		os.makedirs(path + "/" + PDFName[:-4])
	pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis1_" + PDFName)

	#Plot1
	plotEMG(pks, emg, pp)
	# plotEMG3D(np.power(coef, 2), pp)
	print("Analysis1")
	#Anlysis of the signal for each burst
	Analysis1(cwt_N, path, filename, pp)

	pp.close()

	# #Anlysis of the signal for mean of bursts over the signal (5, 10 and 20)
	print("Analysis2")
	pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis2_" + PDFName)
	Analysis2(cwt_N, 10, path, filename, pp)
	pp.close()
	#Analysis of the beginning and the end of the signal
	print("Analysis3")
	pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis3_" + PDFName)
	Analysis3(cwt_N, 10, path, filename, pp)
	pp.close()
	# Analysis of the moving window over the spectogram
	# Analysis4