from Methods import EMG_Pre_P, freq2scale, CreateInterpolatedBurstCWT, ACC_Pre_P
from AnalysisMethods import Analysis1, Analysis2_4, Analysis3, Analysis5
from Peaks import detect_peaks
from PlottingSavers import plotEMG, plotEMG3D, SynthesisGrid
from AuxiliaryMethods import TxtGlobalDecode
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import scipy.io as sio
import pywt
import os
import pylab as plt
import novainstrumentation as ni
from pandas import DataFrame, concat

# Function for Identification of Signal Peaks.
# (In this case for accelerometer data related to muscular activation periods).
def extractPks(accX, fs):
    # filter acc
    acc = ACC_Pre_P(accX, fs)
    acc = (acc - np.mean(acc)) / max(acc)

    # Additional Smoothing Phase.
    smooth_acc = ni.smooth(acc, int(fs / 3))

    # Identification of the start and end of activation periods.
    pks_max = detect_peaks(smooth_acc)  # We should decrease the number of function inputs, in this case produces good results when mph and mpd are excluded.
    pks_min = detect_peaks(smooth_acc, valley=True)

    return pks_max, pks_min

# EMG Signal Analysis - Nuclear Function.
def Analysis(filename, path, signal, pks_start, pks_end, fs, wavelet, txt_data_temp, txt_data_global, pandaData,
             pandaDataMuscle, final=False, muscle=None, muscleFlag=False, radarData=None, muscleIndex=0,
             muscleName=None):
    # [NOTE] The txt_data_global array will be used for a txt file generation with the results of the different Analysis.

    # ----- Copy of content. -----
    # (Is needed to preserve the original information between iterations. We change the array txt_data_temp
    # and in any moment the original content can be retrieved with txt_data_aux).
    txt_data_aux = list(txt_data_temp)

    # ----- PreProcessing EMG -----
    emg = EMG_Pre_P(signal, fs)

    # Calculate Scalogram
    frequencyRange = np.arange(5, 500, 4)
    # frequencyRange = np.arange(5, 500, 1)
    scales = 1000 * freq2scale(frequencyRange, wavelet)

    # Time to Frequency Domain Transposition.
    coef, freqs = pywt.cwt(emg, scales, wavelet, sampling_period=1.0 / fs)

    # Calculate meanBurstsParameters
    cwt_N = CreateInterpolatedBurstCWT(coef, pks_start, pks_end)

    # Report Specifications.
    PDFName = filename + '.pdf'

    if not os.path.exists(path + "/" + PDFName[:-4]):
        os.makedirs(path + "/" + PDFName[:-4])

    # ----- Analysis 1 - Burst to Burst Analysis. -----
    print('\033[1;32m' + "\t\tThe Analysis1 started. [Burst by Burst Processing]" + '\033[0m')
    pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis1_" + PDFName)

    plotEMG(pks_start, pks_end, emg, pp)
    # plotEMG3D(np.power(coef, 2), pp)

    # Analysis of the signal for each burst
    Analysis1(cwt_N, path, filename, pp)

    pp.close()

    # ----- Analysis 2 - Analysis of the signal using a sliding window mechanism (with or without overlap). ------
    print('\033[1;32m' + "\t\tThe Analysis2 started. [Restrictive OTSU Thresholding]" + '\033[0m')
    pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis2_" + PDFName)

    # -- Original Analysis (window length = 10 and lag = 9) --
    txt_data_global = Analysis2_4(cwt_N, 10, path, filename, pp, "Original_Analysis", analysis=2,
                                  txt_data=txt_data_temp, txt_data_global=TxtGlobalDecode(txt_data_global))
    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    # -- Non Overlap Analysis (window length determined with percentile) --
    length_perc = int(0.10 * len(cwt_N))
    txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Non_Overlap_Analysis", analysis=2,
                                  txt_data=txt_data_temp, txt_data_global=TxtGlobalDecode(txt_data_global))
    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    # -- Overlap Analysis (lag = 0.30 or 0.50 or 0.70 of window length) --
    # [Lag Factor --> 0.70]
    txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis",
                                  lag=int(0.70 * length_perc), analysis=2, txt_data=txt_data_temp,
                                  txt_data_global=TxtGlobalDecode(txt_data_global))
    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    # [Lag Factor --> 0.50]
    txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis",
                                  lag=int(0.50 * length_perc), analysis=2, txt_data=txt_data_temp,
                                  txt_data_global=TxtGlobalDecode(txt_data_global))
    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    # [Lag Factor --> 0.30]
    txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis",
                                  lag=int(0.30 * length_perc), analysis=2, txt_data=txt_data_temp,
                                  txt_data_global=TxtGlobalDecode(txt_data_global))
    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    pp.close()

    # ----- Analysis 3 - Analysis of the beginning and the end of the signal. -----
    print('\033[1;32m' + "\t\tThe Analysis3 started. [Analysis of the first and last sets of 20 and 50 muscular activation periods]" + '\033[0m')
    pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis3_" + PDFName)

    # Sets of 20 Muscular Activations.
    Analysis3(cwt_N, 20, path, filename, pp)
    # Sets of 50 Muscular Activations.
    Analysis3(cwt_N, 50, path, filename, pp)

    pp.close()

    # ----- Analysis 4 - Analysis of the original cwt_map, without OTSUs Thresholds (Identical to Analysis 2). -----
    print('\033[1;32m' + "\t\tThe Analysis4 started. [Parameters extracted from the original Scalogram]" + '\033[0m')
    pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis4_" + PDFName)

    # -- Original Analysis (window length = 10 and lag = 9) --
    #txt_data_global = Analysis2_4(cwt_N, 10, path, filename, pp, "Original_Analysis", analysis=4,
    #                              txt_data=txt_data_temp, txt_data_global=TxtGlobalDecode(txt_data_global))

    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    # -- Non Overlap Analyis (window length determined with percentile) --
    length_perc = int(0.10 * len(cwt_N))
    txt_data_global, radarData = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Non_Overlap_Analysis", analysis=4,
                                             txt_data=txt_data_temp, txt_data_global=TxtGlobalDecode(txt_data_global),
                                             radarData=radarData, muscleIndex=muscleIndex, muscleName=muscleName)

    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    # -- Overlap Analysis (lag = 0.30 or 0.50 or 0.70 of window length) --
    # [Lag Factor --> 0.70]
    txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis",
                                  lag=int(0.70 * length_perc), analysis=4, txt_data=txt_data_temp,
                                  txt_data_global=TxtGlobalDecode(txt_data_global))

    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    # [Lag Factor --> 0.50]
    txt_data_global, pandaData, pandaDataMuscle = Analysis2_4(cwt_N, length_perc, path, filename, pp,
                                                              "Overlap_Analysis", lag=int(0.50 * length_perc),
                                                              analysis=4, txt_data=txt_data_temp,
                                                              txt_data_global=TxtGlobalDecode(txt_data_global), pandaData=pandaData,
                                                              final=final, pandaDataMuscle=pandaDataMuscle,
                                                              muscleName=muscleName)

    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    # [Lag Factor --> 0.30]
    txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis",
                                  lag=int(0.30 * length_perc), analysis=4, txt_data=txt_data_temp,
                                  txt_data_global=TxtGlobalDecode(txt_data_global))

    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    pp.close()

    # ----- Analysis 5 - Analysis of the cwt_map, with OTSUs Thresholds (But less restrictive than Analysis 2). -----
    print('\033[1;32m' + "\t\tThe Analysis5 started. [Less Restrictive OTSU Thresholding comparing to Analysis2]" + '\033[0m')
    pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis5_" + PDFName)

    # -- Original Analyis (window length = 10 and lag = 9) --
    txt_data_global = Analysis5(cwt_N, 10, path, filename, pp, "Original_Analysis", analysis=5, txt_data=txt_data_temp,
                                txt_data_global=TxtGlobalDecode(txt_data_global))
    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    # -- Non Overlap Analyis (window length determined with percentil and lag = 0.30 or 0.50 or 0.70 of window length) --
    length_perc = int(0.10 * len(cwt_N))
    txt_data_global = Analysis5(cwt_N, length_perc, path, filename, pp, "Non_Overlap_Analysis", analysis=5,
                                txt_data=txt_data_temp, txt_data_global=TxtGlobalDecode(txt_data_global))
    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    # -- Overlap Analysis (lag = 0.30 or 0.50 or 0.70 of window length) --
    # [Lag Factor --> 0.70]
    txt_data_global = Analysis5(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis", lag=int(0.70 * length_perc),
                                analysis=5, txt_data=txt_data_temp, txt_data_global=TxtGlobalDecode(txt_data_global))
    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    # [Lag Factor --> 0.50]
    txt_data_global, pandaData, pandaDataMuscle = Analysis5(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis",
                                                            lag=int(0.50 * length_perc), analysis=5,
                                                            txt_data=txt_data_temp, txt_data_global=TxtGlobalDecode(txt_data_global),
                                                            pandaData=pandaData, final=final,
                                                            pandaDataMuscle=pandaDataMuscle)
    # Reboot of content.
    txt_data_temp = list(txt_data_aux)

    # [Lag Factor --> 0.70]
    txt_data_global = Analysis5(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis", lag=int(0.30 * length_perc),
                                analysis=5, txt_data=txt_data_temp, txt_data_global=TxtGlobalDecode(txt_data_global))

    pp.close()

    # Synthesis Reports Generation. (Results By Muscle)
    if muscleFlag == True:
        # Generation of data frame.
        pandaStructMuscle = DataFrame(np.transpose(pandaDataMuscle),
                                      columns=['Sbj', 'Msc', 'PName', 'PValue', '#Set', 'Anly'])

        # Identification of the list of muscles.
        muscleList = list(set(pandaStructMuscle['Msc'].tolist()))

        # Generation of a pdf synthesis for each muscle.
        for muscleIndex in range(0, len(muscleList)):
            # Analysis 4.
            # Results are restricted to the muscle in analysis.
            pandaTemp = pandaStructMuscle[pandaStructMuscle.Msc == muscleList[muscleIndex]]
            pandaTemp = pandaTemp[pandaTemp.Anly == str(4)]
            pandaTemp = pandaTemp[pandaTemp.PValue != 'False']

            pp = PdfPages(path + "/" + str(muscleList[muscleIndex]) + "_Synthesis4.pdf")

            # Graphical Representation and fill of data frame.
            # Groups of five subjects.
            subjList = list(set(pandaTemp['Sbj'].tolist()))

            # Auxiliary Counter (Essential when the number of subject is not a multiple of 5).
            remainingSbjGrid = [True, True, True, True, True]

            for subjIndex in range(0, len(subjList), 5):
                remainingSbj = len(subjList) - subjIndex
                if remainingSbj >= 5:
                    remainingSbjGrid = [True, True, True, True, True]
                else:
                    for i in range(0, remainingSbj):
                        remainingSbjGrid[i] = True
                    for i in range(remainingSbj, len(remainingSbjGrid)):
                        remainingSbjGrid[i] = False
                if remainingSbjGrid[0] == True:
                    panda1 = pandaTemp[pandaTemp.Sbj == subjList[subjIndex + 0]]
                    pandaConcat = panda1
                if remainingSbjGrid[1] == True:
                    panda2 = pandaTemp[pandaTemp.Sbj == subjList[subjIndex + 1]]
                    pandaConcat = concat([pandaConcat, panda2])
                if remainingSbjGrid[2] == True:
                    panda3 = pandaTemp[pandaTemp.Sbj == subjList[subjIndex + 2]]
                    pandaConcat = concat([pandaConcat, panda3])
                if remainingSbjGrid[3] == True:
                    panda4 = pandaTemp[pandaTemp.Sbj == subjList[subjIndex + 3]]
                    pandaConcat = concat([pandaConcat, panda4])
                if remainingSbjGrid[4] == True:
                    panda5 = pandaTemp[pandaTemp.Sbj == subjList[subjIndex + 4]]
                    pandaConcat = concat([pandaConcat, panda5])

                SynthesisGrid(pandaConcat, pp, colIn="PName", rowIn="Sbj")

            pp.close()

            # Analysis 5.
            # Results are restricted to the muscle in analysis.
            pandaTemp = pandaStructMuscle[pandaStructMuscle.Msc == muscleList[muscleIndex]]
            pandaTemp = pandaTemp[pandaTemp.Anly == str(5)]
            pandaTemp = pandaTemp[pandaTemp.PValue != 'False']

            pp = PdfPages(path + "/" + str(muscleList[muscleIndex]) + "_Synthesis5.pdf")

            # Graphical Representation and fill of data frame.
            # Groups of five subjects.
            subjList = list(set(pandaTemp['Sbj'].tolist()))

            for subjIndex in range(0, len(subjList), 5):
                remainingSbj = len(subjList) - subjIndex
                if remainingSbj >= 5:
                    remainingSbjGrid = [True, True, True, True, True]
                else:
                    for i in range(0, remainingSbj):
                        remainingSbjGrid[i] = True
                    for i in range(remainingSbj, len(remainingSbjGrid)):
                        remainingSbjGrid[i] = False

                if remainingSbjGrid[0] == True:
                    panda1 = pandaTemp[pandaTemp.Sbj == subjList[subjIndex + 0]]
                    pandaConcat = panda1
                if remainingSbjGrid[1] == True:
                    panda2 = pandaTemp[pandaTemp.Sbj == subjList[subjIndex + 1]]
                    pandaConcat = concat([pandaConcat, panda2])
                if remainingSbjGrid[2] == True:
                    panda3 = pandaTemp[pandaTemp.Sbj == subjList[subjIndex + 2]]
                    pandaConcat = concat([pandaConcat, panda3])
                if remainingSbjGrid[3] == True:
                    panda4 = pandaTemp[pandaTemp.Sbj == subjList[subjIndex + 3]]
                    pandaConcat = concat([pandaConcat, panda4])
                if remainingSbjGrid[4] == True:
                    panda5 = pandaTemp[pandaTemp.Sbj == subjList[subjIndex + 4]]
                    pandaConcat = concat([pandaConcat, panda5])

                SynthesisGrid(pandaConcat, pp, colIn="PName", rowIn="Sbj")

            pp.close()

    # Synthesis Reports Generation. (Results By Subject)
    if final == True:
        # Analysis 4.
        pp = PdfPages(path + "/" + "Synthesis4.pdf")

        # Generation of data frame.
        pandaStruct = DataFrame(np.transpose(pandaData), columns=['Sbj', 'Msc', 'PName', 'PValue', '#Set', 'Anly'])
        pandaTemp = pandaStruct[pandaStruct.Anly == str(4)]
        pandaTemp = pandaTemp[pandaTemp.PValue != 'False']

        # Graphical Representation and fill of data frame.
        SynthesisGrid(pandaTemp, pp)

        pp.close()

        # Analysis 5.
        pp = PdfPages(path + "/" + "Synthesis5.pdf")

        # Generation of data frame.
        pandaStruct = DataFrame(np.transpose(pandaData), columns=['Sbj', 'Msc', 'PName', 'PValue', '#Set', 'Anly'])
        pandaTemp = pandaStruct[pandaStruct.Anly == str(5)]
        pandaTemp = pandaTemp[pandaTemp.PValue != 'False']

        # Graphical Representation and fill of data frame.
        SynthesisGrid(pandaTemp, pp)

        pp.close()

    return TxtGlobalDecode(txt_data_global), pandaData, pandaDataMuscle, radarData

    # Provisional Version of 15th of July of 2017 :) *-* (: ª-ª
