import numpy as np
import pywt
import scipy.io as sio
from Methods import StartThresholdOtsu, WCentroid, MaxFreq, MeanP, CalculateMeanBurst, CalculateParameters
from PlottingSavers import plotParameters, plotEMG, PlotMap3, PlotParam3, plotEMG3D, plotBurst3D
from AuxiliaryMethods import PandaConstruct


# Burst by Burst Analysis.
def Analysis1(cwt_map, path, filename, pp):
    # Calculate Parameters
    MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height, nbr_Burst = CalculateParameters(
        cwt_map, 1, nbr_Burst=np.arange(1, len(cwt_map) + 1))

    # Creation of .mat file.
    sio.savemat(path + "/A1" + filename + ".mat",
                mdict={"MajorF": MajorFrequency, "MeanPower": MeanPower1, "BurstPos": BurstPos, "Area": Area2,
                       "Vol": Vol, "Width": Width, "Height": Height})

    # Generation of pdf Report.
    plotParameters(MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1, Area2, Vol, pp,
                   Title="Each Burst Analysis", analysis=1, nbr_Burst=nbr_Burst, show=False)


# Analysis of Sets of Bursts (Analysis 2 --> From a filtered Scalogram with Otsu Thresholds; Analysis 4 --> From the original Scalogram).
def Analysis2_4(cwt_map, nbr, path, filename, pp, type, lag=0, analysis=2, txt_data=None, txt_data_global=None,
                pandaData=None, final=False, pandaDataMuscle=None, radarData=None, muscleIndex=0, muscleName=None):
    # Replication of data.
    txt_data_aux = txt_data

    # Data storage for generation of a txt file.
    txt_data.append(analysis)
    txt_data.append(lag)

    if type == "Original_Analysis":  # It is a specialization of the clause "Overlap Analysis".
        # GetMeanBursts
        cwt_map, nbr_Burst = CalculateMeanBurst(nbr, cwt_map, True, nbr - 1)
        lag = nbr - 1

        # Calculate all Parameters
        MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height, nbr_Burst = CalculateParameters(
            cwt_map, analysis, nbr_Burst=nbr_Burst)

        # Creation of .mat file.
        sio.savemat(path + "/A2_Orig" + filename + ".mat",
                    mdict={"MajorF": MajorFrequency, "MeanPower": MeanPower1, "BurstPos": BurstPos, "Area": Area2,
                           "Vol": Vol, "Width": Width, "Height": Height})

        # Generation of pdf Report.
        if analysis == 2:
            txt_data_global = plotParameters(MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1, Area2, Vol, pp,
                                             Title="Mean Burst Original Analysis (Windows length " + str(
                                                 nbr) + " lag " + str(lag) + ")", analysis=analysis,
                                             nbr_Burst=nbr_Burst, show=False, txt_data_temp=txt_data,
                                             txt_data_global=txt_data_global)
        else:
            txt_data_global = plotParameters(MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1, Area2, Vol, pp,
                                             Title="Mean Burst Original Analysis (Windows length " + str(
                                                 nbr) + " lag " + str(lag) + ")", analysis=analysis,
                                             nbr_Burst=nbr_Burst, show=False, txt_data_temp=txt_data,
                                             txt_data_global=txt_data_global)

    elif type == "Overlap_Analysis":
        # GetMeanBursts
        cwt_map, nbr_Burst = CalculateMeanBurst(nbr, cwt_map, True, lag)

        # Calculate all Parameters
        MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height, nbr_Burst = CalculateParameters(
            cwt_map, analysis, nbr_Burst=nbr_Burst)

        # Creation of .mat file.
        sio.savemat(path + "/A2_Perc_nOvr" + filename + ".mat",
                    mdict={"MajorF": MajorFrequency, "MeanPower": MeanPower1, "BurstPos": BurstPos, "Area": Area2,
                           "Vol": Vol, "Width": Width, "Height": Height})

        # Generation of pdf Report.
        if analysis == 2:
            txt_data_global = plotParameters(MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1, Area2, Vol, pp,
                                             Title="Mean Burst Analysis - Overlapping Windows (Windows length " + str(
                                                 nbr) + " lag " + str(lag) + ")", nbr_Burst=nbr_Burst,
                                             analysis=analysis, show=False, txt_data_temp=txt_data,
                                             txt_data_global=txt_data_global)
        else:
            txt_data_global = plotParameters(MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1, Area2, Vol, pp,
                                             Title="Mean Burst Analysis - Overlapping Windows (Windows length " + str(
                                                 nbr) + " lag " + str(lag) + ")", analysis=analysis,
                                             nbr_Burst=nbr_Burst, show=False, txt_data_temp=txt_data,
                                             txt_data_global=txt_data_global)

            # Stage of Panda Structure generation used in graphical synthesis of the results.
            if pandaData is not None and pandaDataMuscle is not None:
                panda_data = PandaConstruct(subject=txt_data_aux[0], muscle=txt_data_aux[1],
                                            paramName=['Major_Frequency', 'Mean_Power', 'Centroid_Postion',
                                                       'Time_Dispersion', 'Frequency_Dispersion', 'Area_in_Pixels',
                                                       'Convex_Hull_Area', 'Convex_Hull_Volume'],
                                            paramValues=[MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1,
                                                         Area2, Vol], time=nbr_Burst, panda_data=pandaData)
                panda_data_muscle = PandaConstruct(subject=txt_data_aux[0], muscle=txt_data_aux[1],
                                                   paramName=['Major_Frequency', 'Mean_Power', 'Centroid_Postion',
                                                              'Time_Dispersion', 'Frequency_Dispersion',
                                                              'Area_in_Pixels', 'Convex_Hull_Area',
                                                              'Convex_Hull_Volume'],
                                                   paramValues=[MajorFrequency, MeanPower1, BurstPos, Width, Height,
                                                                Area1, Area2, Vol], time=nbr_Burst,
                                                   panda_data=pandaDataMuscle)
                return txt_data_global, panda_data, panda_data_muscle

            else:
                return txt_data_global

    elif type == "Non_Overlap_Analysis":
        # GetMeanBursts
        cwt_map, nbr_Burst = CalculateMeanBurst(nbr, cwt_map, False)

        # Calculate all Parameters
        MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height, nbr_Burst = CalculateParameters(
            cwt_map, analysis, nbr_Burst=nbr_Burst)

        # Creation of .mat file.
        sio.savemat(path + "/A2_Perc_nOvr" + filename + ".mat",
                    mdict={"MajorF": MajorFrequency, "MeanPower": MeanPower1, "BurstPos": BurstPos, "Area": Area2,
                           "Vol": Vol, "Width": Width, "Height": Height})

        # Generation of pdf Report.
        if analysis == 2:
            txt_data_global = plotParameters(MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1, Area2, Vol, pp,
                                             Title="Mean Burst Analysis - Non Overlapping Windows (Windows length " + str(
                                                 nbr) + " lag " + str(lag) + ")", analysis=analysis,
                                             nbr_Burst=nbr_Burst, show=False, txt_data_temp=txt_data,
                                             txt_data_global=txt_data_global)
        else:
            txt_data_global = plotParameters(MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1, Area2, Vol, pp,
                                             Title="Mean Burst Analysis - Non Overlapping Windows (Windows length " + str(
                                                 nbr) + " lag " + str(lag) + ")", analysis=analysis,
                                             nbr_Burst=nbr_Burst, show=False, txt_data_temp=txt_data,
                                             txt_data_global=txt_data_global)

            # Radar Data - Fill of Strucutre.
            radarData[muscleIndex + 1] = radarData[muscleIndex + 1] + (muscleName,)
            radarData[muscleIndex + 1] = radarData[muscleIndex + 1] + (MeanPower1,)

    return txt_data_global, radarData

