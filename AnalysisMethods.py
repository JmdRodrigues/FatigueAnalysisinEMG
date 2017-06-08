import numpy as np
import pywt
import scipy.io as sio
from Methods import StartThresholdOtsu, WCentroid, MaxFreq, MeanP, CalculateMeanBurst, CalculateParameters
from PlottingSavers import plotParameters, plotEMG, PlotMap3, PlotParam3, plotEMG3D, plotBurst3D


def Analysis1(cwt_map, path, filename, pp):

	#Calculate Parameters
	MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height = CalculateParameters(
		cwt_map, 1)

	sio.savemat(path+"A1"+filename+".mat", mdict={"MajorF": MajorFrequency, "MeanPower": MeanPower1, "BurstPos":BurstPos, "Area":Area2, "Vol":Vol, "Width":Width, "Height":Height})

	plotParameters(MajorFrequency, MeanPower2, BurstPos, Width, Height, Area1, Area2, Vol, pp, Title="Each Burst Analysis", show=False)


def Analysis2(cwt_map, nbr, path, filename, pp):

	#GetMeanBursts
	cwt_map = CalculateMeanBurst(nbr, cwt_map)

	# Calculate all Parameters
	MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height = CalculateParameters(cwt_map, 2)

	sio.savemat(path + "A2" + filename + ".mat",
	            mdict={"MajorF": MajorFrequency, "MeanPower": MeanPower1, "BurstPos": BurstPos, "Area": Area2,
	                       "Vol": Vol, "Width": Width, "Height": Height})
	#Plot Things
	plotParameters(MajorFrequency, MeanPower2, BurstPos, Width, Height, Area1, Area2, Vol, pp, Title="Mean Burst Analysis", show=False)


def Analysis3(cwt_map, nbr, path, filename, pp):
	cwt_map = np.power(cwt_map, 2)

	Begin = np.mean(cwt_map[0:nbr], axis=0)
	End = np.mean(cwt_map[-nbr:], axis=0)
	cwtmap = np.array([Begin, End])

	Thresholds = StartThresholdOtsu(cwtmap, 2048)

	maxT = np.maximum(np.max(Begin), np.max(End))

	# Calculate all Parameters for Begin
	BeginParams = CalculateParameters(Begin, 3, Thresholds, maxT)
	# Calculate all Parameters for End
	EndParams = CalculateParameters(End, 3, Thresholds, maxT)

	hullAB = BeginParams[10]
	hullAE = EndParams[10]
	pointsB = BeginParams[11]
	pointsE = EndParams[11]
	coorB = (BeginParams[4]*100, BeginParams[0])
	coorE = (EndParams[4]*100, EndParams[0])

	sio.savemat(path + "A3" + filename + ".mat",
	            mdict={"MajorF_Begin": BeginParams[0], "MajorF_End": EndParams[0], "MeanPower_Begin": BeginParams[2],"MeanPower_Ending": EndParams[2], "BurstPos_Begin": BeginParams[4], "BurstPos_End": EndParams[4], "Area_Begin": BeginParams[5],
	                       "Area_End": EndParams[5], "Vol_Begin": BeginParams[7], "Vol_End": EndParams[7], "Width_Begin": BeginParams[8], "Width_End": EndParams[8], "Height_Begin": BeginParams[9], "Height_End": EndParams[9]})

	plotBurst3D(Begin, End, pp)
	PlotMap3(Begin, End, maxT, coorB, coorE, hullAB, hullAE, pointsB, pointsE, pp)
	PlotParam3(BeginParams, EndParams, pp)



# def Analysis4():
#
