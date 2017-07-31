from pandas import DataFrame
import numpy as np

# Function with the main purpose of creating a Panda dataframe that makes possible and easier the presentation of graphical results.
def PandaConstruct(subject, muscle, paramName, paramValues, time, panda_data, analysis=4):

    # Name Conversion.
    subject, muscle, paramName = NameConversion(subject, muscle, paramName)

    # Fill of dataframe [Subject, Muscle_Name, Time_Axis, Parameter_Value, Parameter_Name].
    for param in range(0, len(paramName)):
        if len(paramValues[param]) != 0:
            for timeInst in range(0, len(paramValues[0])):
                panda_data[0].append(subject)
                panda_data[1].append(muscle)
                panda_data[2].append(paramName[param])
                panda_data[3].append(paramValues[param][timeInst])
                panda_data[4].append(time[timeInst])
                panda_data[5].append(analysis)

    return panda_data

# Function used for trunc names, which simplifies the presentation of graphical results.
def NameConversion(subject, muscle, paramName):
    # 'Subject' String Conversion.
    if len(subject) == 8:
        subject = 'Sbj' + subject[-1:]
    else:
        subject = 'Sbj' + subject[-2:]

    # 'Muscle' String Conversion.
    if muscle == 'Rectus_Femoris':
        muscle = 'RF'
    elif muscle == 'Biceps_Femoris':
        muscle = 'BF'
    elif muscle == 'Vastus_Medialis':
        muscle = 'VM'
    elif muscle == 'Vastus_Lateralis':
        muscle = 'VL'
    elif muscle == 'SemiTendinosus':
        muscle = 'ST'

    # 'paramName' String Conversion.
    for i in range(0, len(paramName)):
        if paramName[i] == 'Major_Frequency':
            paramName[i] = 'MF'
        elif paramName[i] == 'Mean_Power':
            paramName[i] = 'MP'
        elif paramName[i] == 'Centroid_Postion':
            paramName[i] = 'CP'
        elif paramName[i] == 'Frequency_Dispersion':
            paramName[i] = 'FD'
        elif paramName[i] == 'Area_in_Pixels':
            paramName[i] = 'AP'
        elif paramName[i] == 'Convex_Hull_Area':
            paramName[i] = 'CHA'
        elif paramName[i] == 'Convex_Hull_Volume':
            paramName[i] = 'CHV'

    return subject, muscle, paramName

# Identification of a pdf file in a folder name list.
def RemovePdf(array):
    index = []
    for i in range(0, len(array)):
        if '.pdf' in array[i]:
            index.append(i)

    array = np.delete(np.array(array), index)

    return array

# This function has the capability to return an array from the input structure (tuple or array).
def TxtGlobalDecode(txt_data_global):
    if type(txt_data_global) is tuple:
        return txt_data_global[0]
    else:
        return txt_data_global

# Provisional Version of 16th of July of 2017 :) *-* (: ª-ª