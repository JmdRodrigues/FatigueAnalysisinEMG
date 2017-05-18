import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Circle
import pywt
from scipy.spatial import ConvexHull
from scipy.sparse import hstack
from novainstrumentation import smooth


def Prob(hist):
	w = np.sum(hist)
	return w

def ClassMeanLevels(hist, array, w):
	m = np.sum(np.multiply(hist, array)) / w

	return m

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
		#Recursive Thresholding
		counts = Image_hist[nbins_S:nbins_E]
		p = counts / sum(counts)
		new_end = nbins_E - nbins_S + 1
		sigmas = []
		#Calculate sigma
		for t in range(1, new_end):
			w0 = sum(p[0:t])
			w1 = sum(p[t+1:len(p)])
			miu0 = ClassMeanLevels(p[0:t], range(0, t), w0)
			miu1 = ClassMeanLevels(p[t+1:len(p)], range(t+1, len(p)), w1)
			sigma = w0 * w1 * (miu0 - miu1) ** 2
			sigmas.append(sigma)

		#Remove Nan sigmas
		sigmas = np.nan_to_num(sigmas)
		y = np.argmax(sigmas)
		y = nbins_S+y-1
		#recursive
		Thresholds_Left = RecMultiThresholdOtsu(Image_hist, nbins_S, y, 2 * curr, n)
		Thresholds_Right = RecMultiThresholdOtsu(Image_hist, y, nbins_E, 2 * curr + 1, n)

		if (np.logical_and(Thresholds_Left != -1, Thresholds_Right != -1)):
			Thresholds = [Thresholds_Left, y, Thresholds_Right]
		else:
			Thresholds = y

		return Thresholds

