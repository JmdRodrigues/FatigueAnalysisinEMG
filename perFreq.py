import numpy as np
import matplotlib.pyplot as plt
from novainstrumentation import smooth

def energy(mat, freqs):
	sum = np.zeros(len(freqs))
	for freq in range(0, len(freqs)):
		sum[freq] = np.sum(mat[freq, :]**2)/np.shape(mat)[1]


	plt.plot(freqs, sum)
	plt.show()

def CompareBE(sig, mat, part):

	begin = mat[:,:int(len(mat[0,:])/part)]
	end = mat[:, -int(len(mat[0, :]) / part):]

	# plt.plot(sig)
	# plt.plot(sig[:int(len(mat[0,:])/part)])
	# plt.plot(np.linspace(len(sig)-int(len(mat[0, :]) / part), len(sig), len(sig[-int(len(mat[0, :]) / part):])),sig[-int(len(mat[0, :]) / part):])
	# plt.show()
	#
	sum = np.zeros(len(sig))
	for i in range(0, len(sig)):
		sum[i] = np.sum(mat[:, i]**2)/len(mat[:, 0])



	plt.plot(sum)
	plt.show()


