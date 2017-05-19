import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import path
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

	# plt.hist(ImageArray, bins=256)
	# plt.vlines(Thresholds, ymin = 0, ymax=max(hist))
	# plt.show()

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


def WCentroid(Burst, OriginalBurst):
	lines = len(Burst)
	columns = len(Burst[0])
	# columns2 = len(OriginalBurst[0])

	BurstArrayX = np.concatenate(np.transpose(Burst))
	BurstArrayY = np.concatenate(Burst)

	# BurstArrayXO = np.concatenate(np.transpose(OriginalBurst))
	# BurstArrayYO = np.concatenate(OriginalBurst)

	centroidX = np.sum(np.multiply(range(0, len(BurstArrayX)), BurstArrayX)) / (np.sum(BurstArrayX))
	centroidY = np.sum(np.multiply(range(0, len(BurstArrayY)), BurstArrayY)) / (np.sum(BurstArrayY))

	# Calculate Area Correctly:
	burstarray = BurstArrayY[np.where(BurstArrayY > 0)[0]]
	pointsX = np.remainder(np.where(BurstArrayY > 0)[0], columns)
	pointsY = np.divide(np.where(BurstArrayY > 0)[0], columns)
	pointsV = np.transpose(np.array([pointsX, pointsY, burstarray]))
	pointsA = np.transpose(np.array([pointsX, pointsY]))

	# pointsXO = np.remainder(BurstArrayYO, columns2)
	# pointsYO = np.divide(BurstArrayYO, columns2)
	# pointsO = np.transpose(np.array([pointsXO, pointsYO]))

	hull = ConvexHull(pointsA)

	# plt.plot(pointsA[:, 0], pointsA[:, 1], 'o')
	# # plt.plot(pointsO[:, 0], pointsO[:, 1], 'yo')
	# for simplex in hull.simplices:
	# 	plt.plot(pointsA[simplex, 0], pointsA[simplex, 1], 'k-')
	# plt.show()

	area = hull.area
	vol = hull.volume

	# p = path.Path(pointsA[hull.vertices, :])
	# flags = p.contains_points(pointsO)
	# plt.plot(pointsO[flags, 0], pointsO[flags, 1], 'o')
	# print(flags)
	# print(pointsA[hull.vertices, :])

	X = int(centroidX // lines)
	Y = int(centroidY // columns)

	return (X, Y, area, vol, hull, pointsA)


def MeanPowerandArea(Burst):
	BurstArray = np.concatenate(Burst)
	PowerSum = np.sum(BurstArray)
	S = len(np.where(BurstArray > 0)[0])
	return PowerSum / S, S


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
		print(np.shape(cwtBurst))
		NewCwt.append(cwtBurst)

	print("calculating mean")
	MBursts = CalculateMeanBurst(15, NewCwt)

	# ax1=plt.subplot(1,1,1)
	# ax1.imshow(np.concatenate(MBursts, axis=1), cmap=cm.hot, aspect='auto')
	# plt.show()
	# mean over axis 0
	# concatenate over axis 1
	return MBursts


def CalculateMeanBurst(nBursts, cwt_map):
	MeanBursts = []
	for burst in range(0, len(cwt_map) - nBursts):
		M = np.mean(cwt_map[burst:burst + nBursts], axis=0)
		# plt.imshow(M, cmap=cm.hot, aspect='auto')
		# plt.show()
		# print(np.shape(M))
		MeanBursts.append(M)
	# print(np.shape(MeanBursts))
	return MeanBursts


def CalculateAV2(Burst):



	hull = ConvexHull(points)

	print(hull.equations)

	plt.plot(points[:, 0], points[:, 1], 'o')
	for simplex in hull.simplices:
		plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

	plt.show()

	vol = hull.volume


def CalculateMeanBurstsParameters(MeanBurstsMap):
	MajorFrequency = []
	BurstPos = []
	Area1 = []
	Area2 = []
	Vol = []
	MeanPower = []

	a, b, c = np.shape(MeanBurstsMap)
	MeanBurst= np.power(MeanBurstsMap, 2)
	Thresholds = StartThresholdOtsu(np.concatenate(MeanBurst, axis=1), 2048)
	# Find maximum value for map intensity
	maxT = np.max(MeanBurst)
	# select the area of the image that belongs to the 4th order of Otus threshold technique


	for burst in range(0, a):

		cwtBurst = MeanBurst[burst]
		# Find new Burst based on the thresholds

		newBurst = pywt.threshold(cwtBurst, Thresholds[1] * maxT, mode='greater')
		# newBurst = pywt.threshold(cwtBurst, Thresholds[2]*maxB, mode='less')
		# Calculate centroid
		X, Y, A, V, hull, points = WCentroid(newBurst, cwtBurst)

		# plt.figure()
		#
		# axis1 = plt.subplot(2,1,1)
		# axis1.set_title('Scalogram Map of the EMG signal')
		# axis1.imshow(np.concatenate(MeanBurst, axis=1), cmap=cm.hot, aspect='auto', vmax=maxT, vmin=0)
		# axis2 = plt.subplot(2, 1, 2)
		# axis2.set_title('Scalogram Map of a Burst')
		# axis2.imshow(cwtBurst, cmap=cm.hot, aspect='auto', vmax=maxT, vmin=0)
		# plt.show()
		#
		# plt.figure()
		# plt.title('Segmentation of the major intensity levels - Threshold Base')
		# ax3=plt.subplot(2, 1, 1)
		# ax3.set_title('Burst')
		# ax3.imshow(cwtBurst, cmap=cm.hot, aspect='auto', vmax=maxT, vmin=0)
		#
		# ax4 = plt.subplot(2, 1, 2)
		# ax4.set_title('Segemented Burst with 4th order threshold')
		# ax4.imshow(newBurst, cmap=cm.hot, aspect='auto', vmax=maxT, vmin=0)
		#
		# circ = Circle((X, Y), 5, label="Weighted Centroid")
		# ax4.add_patch(circ)
		#
		# for simplex in hull.simplices:
		# 	ax4.plot(points[simplex, 0], points[simplex, 1], 'b-')
		# plt.legend(facecolor='b')
		# plt.show()

		MP, PixArea = MeanPowerandArea(newBurst)
		MajorFrequency.append(Y)
		BurstPos.append(X / c)
		Area1.append(PixArea)
		Area2.append(A)
		Vol.append(V)
		MeanPower.append(MP)

	plt.figure()
	ax1 = plt.subplot(3, 1, 1)
	ax1.plot(Area1)
	ax1.set_title('Pixel Area')
	ax11 = plt.subplot(3,1,2)
	ax11.plot(Area2)
	ax11.set_title('Complex Hull Area')
	ax12 = plt.subplot(3, 1, 3)
	ax12.plot(Vol)
	ax12.set_title('Complex Hull Volume')


	plt.figure()
	ax2 = plt.subplot(3, 1, 1)
	ax2.plot(MeanPower)
	ax2.set_title('Mean Power')
	ax3 = plt.subplot(3, 1, 2)
	ax3.plot(MajorFrequency)
	ax3.set_title('Major Frequency')
	ax4 = plt.subplot(3, 1, 3)
	ax4.set_title('Centroid Position Over The Pedal Cicle')
	ax4.plot(BurstPos)

	plt.show()


def CalculateEachBurst(pks, cwt_map):
	MajorFrequency = []
	BurstPos = []
	Area1 = []
	Area2 = []
	Vol = []
	MeanPower = []

	L = max(np.diff(pks))
	x_i = np.linspace(0, 100, L)
	cwt_map = np.power(cwt_map, 2)
	maxT = np.max(cwt_map)


	for i in range(1, len(pks)):
		print(i)
		# select burst
		cwtBurst = cwt_map[:, pks[i - 1]:pks[i]]

		# Time interpolation [0-100]%
		cwtBurst = TimeInterpolation(cwtBurst, x_i)

		# Find maximum value for map intensity
		maxB = np.max(cwtBurst)

		# select the area of the image that belongs to the 4th order of Otus threshold technique
		Thresholds = StartThresholdOtsu(cwtBurst, 256)

		# Find new Burst based on the thresholds
		newBurst = pywt.threshold(cwtBurst, Thresholds[2] * maxB, mode='greater')
		A1 = len(np.where(newBurst>0)[0])
		# Calculate centroid
		X, Y, A2, V, Hull, points = WCentroid(newBurst, cwtBurst)

		# plt.figure()
		#
		# axis1 = plt.subplot(2,1,1)
		# axis1.set_title('Scalogram Map of the EMG signal')
		# axis1.imshow(cwt_map, cmap=cm.hot, aspect='auto', vmax=maxT, vmin=0)
		# axis2 = plt.subplot(2, 1, 2)
		# axis2.set_title('Scalogram Map of a Burst')
		# axis2.imshow(cwtBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)
		# plt.show()
		#
		# plt.figure()
		# plt.title('Segmentation of the major intensity levels - Threshold Base')
		# ax3=plt.subplot(2, 1, 1)
		# ax3.set_title('Burst')
		# ax3.imshow(cwtBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)
		#
		# ax4 = plt.subplot(2, 1, 2)
		# ax4.set_title('Segemented Burst with 4th order threshold')
		# ax4.imshow(newBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)
		#
		# circ = Circle((X, Y), 5, label="Weighted Centroid")
		# ax4.add_patch(circ)
		#
		# for simplex in Hull.simplices:
		# 	ax4.plot(points[simplex, 0], points[simplex, 1], 'b-')
		# plt.legend(facecolor='b')
		# plt.show()

		# Calculate MeanPower and Total Area in Pixels
		MP, area = MeanPowerandArea(newBurst)
		MajorFrequency.append(Y)
		BurstPos.append(X / L)
		Area1.append(area)
		Area2.append(A2)
		Vol.append(V)
		MeanPower.append(MP)

	plt.figure()
	ax1 = plt.subplot(3, 1, 1)
	ax1.plot(Area1)
	ax1.set_title('Pixel Area')
	ax11 = plt.subplot(3,1,2)
	ax11.plot(Area2)
	ax11.set_title('Complex Hull Area')
	ax12 = plt.subplot(3, 1, 3)
	ax12.plot(Vol)
	ax12.set_title('Complex Hull Volume')


	plt.figure()
	ax2 = plt.subplot(3, 1, 1)
	ax2.plot(MeanPower)
	ax2.set_title('Mean Power')
	ax3 = plt.subplot(3, 1, 2)
	ax3.plot(MajorFrequency)
	ax3.set_title('Major Frequency')
	ax4 = plt.subplot(3, 1, 3)
	ax4.set_title('Centroid Position Over The Pedal Cicle')
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
		# select burst
		cwtBurst = np.power(cwt_map[:, pks[i - 1]:pks[i]], 2)

		# Time interpolation [0-100]%
		cwtBurst = TimeInterpolation(cwtBurst, x_i)

		# Find maximum value for map intensity
		maxB = np.max(cwtBurst)

		# select the area of the image that belongs to the 4th order of Otus threshold technique
		Thresholds = StartThresholdOtsu(cwtBurst, 256)

		# Find new Burst based on the thresholds
		newBurst = pywt.threshold(cwtBurst, Thresholds[2] * maxB, mode='greater')
		# Calculate centroid
		X, Y = WCentroid(newBurst)

		# ax1=plt.subplot(2,1,1)
		# ax1.imshow(cwtBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)
		#
		# ax2 = plt.subplot(2,1,2)
		# ax2.imshow(newBurst, cmap=cm.hot, aspect='auto', vmax=maxB, vmin=0)
		# circ = Circle((X, Y), 5)
		# ax2.add_patch(circ)
		# plt.show()

		# Calculate MeanPower and Total Area in Pixels
		MP, area = MeanPowerandArea(newBurst)
		MajorFrequency.append(Y)
		BurstPos.append(X / L)
		Area.append(area)
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