def WCentroid(Burst):
	lines = len(Burst)
	columns = len(Burst[0])

	BurstArrayX = np.concatenate(np.transpose(Burst))
	BurstArrayY = np.concatenate(Burst)

	centroidX = np.sum(np.multiply(range(0, len(BurstArrayX)), BurstArrayX))/(np.sum(BurstArrayX))
	centroidY = np.sum(np.multiply(range(0, len(BurstArrayY)), BurstArrayY))/(np.sum(BurstArrayY))
	
	#Calculate Area Correctly:
	burstarray = BurstArrayY[np.where(BurstArrayY>0)[0]]
	pointsX = np.remainder(np.where(BurstArrayY>0)[0], columns)
	pointsY = np.divide(np.where(BurstArrayY>0)[0], columns)
	points = np.transpose(np.array([pointsX, pointsY, burstarray]))
	# points  = np.reshape(np.array([pointsX, pointsY]), (len(pointsX), 2), 'F')

	hull = ConvexHull(points)

	# plt.plot(points[:, 0], points[:, 1], 'o')
	# for simplex in hull.simplices:
	# 	plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
	#
	# plt.show()
	area = hull.area
	vol = hull.volume

	X = int(centroidX // lines)
	Y = int(centroidY // columns)

	return (X, Y, area, vol)

def MeanPowerandArea(Burst):
	BurstArray = np.concatenate(Burst)
	PowerSum = np.sum(BurstArray)
	S = len(np.where(BurstArray>0)[0])
	return PowerSum/S, S

def CreateInterpolatedBurstCWT(cwt_map, pks):
	#Select each burst to organize in a timenormalize array of maps
	NewCwt = []
	L = max(np.diff(pks))
	x_i = np.linspace(0, 100, L)

	for pk in range(1, len(pks)):
		#EachBurst
		cwtBurst = cwt_map[:, pks[pk-1]:pks[pk]]
		# Time interpolation [0-100]%
		cwtBurst = TimeInterpolation(cwtBurst, x_i)
		print(np.shape(cwtBurst))
		NewCwt.append(cwtBurst)

	print("calculating mean")
	MBursts = CalculateMeanBurst(20, NewCwt)

	# ax1=plt.subplot(1,1,1)
	# ax1.imshow(np.concatenate(MBursts, axis=1), cmap=cm.hot, aspect='auto')
	# plt.show()
	#mean over axis 0
	#concatenate over axis 1
	return MBursts

def CalculateMeanBurst(nBursts, cwt_map):
	MeanBursts = []
	for burst in range(0, len(cwt_map)-nBursts):
		M = np.mean(cwt_map[burst:burst+nBursts], axis=0)
		# plt.imshow(M, cmap=cm.hot, aspect='auto')
		# plt.show()
		# print(np.shape(M))
		MeanBursts.append(M)
		# print(np.shape(MeanBursts))
	return MeanBursts

def CalculateAV2(Burst):
	#Add original Burst to select the total area withouth threshold
	lines = len(Burst)
	columns = len(Burst[0])

	BurstArrayX = np.concatenate(np.transpose(Burst))
	BurstArrayY = np.concatenate(Burst)


	frontZerosX = np.remainder(len(BurstArrayX) - len(np.trim_zeros(BurstArrayX, 'f')), columns)
	backZerosX = np.remainder(len(BurstArrayX) - len(np.trim_zeros(BurstArrayX, 'b')), columns)
	# pointsX = np.arange(frontZerosX, len(np.trim_zeros(BurstArrayX, 'b')), 1)
	frontZerosY = np.divide(len(BurstArrayX) - len(np.trim_zeros(BurstArrayY, 'f')), columns)
	backZerosY = np.divide(len(BurstArrayX) - len(np.trim_zeros(BurstArrayY, 'b')), columns)

	# pointsY = np.arange(frontZerosY, len(np.trim_zeros(BurstArrayY, 'b')), 1)

	# TrimY = np.trim_zeros(BurstArrayY)

	# Calculate Area Correctly:
	burstarray = BurstArrayY[np.where(BurstArrayY > 0)[0]]
	pointsX = np.remainder(np.where(BurstArrayY > 0)[0], columns)
	pointsY = np.divide(np.where(BurstArrayY > 0)[0], columns)

	plt.plot(pointsX, pointsY, 'o')
	plt.plot()


	points = np.transpose(np.array([pointsX, pointsY]))
	# points  = np.reshape(np.array([pointsX, pointsY]), (len(pointsX), 2), 'F')

	hull = ConvexHull(points)

	plt.plot(points[:, 0], points[:, 1], 'o')
	for simplex in hull.simplices:
		plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

	plt.show()

	vol = hull.volume


def CalculateMeanBurstsParameters(MeanBurstsMap):

	MajorFrequency = []
	BurstPos = []
	Area = []
	MeanPower = []

	a,b,c = np.shape(MeanBurstsMap)

	for burst in range(0, a):
		cwtBurst = np.power(MeanBurstsMap[burst], 2)

		#Find maximum value for map intensity
		maxB = np.max(cwtBurst)

		#select the area of the image that belongs to the 4th order of Otus threshold technique
		Thresholds = StartThresholdOtsu(cwtBurst, 256)

		#Find new Burst based on the thresholds
		newBurst = pywt.threshold(cwtBurst, Thresholds[2]*maxB, mode='greater')
		#Calculate centroid
		X, Y, A, V = WCentroid(newBurst)
		CalculateAV2(newBurst)
		# ax1=plt.subplot(2,1,1)
		# ax1.imshow(cwtBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)
        #
		# ax2 = plt.subplot(2,1,2)
		# ax2.imshow(newBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)
        #
		# circ = Circle((X, Y), 5)
		# ax2.add_patch(circ)
		# plt.show()

		MP, PixArea = MeanPowerandArea(newBurst)
		MajorFrequency.append(Y)
		BurstPos.append(X / c)
		Area.append(A)
		MeanPower.append(MP)

	ax1 = plt.subplot(4, 1, 1)
	ax1.plot(Area)
	ax2 = plt.subplot(4, 1, 2)
	ax2.plot(MeanPower)
	ax3 = plt.subplot(4, 1, 3)
	ax3.plot(MajorFrequency)
	ax4 = plt.subplot(4, 1, 4)
	ax4.plot(BurstPos)

	plt.show()

def CaclulateEachBurst(pks, cwt_map):
	MajorFrequency = []
	BurstPos = []
	Area = []
	MeanPower = []

	L = max(np.diff(pks))
	x_i = np.linspace(0, 100, L)

	for i in range(1, len(pks)):
		print(i)
		#select burst
		cwtBurst = np.power(cwt_map[:, pks[i-1]:pks[i]], 2)

		#Time interpolation [0-100]%
		cwtBurst = TimeInterpolation(cwtBurst, x_i)

		#Find maximum value for map intensity
		maxB = np.max(cwtBurst)

		#select the area of the image that belongs to the 4th order of Otus threshold technique
		Thresholds = StartThresholdOtsu(cwtBurst, 256)

		#Find new Burst based on the thresholds
		newBurst = pywt.threshold(cwtBurst, Thresholds[2]*maxB, mode='greater')
		#Calculate centroid
		X, Y, A = WCentroid(newBurst)

		# ax1=plt.subplot(2,1,1)
		# ax1.imshow(cwtBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)
        #
		# ax2 = plt.subplot(2,1,2)
		# ax2.imshow(newBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)

		# circ = Circle((X, Y), 5)
		# ax2.add_patch(circ)
		# plt.show()

		#Calculate MeanPower and Total Area in Pixels
		MP, area = MeanPowerandArea(newBurst)
		MajorFrequency.append(Y)
		BurstPos.append(X/L)
		Area.append(A)
		MeanPower.append(MP)

	ax1 = plt.subplot(4,1,1)
	ax1.plot(Area)
	ax2 = plt.subplot(4,1,2)
	ax2.plot(MeanPower)
	ax3 = plt.subplot(4,1,3)
	ax3.plot(MajorFrequency)
	ax4 = plt.subplot(4,1,4)
	ax4.plot(BurstPos)

	plt.show()

def CalculateParameters(pks, cwt_map):
	MajorFrequency = []
	BurstPos = []
	Area = []
	MeanPower = []

	L = max(np.diff(pks))
	x_i = np.linspace(0, 100, L)

	for i in range(1, len(pks)):
		print(i)
		#select burst
		cwtBurst = np.power(cwt_map[:, pks[i-1]:pks[i]], 2)

		#Time interpolation [0-100]%
		cwtBurst = TimeInterpolation(cwtBurst, x_i)

		#Find maximum value for map intensity
		maxB = np.max(cwtBurst)

		#select the area of the image that belongs to the 4th order of Otus threshold technique
		Thresholds = StartThresholdOtsu(cwtBurst, 256)

		#Find new Burst based on the thresholds
		newBurst = pywt.threshold(cwtBurst, Thresholds[2]*maxB, mode='greater')
		#Calculate centroid
		X, Y = WCentroid(newBurst)

		# ax1=plt.subplot(2,1,1)
		# ax1.imshow(cwtBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)
		#
		# ax2 = plt.subplot(2,1,2)
		# ax2.imshow(newBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)
		# circ = Circle((X, Y), 5)
		# ax2.add_patch(circ)
		# plt.show()

		#Calculate MeanPower and Total Area in Pixels
		MP, area = MeanPowerandArea(newBurst)
		MajorFrequency.append(Y)
		BurstPos.append(X/L)
		Area.append(area)
		MeanPower.append(MP)

	ax1 = plt.subplot(4,1,1)
	ax1.plot(Area)
	ax2 = plt.subplot(4,1,2)
	ax2.plot(MeanPower)
	ax3 = plt.subplot(4,1,3)
	ax3.plot(MajorFrequency)
	ax4 = plt.subplot(4,1,4)
	ax4.plot(BurstPos)

	plt.show()

def TimeInterpolation(Burst, X):

	InterpolatedBurst = []
	for i in range(0, len(Burst)):
		CoefTemp = Burst[i]
		xp = np.linspace(0, 100, len(CoefTemp))
		CoefTemp = np.interp(X, xp, CoefTemp)

		InterpolatedBurst.append(CoefTemp)

	return InterpolatedBurst


		# plt.figure()
		# ax1 = plt.subplot(2,1,1)
		# ax1.imshow(cwtBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)
		#
		# ax2 = plt.subplot(2,1,2)
		# ax2.imshow(newBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)

		# circ = Circle((X, Y), 5)
		# ax2.add_patch(circ)

		# plt.figure()
		# ax3 = plt.subplot(4,1,3)
		# ax3.hist(np.concatenate(cwtBurst), 256)

		# plt.show()



