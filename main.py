from WaveletAnalysis import Analysis, extractPks
import json
import numpy as np
import os
from Methods import filter_pks
from GenerateTxtFile import generateTxtFile
from PlottingSavers import PlotRadar
from AuxiliaryMethods import RemovePdf

# ----- Assessment to the list of folders inside "Signals" -----
# Name of the folder, inside the project, where the reports generated after the processing will be saved.
files_path = "Signals"
folders = os.listdir(files_path)
folders = RemovePdf(folders)

# ----- Arrays that will store data for txt file generation. -----
txt_data_global = []
txt_data_temp = []

# Structures used in the dataframe (Are extremely important for the graphical representation phase of the results).
panda_data = [[], [], [], [], [],
              []]  # Pseudo-dataframe [Subject, Muscle_Name, Time_Axis, Parameter_Value, Parameter_Name]
panda_data_muscle = [[], [], [], [], [], []]
cnt_subject = 0  # Auxiliary Counter.

# Structures that support the generation of "Radar Plots", congregating information from all muscles.
radar_data = [[], (), (), (), (), ()]
radar_data_all_sbj = []
sbjOrder = []

# Muscles Information.
MuscleNames = ["Rectus_Femoris", "Vastus_Lateralis", "Vastus_Medialis", "SemiTendinosus", "Biceps_Femoris"]
MuscleSeg = ["AccXmax", "AccXmax", "AccXmin", "AccXmax", "AccXmin"]

# Sampling Frequency
fs = 1000

