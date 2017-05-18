import numpy as np
import scipy.signal as sc
import pywt
import smooth as sm
import matplotlib.pyplot as plt
import seaborn

def MF_calculus(Pxx):
    sumPxx = np.sum(Pxx)
    mf = 0
    for i in range(0, len(Pxx)):
        if(np.sum(Pxx[0:i]) < sumPxx/2.0):
            continue
        else:
            mf = i
            break

    return mf

def PowerSpectrum(data, fs):
    f, Pxx = sc.welch(data, fs=fs, nfft=1024)

    return f, Pxx


