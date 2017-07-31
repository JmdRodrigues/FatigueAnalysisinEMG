import numpy as np
import pywt
from scipy.spatial import ConvexHull
from matplotlib import cm, path
from novainstrumentation import smooth, filter
from matplotlib.patches import Circle
import pylab as plt


def EMG_Pre_P(emg, fs):
    # DC Component Removal
    emg = (emg - np.mean(emg))

    # Signal full-wave rectification.
    # EMGFilt = np.absolute(emg)

    # Signal Filtering Stage.
    # EMGFilt  = filter.bandpass(emg, f1=5, f2=500, fs=1000)
    EMGFilt = filter.bandpass(emg, 20, 490, fs=fs)

    return EMGFilt


def ACC_Pre_P(acc, fs):
    # acc = filter.lowpass(acc, 15, 4, fs)
    acc = smooth(acc, window_len=fs // 10)

    return acc


def freq2scale(freqs, wavelet):
    return pywt.central_frequency(wavelet=wavelet) / freqs


def CreateInterpolatedBurstCWT(cwt_map, pks_start, pks_end):
    # Select each burst to organize in a timenormalize array of maps (Interpolation of data to obtain scalograms with similar dimension and equal to the length of the smallest burst).
    NewCwt = []
    delta_pks = pks_end - pks_start
    L = min(delta_pks)
    x_i = np.linspace(0, 100, L)

    for pk in range(0, len(pks_start) - 1):
        # EachBurst
        cwtBurst = cwt_map[:, pks_start[pk]:pks_end[pk]]
        # Time interpolation [0-100]%
        cwtBurst = TimeInterpolation(cwtBurst, x_i)
        NewCwt.append(cwtBurst)

    # mean over axis 0
    # concatenate over axis 1

    return NewCwt


# Line by line interpolation of Scalogram.
def TimeInterpolation(Burst, X):
    InterpolatedBurst = []
    for i in range(0, len(Burst)):
        CoefTemp = Burst[i]
        xp = np.linspace(0, 100, len(CoefTemp))
        CoefTemp = np.interp(X, xp, CoefTemp)

        InterpolatedBurst.append(CoefTemp)

    return InterpolatedBurst


def StartThresholdOtsu(Image):
    ImageArray = np.concatenate(Image)

    # Theoretical Approach.
    # nbins = int(1 + (np.log10(len(ImageArray)) / np.log10(2)))
    # nbins = int((np.ceil(nbins) // 2) * 2) # Procedure that guarantees that exists an even number of bins.
    nbins = 512

    # hist, binsA = np.histogram(ImageArray, 'auto')
    hist, binsA = np.histogram(ImageArray, nbins)

    Thresholds = RecMultiThresholdOtsu(hist, 0, nbins, 1, 4)
    # Thresholds = RecMultiThresholdOtsu(hist, 0, len(binsA) - 1, 1, 4)

    return np.divide(Thresholds, float(nbins))


# Original Version of the function StartThresholdOtsu.
# def StartThresholdOtsu_v1(Image, nbins):
# 	ImageArray = np.concatenate(Image)
# 	hist, binsA = np.histogram(ImageArray, nbins)
#
# 	Thresholds = RecMultiThresholdOtsu(hist, 0, nbins, 1, 4)
#
# 	return np.divide(Thresholds, float(nbins))

def RecMultiThresholdOtsu(Image_hist, nbins_S, nbins_E, curr, n):
    if (curr >= n):
        Thresholds = -1
        return Thresholds

    else:
        # Recursive Thresholding
        counts = Image_hist[nbins_S:nbins_E]
        p = counts / float(sum(counts))
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

        # Threshold that maximizes the inter-class variance, according to Otsu Method.
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
    #print (np.multiply(hist, array))
    #print (w)
    m = np.sum(np.multiply(hist, array)) / float(w)
    return m


def WCentroid(Burst, OriginalBurst, Analysis, FlagLessInformativeBurst=False):
    lines, columns = np.shape(OriginalBurst)

    # Create Arrays to find centroid in X and Y positions
    BurstArrayX = np.concatenate(np.transpose(Burst))
    BurstArrayY = np.concatenate(Burst)

    # Create array to find the total number of points that are present in that area
    TestRange = np.arange(0, lines * columns, 1)

    # Find Centroid X and Y positions
    centroidX = np.sum(np.multiply(range(0, len(BurstArrayX)), BurstArrayX)) / (np.sum(BurstArrayX))
    centroidY = np.sum(np.multiply(range(0, len(BurstArrayY)), BurstArrayY)) / (np.sum(BurstArrayY))

    if Analysis != 4:  # When Scalograms are "filtered" by the threshold of Otsus method.
        if FlagLessInformativeBurst == False:
            # Calculate Area with Convex Hull
            burstarray = BurstArrayY[np.where(BurstArrayY > 0)[0]]
            # ---> Array with which we can calulcate volume because it contains the amplitudes of the wavelet map
            # (Pixels with information).

            # Temporal dispersion of the Wavelet Components.
            pointsX = np.remainder(np.where(BurstArrayY > 0)[0], columns)
            width = max(pointsX) - min(pointsX)

            # Frequency dispersion of the Wavelet Components.
            pointsY = np.divide(np.where(BurstArrayY > 0)[0], columns)
            # pointsY = np.divide(np.where(BurstArrayY > 0)[0], lines)
            height = max(pointsY) - min(pointsY)

            # Find the number of each sample in that area
            pointsXO = np.remainder(TestRange, columns)
            pointsYO = np.divide(TestRange, columns)
            pointsO = np.transpose(np.array([pointsXO, pointsYO]))

            pointsA = np.transpose(np.array([pointsX, pointsY])).astype(int)
            pointsV = np.transpose(np.array([pointsX, pointsY, burstarray]))

            hullArea = ConvexHull(pointsA)
            area = hullArea.area

            # Find which points belong to that area
            p = path.Path(pointsA[hullArea.vertices, :])
            flags = p.contains_points(pointsO)

            hullVolume = ConvexHull(pointsV)
            vol = hullVolume.volume

            X = int(centroidX // lines)
            Y = int(centroidY // columns)

            return (X, Y, area, vol, hullArea, pointsA, pointsO[flags, 0].astype(int), pointsO[flags, 1].astype(int),
                    width, height)

        else:
            # Information Content.
            burstarray = BurstArrayY[np.where(BurstArrayY > 0)[0]]
            # ---> Array with which we can calculate volume because it contains the amplitudes of the wavelet map.

            # Temporal dispersion of the Wavelet Components.
            pointsX = np.remainder(np.where(BurstArrayY > 0)[0], columns)
            width = False

            # Frequency dispersion of the Wavelet Components.
            pointsY = np.divide(np.where(BurstArrayY > 0)[0], columns)
            height = False

            # Find the number of each sample in that area
            # pointsXO = np.remainder(TestRange, columns)
            # pointsYO = np.divide(TestRange, columns)
            pointsO = False

            pointsA = np.transpose(np.array([pointsX, pointsY])).astype(int)
            # pointsV = np.transpose(np.array([pointsX, pointsY, burstarray]))

            # Hull Parameters.
            hullArea = False
            area = False
            hullVolume = False
            vol = False

            X = int(centroidX // lines)
            Y = int(centroidY // columns)

            return (X, Y, area, vol, hullArea, pointsA, pointsO, pointsO, width, height)

    else:
        # Identification of Column and line numbers in 1D format, with the function divide and remainder.
        burstarray = BurstArrayY[np.where(BurstArrayY > 0)[0]]
        # ---> Array with which we can calulcate volume because it contain the amplitudes of the wavelet map.

        # Coordinate determination of each pixel.
        pointsX = np.remainder(np.where(BurstArrayY > 0)[0], columns)
        pointsY = np.divide(np.where(BurstArrayY > 0)[0], columns)

        hullVolume = ConvexHull(np.transpose(np.array([pointsX, pointsY, burstarray])))
        vol = hullVolume.volume

        X = int(centroidX // lines)
        Y = int(centroidY // columns)

        # Create matrix for Area and Volume calculation - "Preparation of information".
        # (Each entry will contain a 2D or 3D point coordinates - Very Ingenious)
        pointsA = np.transpose(np.array([pointsX, pointsY])).astype(int)

        return (X, Y, False, vol, False, pointsA, False, False, False, False)


def MaxFreq(map):
    return np.max(map)


def MeanP(map):
    return np.mean(map)


def CalculateMeanBurst(nBursts, cwt_map, ovr=False, lag=0):
    MeanBursts = []
    nbrBurst = []
    aux = 1

    # Generation of iteration sequence (A problematic scenario of erratic exclusion of the last burst is avoided).
    iterSeq = list(np.arange(0, len(cwt_map) - nBursts, nBursts))
    if (len(cwt_map) - nBursts) - iterSeq[-1] == nBursts:
        iterSeq.append(len(cwt_map) - nBursts)

    if ovr == False:
        for burst in iterSeq:
            M = np.mean(cwt_map[burst:burst + nBursts], axis=0)
            MeanBursts.append(M)
            nbrBurst.append(aux)
            aux = aux + 1
    else:
        for burst in np.arange(0, len(cwt_map) - nBursts, nBursts - lag):
            M = np.mean(cwt_map[burst:burst + nBursts], axis=0)
            MeanBursts.append(M)
            nbrBurst.append(aux)
            aux = aux + 1

    return MeanBursts, nbrBurst


def CalculateParameters(cwt_map, Analysis, Thresholds=None, maxT=None, nbr_Burst=None):
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
    result = []

    aux = 0

    # Preparatory Steps.
    if Analysis in [1, 2, 4, 5]:
        cwt_map = np.power(cwt_map, 2)

        # Size of each Burst
        L = len(cwt_map[0][0])

        # Get Shape items
        a, b, c = np.shape(cwt_map)

        # Define maximum value
        maxT = np.max(cwt_map)

    elif Analysis == 3:
        # Size of each Burst
        L = len(cwt_map[0])

    # Determination Phase.
    if Analysis == 1 or Analysis == 2:
        # Find threshold values
        Thresholds = StartThresholdOtsu(np.concatenate(cwt_map, axis=1))
        if type(Thresholds) is not list and type(Thresholds) is not np.ndarray:
            print('\t\tIncomplete Histogram Segmentation and OTSU Thresholding.')

        # For each burst in map
        for burst in range(0, a):  # With this mechanism the system analyse each window and do the slide.
            # Select one burst
            cwtBurst = cwt_map[burst]

            # Find new Burst based on the thresholds
            if type(Thresholds) is list or type(Thresholds) is np.ndarray:
                newBurst = pywt.threshold(cwtBurst, Thresholds[1] * maxT, mode='greater')
            else:
                newBurst = pywt.threshold(cwtBurst, Thresholds * maxT, mode='greater')

            # Identification of the points with information on scalogram.
            zeros = np.where(newBurst > 0)[0]

            if (np.max(newBurst) == 0 or len(zeros) == 0):  # Exclusion Criterium.
                # The "False" flag identifies an entry to remove in "PlottingSavers.py".
                [X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height, meanP1, meanP2, area] = [False, False,
                                                                                                        False, False,
                                                                                                        False, False,
                                                                                                        False, False,
                                                                                                        False, False,
                                                                                                        False, False,
                                                                                                        False]

            elif len(zeros > 0) and len(zeros) < 20:

                # Calculate centroid and other parameters
                X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height = WCentroid(newBurst, cwtBurst, Analysis,
                                                                                         True)

                # Maximum Frequency
                # maxFreq = MaxFreq(cwtBurst[pointsOY, pointsOX])

                # MeanPower
                # meanP1 = MeanP(cwtBurst)  # Mean Power of all points (with information) in the scalogram of the activation period.
                # meanP2 = MeanP(cwtBurst)
                meanP1 = MeanP(cwtBurst[points[:, 1], points[:, 0]])
                meanP2 = MeanP(cwtBurst[points[:, 1], points[:, 0]])

                # PixelArea (Points with information)
                area = len(points)

                # Exclusion of irrelevant indexes due to the present exclusion criterium (Redundant - Remove in Future Versions).
                [A, hullA, width, height] = [False, False, False, False]

            else:
                # Calculate centroid and other parameters
                X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height = WCentroid(newBurst, cwtBurst, Analysis)

                # Maximum Frequency
                maxFreq = MaxFreq(cwtBurst[pointsOY, pointsOX])

                # MeanPower
                meanP1 = MeanP(cwtBurst[points[:, 1], points[:,
                                                      0]])  # Mean Power of all points (with information) in the scalogram of the activation period.
                meanP2 = MeanP(cwtBurst[pointsOY, pointsOX])  # Mean power of points inside convex hull area.

                # PixelArea (Points with information)
                area = len(points)

            # Fill Arrays
            MajorFrequency.append(Y)

            if type(pointsOY) is 'list':
                MaximumFrequency.append(np.max(cwtBurst[pointsOY, pointsOX]))
            elif type(pointsOY) is 'bool':
                MaximumFrequency.append(np.max(cwtBurst))

            MeanPower1.append(meanP1)
            MeanPower2.append(meanP2)
            BurstPos.append(np.divide(X, L))
            Area1.append(area)
            Area2.append(A)
            Vol.append(V)
            Width.append(width)
            Height.append(height)

        return (MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height,
                nbr_Burst)

    elif Analysis == 3:
        cwtBurstB = cwt_map[0]
        cwtBurstE = cwt_map[1]

        # Find new Burst based on the thresholds
        newBurstB = pywt.threshold(cwtBurstB, Thresholds[1] * maxT, mode='greater')
        newBurstE = pywt.threshold(cwtBurstE, Thresholds[1] * maxT, mode='greater')
        # newBurst = pywt.threshold(cwtBurst, Thresholds[0] * maxT, mode='greater')#+_+

        if (np.max(newBurstB) == 0 or len(np.where(newBurstB > 0)[0]) < 20) or (
                np.max(newBurstE) == 0 or len(np.where(newBurstE > 0)[0]) < 20):  # Emergency Plan.
            newBurstB = pywt.threshold(cwtBurstB, Thresholds[0] * maxT, mode='greater')
            newBurstE = pywt.threshold(cwtBurstE, Thresholds[0] * maxT, mode='greater')
            if (np.max(newBurstB) == 0 or len(np.where(newBurstB > 0)[0]) < 20) or (
                    np.max(newBurstE) == 0 or len(np.where(newBurstE > 0)[0]) < 20):
                newBurstB = cwtBurstB
                newBurstE = cwtBurstE

            # maxB = np.max(cwtBurst)
            # Find threshold values
            # Thresholds2 = StartThresholdOtsu(cwtBurst)
            # newBurst = pywt.threshold(cwtBurst, Thresholds2[0] * maxB, mode='greater') #+_+ Using Thresholds2[0] as plan B we have results in this analysis that can't be compared with the remaining ones, because newBrust is generated in different conditions.

        newBursts = [newBurstB, newBurstE]
        oldBursts = [cwtBurstB, cwtBurstE]

        for i in range(0, 2):
            # Calculate centroid and other parameters
            X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height = WCentroid(newBursts[i], oldBursts[i],
                                                                                     Analysis)

            # Maximum Frequency
            maxFreq = MaxFreq(oldBursts[i][pointsOY, pointsOX])

            # MeanPower
            meanP1 = MeanP(oldBursts[i][points[:, 1], points[:, 0]])  # Mean Power of all points (with information) in the scalogram of the activation period.
            meanP2 = MeanP(oldBursts[i][pointsOY, pointsOX])  # Mean power of points inside convex hull area.

            # PixelArea
            area = len(points)
            MaximumPower = np.max(oldBursts[i][pointsOY, pointsOX])
            BurstPosition = np.divide(X, float(L))

            result.append(
                [Y, MaximumPower, meanP1, meanP2, BurstPosition, area, A, V, width, height, hullA, points, nbr_Burst])

        return result

    elif Analysis == 4:
        # For each burst in map
        for burst in range(0, a):  # With this mechanism the system analyse each window and do the slide.
            # Select one burst
            cwtBurst = cwt_map[burst]

            # Calculate centroid and other parameters
            X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height = WCentroid(cwtBurst, cwtBurst, Analysis)

            # Maximum Frequency
            maxFreq = MaxFreq(cwtBurst)

            # MeanPower
            # meanP1 = MeanP(cwtBurst) # Mean power of points inside convex hull area.
            meanP1 = MeanP(cwtBurst[points[:, 1], points[:, 0]])  # Mean power of points with information.

            # PixelArea
            area = len(points)

            # Fill Arrays
            MajorFrequency.append(Y)
            MaximumFrequency.append(np.max(cwtBurst))
            MeanPower1.append(meanP1)
            BurstPos.append(np.divide(X, L))
            # Area1.append(area)
            Vol.append(V)

        return (MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height,
                nbr_Burst)

    elif Analysis == 5:  # Analysis of Scalogram with less restrictive Otsu Methodology.
        # Find threshold values
        Thresholds = StartThresholdOtsu(np.concatenate(cwt_map, axis=1))

        # For each burst in map
        for burst in range(0, a):  # With this mechanism the system analyse each window and do the slide.
            # Select one burst
            cwtBurst = cwt_map[burst]

            # Find new Burst based on the thresholds.
            newBurst = pywt.threshold(cwtBurst, Thresholds[0] * maxT, mode='greater')
            zeros = np.where(newBurst > 0)[0]
            if (np.max(newBurst) == 0 or len(zeros) == 0):  # Exclusion Criterium.
                # The "False" flag identifies an entry to remove in "PlottingSavers.py".
                [X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height, meanP1, meanP2, area] = [False, False,
                                                                                                        False, False,
                                                                                                        False, False,
                                                                                                        False, False,
                                                                                                        False, False,
                                                                                                        False, False,
                                                                                                        False]

            elif len(zeros > 0) and len(zeros) < 20:
                # Calculate centroid and other parameters
                X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height = WCentroid(newBurst, cwtBurst, Analysis,
                                                                                         True)

                # Maximum Frequency
                # maxFreq = MaxFreq(cwtBurst[pointsOY, pointsOX])

                # MeanPower
                meanP1 = MeanP(cwtBurst[points[:, 1], points[:,
                                                      0]])  # Mean Power of all points (with information) in the scalogram of the activation period.
                # meanP2 = MeanP(cwtBurst[pointsOY, pointsOX])  # Mean power of points inside convex hull area.

                # PixelArea (Points with information)
                area = len(points)

                # Exclusion of irrelevant indexes due to the present exclusion criterium.
                [A, hullA, width, height, meanP2] = [False, False, False, False, False]

            else:
                # Calculate centroid and other parameters
                X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height = WCentroid(newBurst, cwtBurst, Analysis)

                # Maximum Frequency
                maxFreq = MaxFreq(cwtBurst[pointsOY, pointsOX])

                # MeanPower
                meanP1 = MeanP(cwtBurst[points[:, 1], points[:,
                                                      0]])  # Mean Power of all points (with information) in the scalogram of the activation period.
                meanP2 = MeanP(cwtBurst[pointsOY, pointsOX])  # Mean power of points inside convex hull area.

                # PixelArea
                area = len(points)

            # Fill Arrays
            MajorFrequency.append(Y)

            if type(pointsOY) is 'list':
                MaximumFrequency.append(np.max(cwtBurst[pointsOY, pointsOX]))
            elif type(pointsOY) is 'bool':
                MaximumFrequency.append(np.max(cwtBurst))

            MeanPower1.append(meanP1)
            MeanPower2.append(meanP2)
            BurstPos.append(np.divide(X, L))
            Area1.append(area)
            Area2.append(A)
            Vol.append(V)
            Width.append(width)
            Height.append(height)

        return (
        MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height, nbr_Burst)


# Original Version of the function CalculateParameters.
# def CalculateParameters_v1(cwt_map, Analysis, Thresholds = None, maxT = None):
#
# 	# AllParameters
# 	MajorFrequency = []
# 	MaximumFrequency = []
# 	Width = []
# 	Height = []
# 	BurstPos = []
# 	Area1 = []
# 	Area2 = []
# 	Vol = []
# 	MeanPower1 = []
# 	MeanPower2 = []
#
# 	if Analysis == 2:
#
# 		# PowerofMap
# 		cwt_map = np.power(cwt_map, 2)
#
# 		# Size of each Burst
# 		L = len(cwt_map[0][0])
#
# 		# Get Shape items
# 		a, b, c = np.shape(cwt_map)
#
# 		# Find threshold values
# 		Thresholds = StartThresholdOtsu(np.concatenate(cwt_map, axis=1), 2048)
#
# 		# Define amximum value
# 		maxT = np.max(cwt_map)
#
# 		# For each burst in map
# 		for burst in range(0, a): # With this mechanism the system analyse each window and do the slide.
# 			# Select one burst
# 			cwtBurst = cwt_map[burst]
#
# 			# Find new Burst based on the thresholds
# 			newBurst = pywt.threshold(cwtBurst, Thresholds[1] * maxT, mode='greater')
# 			zeros = np.where(newBurst > 0)[0]
# 			if (np.max(newBurst) == 0 or len(zeros) < 20):#+_+
# 				continue
# 			else:
# 				# newBurst = pywt.threshold(cwtBurst, Thresholds[2]*maxB, mode='less')
#
# 				# Calculate centroid and other parameters
# 				X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height = WCentroid(newBurst, cwtBurst, Analysis)
#
# 				# Maximum Frequency
# 				maxFreq = MaxFreq(cwtBurst[pointsOY, pointsOX])
#
# 				# MeanPower
# 				meanP1 = MeanP(cwtBurst[points[:, 1], points[:, 0]])
# 				meanP2 = MeanP(cwtBurst[pointsOY, pointsOX])
#
# 				# PixelArea
# 				area = len(points)
#
# 				# Fill Arrays
# 				MajorFrequency.append(Y)
# 				MaximumFrequency.append(np.max(cwtBurst[pointsOY, pointsOX]))
# 				MeanPower1.append(meanP1)
# 				MeanPower2.append(meanP2)
# 				BurstPos.append(np.divide(X, L))
# 				Area1.append(area)
# 				Area2.append(A)
# 				Vol.append(V)
# 				Width.append(width)
# 				Height.append(height)
#
# 	elif Analysis == 1:
#
# 		# PowerofMap
# 		cwt_map = np.power(cwt_map, 2)
#
# 		# Size of each Burst
# 		L = len(cwt_map[0][0])
#
# 		# Get Shape items
# 		a, b, c = np.shape(cwt_map)
#
# 		# Find threshold values
# 		Thresholds = StartThresholdOtsu(np.concatenate(cwt_map, axis=1), 512)
# 		#print ("Thresholds")
# 		#print(Thresholds)
#
# 		# Define amximum value
# 		maxT = np.max(cwt_map)
#
# 		# For each burst in map
# 		for burst in range(0, a):
# 			# Select one burst
# 			cwtBurst = cwt_map[burst]
#
# 			# Find new Burst based on the thresholds
# 			newBurst = pywt.threshold(cwtBurst, Thresholds[1] * maxT, mode='greater')
# 			if(np.max(newBurst)==0 or len(np.where(newBurst>0)[0]) < 20): #+_+
# 				continue
# 			else:
# 				# newBurst = pywt.threshold(cwtBurst, Thresholds[2]*maxB, mode='less')
#
# 				# Calculate centroid and other parameters
# 				X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height = WCentroid(newBurst, cwtBurst, Analysis)
#
# 				# Maximum Frequency
# 				maxFreq = MaxFreq(cwtBurst[pointsOY, pointsOX])
#
# 				# MeanPower
# 				meanP1 = MeanP(cwtBurst[points[:, 1], points[:, 0]])
# 				meanP2 = MeanP(cwtBurst[pointsOY, pointsOX])
#
# 				# PixelArea
# 				area = len(points)
#
# 				# Fill Arrays
# 				MajorFrequency.append(Y)
# 				MaximumFrequency.append(np.max(cwtBurst[pointsOY, pointsOX]))
# 				MeanPower1.append(meanP1)
# 				MeanPower2.append(meanP2)
# 				BurstPos.append(np.divide(X, L))
# 				Area1.append(area)
# 				Area2.append(A)
# 				Vol.append(V)
# 				Width.append(width)
# 				Height.append(height)
#
# 	elif Analysis == 3:
# 		# Size of each Burst
# 		L = len(cwt_map[0])
#
# 		cwtBurst = cwt_map
#
# 		# Find new Burst based on the thresholds
# 		newBurst = pywt.threshold(cwtBurst, Thresholds[1] * maxT, mode='greater')#+_+
# 		#print ("newBurst")
# 		#print(newBurst)
# 		if (np.max(newBurst) == 0 or len(np.where(newBurst>0)[0]) < 20): #+_+ Neste caso nao faz sentido ter um if else, pois possuimos apenas duas janelas temporais para estabelecer uma evolucao dos parametros, perdendo significado a comparacao se os escalogramas forem obtidos com limiares distintos.
# 			maxB = np.max(cwtBurst)
# 			# Find threshold values
# 			Thresholds2 = StartThresholdOtsu(cwtBurst, 1024)
# 			newBurst = pywt.threshold(cwtBurst, Thresholds2[0] * maxB, mode='greater') #+_+ Utilizando Thresholds[0] como plano de recurso para todas as analises mantemos a coerencia e a linearidade de interpretacao (identica em cada conjunto de resultados, pois foram gerados da mesma forma).
#
# 		# Calculate centroid and other parameters
# 		X, Y, A, V, hullA, points, pointsOX, pointsOY, width, height = WCentroid(newBurst, cwtBurst, Analysis)
#
# 		# Maximum Frequency
# 		maxFreq = MaxFreq(cwtBurst[pointsOY, pointsOX])
#
# 		# MeanPower
# 		meanP1 = MeanP(cwtBurst[points[:, 1], points[:, 0]])
# 		meanP2 = MeanP(cwtBurst[pointsOY, pointsOX])
#
# 		# PixelArea
# 		area = len(points)
#
# 		# Fill Arrays
# 		MajorFrequency.append(Y)
# 		MaximumFrequency.append(np.max(cwtBurst[pointsOY, pointsOX]))
# 		MeanPower1.append(meanP1)
# 		MeanPower2.append(meanP2)
# 		BurstPos.append(np.divide(X, float(L)))
# 		Area1.append(area)
# 		Area2.append(A)
# 		Vol.append(V)
# 		Width.append(width)
# 		Height.append(height)
#
# 		return (Y, MaximumFrequency, meanP1, meanP2, np.divide(X, L), area, A, V, width, height, hullA, points)
#
# 	return (MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height)

def filter_pks(pks_max, pks_min, fs):
    # Subdivide peaks (segment delimiters) into start and end points.
    pks_start_max = pks_max[:len(pks_max) - 1]
    pks_end_max = pks_max[1:len(pks_max)]
    pks_start_min = pks_min[:len(pks_min) - 1]
    pks_end_min = pks_min[1:len(pks_min)]
    delta_pks = pks_end_max - pks_start_max

    # Identification of the minimum duration of the activation periods, based on histographic analysis.
    # (The number of bins follows the Sturge Rule).
    hist, bins = np.histogram(delta_pks, int(1 + (np.log10(len(delta_pks)) / np.log10(2))))

    # Empirical Criterium for selection of min_interval duration.
    if bins[len(bins) - 1] - bins[0] < fs / 2:
        min_interval = np.floor(bins[0])
    else:
        min_interval = np.ceil(bins[1])

    # Remove wrong bursts (characterized by small dimension).

    # Phase 1 - Removal of small intervals.
    # pks_remove_1 = np.where(delta_pks < fs / 2)
    pks_remove_1 = np.where(delta_pks < np.floor(min_interval))
    pks_start_max = np.delete(pks_start_max, pks_remove_1, 0)
    pks_end_max = np.delete(pks_end_max, pks_remove_1, 0)

    # Phase 2 - Removal of outlier intervals (When the reference points for burst identification are the minimums of AccX).
    pks_remove_2 = np.where(pks_end_min - pks_start_min < np.floor(min_interval))

    pks_remove_2 = np.concatenate((pks_remove_1, pks_remove_2), 1)

    pks_start_min = np.delete(pks_start_min, pks_remove_2, 0)
    pks_end_min = np.delete(pks_end_min, pks_remove_2, 0)

    return pks_start_max, pks_end_max, pks_start_min, pks_end_min

    # Provisional Version of 16th of July of 2017 :) *-* (: ª-ª