# Study of the binary evolution of extracted indexes between the start and beginning of acquisition.
def Analysis3(cwt_map, nbr, path, filename, pp):
    cwt_map = np.power(cwt_map, 2)

    Begin = np.mean(cwt_map[0:nbr], axis=0)
    End = np.mean(cwt_map[-nbr:], axis=0)
    cwtmap = np.array([Begin, End])

    Thresholds = StartThresholdOtsu(cwtmap)

    maxT = np.maximum(np.max(Begin), np.max(End))

    # Calculate all Parameters for Begin and End.
    Params = CalculateParameters([Begin, End], 3, Thresholds, maxT)

    BeginParams = Params[0]
    EndParams = Params[1]

    hullAB = BeginParams[10]
    hullAE = EndParams[10]
    pointsB = BeginParams[11]
    pointsE = EndParams[11]
    coorB = (BeginParams[4] * 100, BeginParams[0])
    coorE = (EndParams[4] * 100, EndParams[0])

    # Creation of .mat file.
    sio.savemat(path + "/A3" + filename + ".mat",
                mdict={"MajorF_Begin": BeginParams[0], "MajorF_End": EndParams[0], "MeanPower_Begin": BeginParams[2],
                       "MeanPower_Ending": EndParams[2], "BurstPos_Begin": BeginParams[4], "BurstPos_End": EndParams[4],
                       "Area_Begin": BeginParams[5], "Area_End": EndParams[5], "Vol_Begin": BeginParams[7],
                       "Vol_End": EndParams[7], "Width_Begin": BeginParams[8], "Width_End": EndParams[8],
                       "Height_Begin": BeginParams[9], "Height_End": EndParams[9]})

    # Generation of pdf Report.
    plotBurst3D(Begin, End, pp, maxT, nbr)
    PlotMap3(Begin, End, maxT, coorB, coorE, hullAB, hullAE, pointsB, pointsE, pp, nbr)
    PlotParam3(BeginParams, EndParams, pp, nbr)