for subject in folders:
    # Information of reference.
    sbjOrder.append(subject)

    # Data storage for generation of a txt file.
    txt_data_temp.append(subject)

    # ----- Copy of content. -----
    # (Is needed to preserve the original information between iterations. We can change the array txt_data_temp,
    # and in any moment the original content can be retrieved with txt_data_aux).
    txt_data_aux1 = list(txt_data_temp)

    subject_path = files_path + "/" + subject
    files = os.listdir(subject_path)

    print('\033[1;34m' + 'The Processing Stage of ' + str(subject) + ' started.' + '\033[0m')

    for eachFile in files:
        if ("." not in str(eachFile)):  # Folder clause.
            print("\tCould not open" + eachFile)
        else:
            if ("json" in str(eachFile)):  # json files clause.
                with open(subject_path + "/" + eachFile) as json_data:
                    d = json.load(json_data)
                start = d['start']
                end = d['end']
            elif ("txt" in str(eachFile)):  # txt files clause.
                signals = np.loadtxt(subject_path + "/" + eachFile)
                SubjectName = subject

    # Null Value Preventive Clause.
    if 'start' in locals() and 'end' in locals():
        signals = signals[start:end, :]

    # Find Segmentation points
    accx = signals[:, 8]
    accy = signals[:, 9]
    accz = signals[:, 10]

    pks_max, pks_min = extractPks(accx, fs)
    pks_start_max, pks_end_max, pks_start_min, pks_end_min = filter_pks(pks_max, pks_min, fs)

    # Radar Data - Fill of Structure.
    radar_data[0].append('RF')
    radar_data[0].append('VL')
    radar_data[0].append('VM')
    radar_data[0].append('ST')
    radar_data[0].append('BF')

    for muscle in range(0, len(MuscleNames)):
        print('\n\t' + '\033[1;31m' + str(MuscleNames[muscle]) + ' is being analysed.' + '\033[0m')

        # Copy of content.
        # (Is needed to preserve the original information between iterations. We change the array txt_data_temp and
        # in any moment the original content can be retrieved with txt_data_aux).
        txt_data_aux2 = list(txt_data_temp)

        # Data storage for generation of a txt file.
        txt_data_temp.append(MuscleNames[muscle])

        # Update of work folder (path information).
        filename = SubjectName + "_" + MuscleNames[muscle]
        path = files_path + "/" + SubjectName

        # TXTName = PDFName[:-4] + '.txt'
        # REPORTfile = open(files_path + "/" + TXTName[:-4] + "/" + TXTName, "w")  # REPORT FILE

        # Everything
        emg = signals[:, 3 + muscle]

        # Selection of the reference peaks for segmentation.
        if MuscleSeg[muscle] == "AccXmax":
            pks_start = pks_start_max
            pks_end = pks_end_max
        else:
            pks_start = pks_start_min
            pks_end = pks_end_min

        # Start of Analyis.
        if muscle != len(MuscleNames) - 1 and subject != len(folders) - 1:  # Intermediate Values Clause.
            txt_data_global, panda_data, panda_data_muscle, radar_data = Analysis(filename, path, signal=emg,
                                                                                  pks_start=pks_start,
                                                                                  pks_end=pks_end, fs=fs,
                                                                                  wavelet='morl',
                                                                                  txt_data_temp=txt_data_temp,
                                                                                  txt_data_global=txt_data_global,
                                                                                  pandaData=panda_data, final=False,
                                                                                  pandaDataMuscle=panda_data_muscle,
                                                                                  radarData=radar_data,
                                                                                  muscleIndex=muscle,
                                                                                  muscleName=MuscleNames[muscle])

        elif muscle == len(MuscleNames) - 1 and cnt_subject != len(folders) - 1:  # End of Muscle List Clause.
            txt_data_global, panda_data, panda_data_muscle, radar_data = Analysis(filename, path, signal=emg,
                                                                                  pks_start=pks_start,
                                                                                  pks_end=pks_end, fs=fs,
                                                                                  wavelet='morl',
                                                                                  txt_data_temp=txt_data_temp,
                                                                                  txt_data_global=txt_data_global,
                                                                                  pandaData=panda_data, final=True,
                                                                                  pandaDataMuscle=panda_data_muscle,
                                                                                  muscleFlag=False,
                                                                                  radarData=radar_data,
                                                                                  muscleIndex=muscle,
                                                                                  muscleName=MuscleNames[muscle])
        elif muscle != len(MuscleNames) - 1 and cnt_subject == len(folders) - 1:  # End of Subject List Clause.
            txt_data_global, panda_data, panda_data_muscle, radar_data = Analysis(filename, path, signal=emg,
                                                                                  pks_start=pks_start,
                                                                                  pks_end=pks_end, fs=fs,
                                                                                  wavelet='morl',
                                                                                  txt_data_temp=txt_data_temp,
                                                                                  txt_data_global=txt_data_global,
                                                                                  pandaData=panda_data, final=False,
                                                                                  pandaDataMuscle=panda_data_muscle,
                                                                                  muscleFlag=True,
                                                                                  radarData=radar_data,
                                                                                  muscleIndex=muscle,
                                                                                  muscleName=MuscleNames[muscle])
        elif muscle == len(MuscleNames) - 1 and cnt_subject == len(folders) - 1:  # Simultaneous End Clause.
            txt_data_global, panda_data, panda_data_muscle, radar_data = Analysis(filename, path, signal=emg,
                                                                                  pks_start=pks_start,
                                                                                  pks_end=pks_end, fs=fs,
                                                                                  wavelet='morl',
                                                                                  txt_data_temp=txt_data_temp,
                                                                                  txt_data_global=txt_data_global,
                                                                                  pandaData=panda_data, final=True,
                                                                                  pandaDataMuscle=panda_data_muscle,
                                                                                  muscleFlag=True,
                                                                                  radarData=radar_data,
                                                                                  muscleIndex=muscle,
                                                                                  muscleName=MuscleNames[muscle])

        # Reboot of content.
        txt_data_temp = list(txt_data_aux2)

    # Reboot of content.
    txt_data_temp = []
    panda_data = [[], [], [], [], [], []]
    radar_data_all_sbj.append(radar_data)
    radar_data = [[], (), (), (), (), ()]

    # Generation of a txt file with the processing results. [Subject, MuscleName, Analysis, lag, ParameterName, rValue].
    # (Instruction for test proposals)
    generateTxtFile(txt_data_global)
    cnt_subject = cnt_subject + 1

# Generation of a txt file with processing results. [Subject, MuscleName, Analysis, lag, ParameterName, rValue].
print ('\033[1m' + 'The Txt Report Generation began.' + '\033[0m')
generateTxtFile(txt_data_global)

# Generation of the Evolution of Mean Power for each Subject in the "Non-Overlapping Analysis" using a Radar Plot.
print ('\033[1m' + 'Radar Plot Representation started. ' + '\033[0m')
PlotRadar(radar_data_all_sbj, sbjOrder)

# Provisional Version of 15th of July of 2017 :) *-* (: ª-ª
