
from WaveletAnalysis import Analysis, extractPks
import json
import numpy as np
import os

#load signal #3
files_path = "Signals"

folders = os.listdir(files_path)
for subject in folders:
	subject_path = files_path + "/" + subject
	files = os.listdir(subject_path)
	print(subject)
	for eachFile in files:
		print(eachFile)
		if("." not in str(eachFile)):
			print("Could not open" + eachFile)
		else:
			if("json" in str(eachFile)):
				with open(subject_path + "/" + eachFile) as json_data:
					d = json.load(json_data)
				start = d['start']
				end = d['end']
			elif("txt" in str(eachFile)):
				signals = np.loadtxt(subject_path + "/" + eachFile)
				SubjectName = subject

	signals = signals[start:end, :]
	#Muscles
	MuscleNames = ["Rectus_Femoris", "Vastus_Lateralis", "Vastus_Medialis", "SemiTendinosus", "Biceps_Femoris"]
	#Sampling Frequency
	fs = 1000
	#Find Segmentation points
	accx = signals[:, 8]
	pks = extractPks(accx, fs)

	for muscle in range(0, len(MuscleNames)):
		print(MuscleNames[muscle])
		filename = SubjectName + "_" + MuscleNames[muscle]
		path = files_path + "/" + SubjectName

		# TXTName = PDFName[:-4] + '.txt'
		# REPORTfile = open(files_path + "/" + TXTName[:-4] + "/" + TXTName, "w")  # REPORT FILE

		#Everything
		emg = signals[:, 3+muscle]
		Analysis(filename, path, signal=emg, pks=pks, fs=fs, wavelet= 'morl')
		# Analysis(signal=emg, pks=pks, fs=fs, wavelet='mexh', pp=pp)

		# Close report and graphics PDF
		# REPORTfile.close()