def Analysis5(cwt_map, nbr, path, filename, pp, type, lag=0, analysis=5, txt_data=None, txt_data_global=None,
              pandaData=None, final=False,
              pandaDataMuscle=None):  # Analysis of Scalogram with a less restrictive Otsu thresholds.
    # Replication of data.
    txt_data_aux = txt_data

    # Data storage for generation of a txt file.
    txt_data.append(analysis)
    txt_data.append(lag)

    if type == "Original_Analysis":  # It is a specialization of the clause "Overlap Analysis".
        # GetMeanBursts
        cwt_map, nbr_Burst = CalculateMeanBurst(nbr, cwt_map, True, nbr - 1)
        lag = nbr - 1

        # Calculate all Parameters
        MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height, nbr_Burst = CalculateParameters(
            cwt_map, analysis, nbr_Burst=nbr_Burst)

        # Creation of .mat file.
        sio.savemat(path + "/A5_Orig" + filename + ".mat",
                    mdict={"MajorF": MajorFrequency, "MeanPower": MeanPower1, "BurstPos": BurstPos, "Area": Area2,
                           "Vol": Vol, "Width": Width, "Height": Height})

        # Generation of pdf Report.
        txt_data_global = plotParameters(MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1, Area2, Vol, pp,
                                         Title="Mean Burst Original Analysis (Windows length " + str(
                                             nbr) + " lag " + str(lag) + ")", analysis=analysis, nbr_Burst=nbr_Burst,
                                         show=False, txt_data_temp=txt_data, txt_data_global=txt_data_global)

    elif type == "Overlap_Analysis":
        # GetMeanBursts
        cwt_map, nbr_Burst = CalculateMeanBurst(nbr, cwt_map, True, lag)

        # Calculate all Parameters
        MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height, nbr_Burst = CalculateParameters(
            cwt_map, analysis, nbr_Burst=nbr_Burst)

        # Creation of .mat file.
        sio.savemat(path + "/A5_Perc_nOvr" + filename + ".mat",
                    mdict={"MajorF": MajorFrequency, "MeanPower": MeanPower1, "BurstPos": BurstPos, "Area": Area2,
                           "Vol": Vol, "Width": Width, "Height": Height})

        # Generation of pdf Report.
        txt_data_global = plotParameters(MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1, Area2, Vol, pp,
                                         Title="Mean Burst Analysis - Overlapping Windows (Windows length " + str(
                                             nbr) + " lag " + str(lag) + ")", analysis=analysis, nbr_Burst=nbr_Burst,
                                         show=False, txt_data_temp=txt_data, txt_data_global=txt_data_global)

        if pandaData is not None and pandaDataMuscle is not None:
            panda_data = PandaConstruct(subject=txt_data_aux[0], muscle=txt_data_aux[1],
                                        paramName=['Major_Frequency', 'Mean_Power', 'Centroid_Postion',
                                                   'Time_Dispersion', 'Frequency_Dispersion', 'Area_in_Pixels',
                                                   'Convex_Hull_Area', 'Convex_Hull_Volume'],
                                        paramValues=[MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1, Area2,
                                                     Vol], time=nbr_Burst, panda_data=pandaData, analysis=analysis)
            panda_data_muscle = PandaConstruct(subject=txt_data_aux[0], muscle=txt_data_aux[1],
                                               paramName=['Major_Frequency', 'Mean_Power', 'Centroid_Postion',
                                                          'Time_Dispersion', 'Frequency_Dispersion', 'Area_in_Pixels',
                                                          'Convex_Hull_Area', 'Convex_Hull_Volume'],
                                               paramValues=[MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1,
                                                            Area2, Vol], time=nbr_Burst, panda_data=pandaDataMuscle,
                                               analysis=analysis)
            return txt_data_global, panda_data, panda_data_muscle

        else:
            return txt_data_global
    elif type == "Non_Overlap_Analysis":
        # GetMeanBursts
        cwt_map, nbr_Burst = CalculateMeanBurst(nbr, cwt_map, False)

        # Calculate all Parameters
        MajorFrequency, MaximumFrequency, MeanPower1, MeanPower2, BurstPos, Area1, Area2, Vol, Width, Height, nbr_Burst = CalculateParameters(
            cwt_map, analysis, nbr_Burst=nbr_Burst)

        # Creation of .mat file.
        sio.savemat(path + "/A5_Perc_nOvr" + filename + ".mat",
                    mdict={"MajorF": MajorFrequency, "MeanPower": MeanPower1, "BurstPos": BurstPos, "Area": Area2,
                           "Vol": Vol, "Width": Width, "Height": Height})

        # Generation of pdf Report.
        txt_data_global = plotParameters(MajorFrequency, MeanPower1, BurstPos, Width, Height, Area1, Area2, Vol, pp,
                                         Title="Mean Burst Analysis - Non Overlapping Windows (Windows length " + str(
                                             nbr) + " lag " + str(lag) + ")", analysis=analysis, nbr_Burst=nbr_Burst,
                                         show=False, txt_data_temp=txt_data, txt_data_global=txt_data_global)

    return txt_data_global

    # Provisional Version of 16th of July of 2017 :) *-* (: ª-ª
