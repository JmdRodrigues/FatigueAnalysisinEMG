import numpy as np
import pywt
from scipy.spatial import ConvexHull
from matplotlib import cm, path
from novainstrumentation import smooth, filter
from matplotlib.patches import Circle


def EMG_Pre_P(emg):

	emg = (emg - np.mean(emg))
	EMGFilt  = filter.bandpass(emg, f1=5, f2=500, fs=1000)

	return EMGFilt

def ACC_Pre_P(acc, fs):
	acc = smooth(acc, window_len=fs//10)

	return acc

def freq2scale(freqs, wavelet):
	return pywt.central_frequency(wavelet=wavelet) / freqs

def CreateInterpolatedBurstCWT(cwt_map, pks):
	# Select each burst to organize in a timenormalize array of maps
	NewCwt = []
	L = max(np.diff(pks))
	x_i = np.linspace(0, 100, L)

	for pk in range(1, len(pks)):
		# EachBurst
		cwtBurst = cwt_map[:, pks[pk - 1]:pks[pk]]
		# Time interpolation [0-100]%
		cwtBurst = TimeInterpolation(cwtBurst, x_i)
		NewCwt.append(cwtBurst)

	# mean over axis 0
	# concatenate over axis 1

	return NewCwt

def TimeInterpolation(Burst, X):
	InterpolatedBurst = []
	for i in range(0, len(Burst)):
		CoefTemp = Burst[i]
		xp = np.linspace(0, 100, len(CoefTemp))
		CoefTemp = np.interp(X, xp, CoefTemp)

		InterpolatedBurst.append(CoefTemp)

	return InterpolatedBurst

def StartThresholdOtsu(Image, nbins):
	ImageArray = np.concatenate(Image)
	hist, binsA = np.histogram(ImageArray, nbins)

	Thresholds = RecMultiThresholdOtsu(hist, 0, nbins, 1, 4)

	return np.divide(Thresholds, nbins)

def RecMultiThresholdOtsu(Image_hist, nbins_S, nbins_E, curr, n):

	if (curr >= n):
		Thresholds = -1
		return Thresholds

	else:

		# Recursive Thresholding
		counts = Image_hist[nbins_S:nbins_E]
		p = counts / sum(counts)
		new_end = nbins_E - nbins_S + 1
		sigmas = []
		# Calculate sigma
		for t in range(1, new_end):
			w0 = sum(p[0:t])
			w1 = sum(p[t + 1:len(p)])
			miu0 = ClassMeanLevels(p[0:t], range(0, t), w0)
			miu1 = ClassMeanLevels(p[t + 1:len(p)], range(t + 1, len(p)), w1)
			sigma = w0 * w1 * (miu0 - miu1) ** 2
			sigmas.append(sigma)

		# Remove Nan sigmas
		sigmas = np.nan_to_num(sigmas)
		y = np.argmax(sigmas)
		y = nbins_S + y - 1
		# recursive
		Thresholds_Left = RecMultiThresholdOtsu(Image_hist, nbins_S, y, 2 * curr, n)
		Thresholds_Right = RecMultiThresholdOtsu(Image_hist, y, nbins_E, 2 * curr + 1, n)

		if (np.logical_and(Thresholds_Left != -1, Thresholds_Right != -1)):
			Thresholds = [Thresholds_Left, y, Thresholds_Right]
		else:
			Thresholds = y

		return Thresholds

def Prob(hist):
	w = np.sum(hist)
	return w

def ClassMeanLevels(hist, array, w):
	m = np.sum(np.multiply(hist, array)) / w
	return m

def WCentroid(Burst, OriginalBurst):
	lines, columns = np.shape(OriginalBurst)

	#Create Arrays to find centroid in X and Y positions
	BurstArrayX = np.concatenate(np.transpose(Burst))
	BurstArrayY = np.concatenate(Burst)

	#Create array to find the total number of points that are present in that area
	TestRange = np.arange(0, lines*columns, 1)

	#Find Centroid X and Y positions
	centroidX = np.sum(np.multiply(range(0, len(BurstArrayX)), BurstArrayX)) / (np.sum(BurstArrayX))
	centroidY = np.sum(np.multiply(range(0, len(BurstArrayY)), BurstArrayY)) / (np.sum(BurstArrayY))

	#Calculate Area with Convex Hull
	burstarray = BurstArrayY[np.where(BurstArrayY > 0)[0]]                     #---> Array with which we can calulcate volum because it is the amplitudes of the wavelet map

	pointsX = np.remainder(np.where(BurstArrayY > 0)[0], columns)
	print(pointsX)

	width = max(pointsX) - min(pointsX)
	pointsY = np.divide(np.where(BurstArrayY > 0)[0], columns)
	print(pointsY)
	height = max(pointsY) - min(pointsY)

	#Create matrix for Area and Volume calculation
	pointsA = np.transpose(np.array([pointsX, pointsY])).astype(int)
	pointsV = np.transpose(np.array([pointsX, pointsY, burstarray]))

	#Find samples in that area
	pointsXO = np.remainder(TestRange, columns)
	pointsYO = np.divide(TestRange, columns)
	pointsO = np.transpose(np.array([pointsXO, pointsYO]))

	#Calculate Hull area and volume
	hullArea = ConvexHull(pointsA)
	hullVolume = ConvexHull(pointsV)
	area = hullArea.area
	vol = hullVolume.volume

	#Find which points belong to that area
	p = path.Path(pointsA[hullArea.vertices, :])
	flags = p.contains_points(pointsO)

	X = int(centroidX // lines)
	Y = int(centroidY // columns)

	return (X, Y, area, vol, hullArea, pointsA, pointsO[flags, 0].astype(int),  pointsO[flags, 1].astype(int), width, height)

def MaxFreq(map):
	return np.max(map)

def MeanP(map):
	return np.mean(map)

def CalculateMeanBurst(nBursts, cwt_map):
	MeanBursts = []
	for burst in range(0, len(cwt_map) - nBursts):
		M = np.mean(cwt_map[burst:burst + nBursts], axis=0)
		MeanBursts.append(M)

	return MeanBursts

def CalculateParameters(cwt_map, Analysis, Thresholds = None, maxT = None):

	# AllParameters
	MajorFrequency = []
	MaximumFrequency = []
	Width = []
	Height = []
	BurstPos = []
	Area1 = []
	Area2 = []
	Vol = []
	MeanPower1 = []
	MeanPower2 = []

	if Analysis == 2:

		# PowerofMap
		cwt_map = np.power(cwt_map, 2)

		# Size of each Burst
		L = len(cwt_map[0][0])

		# Get Shape items
		a, b, c = np.shape(cwt_map)

		# Find threshold values
		Thresholds = StartThresholdOtsu(np.concatenate(cwt_map, axis=1), 2048)

		# Define amximum value
		maxT = np.max(cwt_map)

		# For each burst in map
		for burst in range(0, a):
			# Select one burst
			cwtBurst = cwt_map[burst]

			# Find new Burst based on the thresholds
			newBurst = pywt.threshold(cwtBurst, Thresholds[1] * maxT, mode='greater')
			zeros = np.where(newBurst > 0)[0]
			if (np.max(newBurst) == 0 or len(zeros) < 20):
				continue
			else:
				# newBurst = pywt.threshold(cwtBurst, Thresholds[2]*maxB, mode='less')

				# Calculate centroid and other parameters
				X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height = WCentroid(newBurst, cwtBurst)

				# Maximum Frequency
				maxFreq = MaxFreq(cwtBurst[pointsOY, pointsOX])

				# MeanPower
				meanP1 = MeanP(cwtBurst[points[:, 1], points[:, 0]])
				meanP2 = MeanP(cwtBurst[pointsOY, pointsOX])

				# PixelArea
				area = len(points)

				# Fill Arrays
				MajorFrequency.append(Y)
				MaximumFrequency.append(np.max(cwtBurst[pointsOY, pointsOX]))
				MeanPower1.append(meanP1)
				MeanPower2.append(meanP2)
				BurstPos.append(np.divide(X, L))
				Area1.append(area)
				Area2.append(A)
				Vol.append(V)
				Width.append(width)
				Height.append(height)

	elif Analysis == 1:

		# PowerofMap
		cwt_map = np.power(cwt_map, 2)

		# Size of each Burst
		L = len(cwt_map[0][0])

		# Get Shape items
		a, b, c = np.shape(cwt_map)

		# Find threshold values
		Thresholds = StartThresholdOtsu(np.concatenate(cwt_map, axis=1), 512)
		print(Thresholds)

		# Define amximum value
		maxT = np.max(cwt_map)

		# For each burst in map
		for burst in range(0, a):
			# Select one burst
			cwtBurst = cwt_map[burst]

			# Find new Burst based on the thresholds
			newBurst = pywt.threshold(cwtBurst, Thresholds[1] * maxT, mode='greater')
			if(np.max(newBurst)==0 or len(np.where(newBurst>0)[0]) < 20):
				continue
			else:
				# newBurst = pywt.threshold(cwtBurst, Thresholds[2]*maxB, mode='less')

				# Calculate centroid and other parameters
				X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height = WCentroid(newBurst, cwtBurst)

				# Maximum Frequency
				maxFreq = MaxFreq(cwtBurst[pointsOY, pointsOX])

				# MeanPower
				meanP1 = MeanP(cwtBurst[points[:, 1], points[:, 0]])
				meanP2 = MeanP(cwtBurst[pointsOY, pointsOX])

				# PixelArea
				area = len(points)

				# Fill Arrays
				MajorFrequency.append(Y)
				MaximumFrequency.append(np.max(cwtBurst[pointsOY, pointsOX]))
				MeanPower1.append(meanP1)
				MeanPower2.append(meanP2)
				BurstPos.append(np.divide(X, L))
				Area1.append(area)
				Area2.append(A)
				Vol.append(V)
				Width.append(width)
				Height.append(height)

	elif Analysis == 3:
		# Size of each Burst
		L = len(cwt_map[0])

		cwtBurst = cwt_map

		# Find new Burst based on the thresholds
		newBurst = pywt.threshold(cwtBurst, Thresholds[2] * maxT, mode='greater')
		print(newBurst)
		if (np.max(newBurst) == 0):
			maxB = np.max(cwtBurst)
			# Find threshold values
			Thresholds2 = StartThresholdOtsu(cwtBurst, 1024)
			newBurst = pywt.threshold(cwtBurst, Thresholds2[2] * maxB, mode='greater')

		# Calculate centroid and other parameters
		X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height = WCentroid(newBurst, cwtBurst)

		# Maximum Frequency
		maxFreq = MaxFreq(cwtBurst[pointsOY, pointsOX])

		# MeanPower
		meanP1 = MeanP(cwtBurst[points[:, 1], points[:, 0]])
		meanP2 = MeanP(cwtBurst[pointsOY, pointsOX])

		# PixelArea
		area = len(points)

		# Fill Arrays
		MajorFrequency.append(Y)
		MaximumFrequency.append(np.max(cwtBurst[pointsOY, pointsOX]))
		MeanPower1.append(meanP1)
		MeanPower2.append(meanP2)
		BurstPos.append(np.divide(X, L))
		Area1.append(area)
		Area2.append(A)
		Vol.append(V)
		Width.append(width)
		Height.append(height)

		return (Y, MaximumFrequency, meanP1, meanP2, np.divide(X, L), area, A, V, width, height, hullA, points)

	return (MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height)