import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.gridspec as grid
import seaborn as sns
import pandas
import itertools
import matplotlib.patheffects as pte
import numpy as np
from matplotlib import cm
from matplotlib.font_manager import FontProperties
from matplotlib.figure import SubplotParams
# import matplotlib.axes3d as p3
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.patches import  Circle


def plotEMG(pks, emg, pp):

	# Specify plot parameters
	# color
	face_color_r = 248 / 255.0
	face_color_g = 247 / 255.0
	face_color_b = 249 / 255.0

	# pars
	left = 0.05  # the left side of the subplots of the figure
	right = 0.95  # the right side of the subplots of the figure
	bottom = 0.05  # the bottom of the subplots of the figure
	top = 0.92  # the top of the subplots of the figure
	wspace = 0.5  # the amount of width reserved for blank space between subplots
	hspace = 0.4  # the amount of height reserved for white space between subplots

	pars = SubplotParams(left, bottom, right, top, wspace, hspace)

	fig1 = plt.figure(subplotpars=pars)
	fig1.set_facecolor((face_color_r, face_color_g, face_color_b))
	fig1.set_dpi(96)
	fig1.set_figheight(1080 / 96)
	fig1.set_figwidth(1920 / 96)
	fig1.suptitle("EMG Segmentation")

	time = np.linspace(0, len(emg)/1000, len(emg))
	plt.plot(time, emg)
	plt.vlines(x=np.divide(pks, 1000), ymin=min(emg), ymax=max(emg), colors='orange')
	plt.xlim((100, 110))
	# plt.show()
	pp.savefig(fig1)


def plotParameters(MajorF, MeanP, BurstPos, width, height, PixelArea, HullArea, HullVolume, pp, Title, show = False):
	#Fonts
	# specify Font properties with fontmanager---------------------------------------------------
	font0 = FontProperties()
	font0.set_weight('medium')
	font0.set_family('monospace')
	# Specify Font properties of Legends
	font1 = FontProperties()
	font1.set_weight('normal')
	font1.set_family('sans-serif')
	font1.set_style('italic')
	font1.set_size(12)
	# Specify font properties of Titles
	font2 = FontProperties()
	font2.set_size(15)
	font2.set_family('sans-serif')
	font2.set_weight('medium')
	font2.set_style('italic')

	#Specify plot parameters
	# color
	face_color_r = 248 / 255.0
	face_color_g = 247 / 255.0
	face_color_b = 249 / 255.0

	# pars
	left = 0.05  # the left side of the subplots of the figure
	right = 0.95  # the right side of the subplots of the figure
	bottom = 0.05  # the bottom of the subplots of the figure
	top = 0.92  # the top of the subplots of the figure
	wspace = 0.5  # the amount of width reserved for blank space between subplots
	hspace = 0.4  # the amount of height reserved for white space between subplots

	pars = SubplotParams(left, bottom, right, top, wspace, hspace)

	fig1 = plt.figure(subplotpars=pars)
	fig1.set_facecolor((face_color_r, face_color_g, face_color_b))
	fig1.set_dpi(96)
	fig1.set_figheight(1080 / 96)
	fig1.set_figwidth(1920 / 96)
	fig1.suptitle(Title)
	# fig1.subplotpars(pars)

	ax11 = plt.subplot(3,1,1)
	ax11.plot(MajorF) #limit from min and max frequencies
	ax11.set_title('Major Frequency', fontproperties=font2)
	ax11.set_ylabel("Major Frequency (Hz)", fontproperties=font1)
	ax11.set_xlabel("Burst", fontproperties=font1)
	ax12 = plt.subplot(3, 1, 2)
	ax12.plot(MeanP)
	ax12.set_title('Mean Power', fontproperties=font2) #limit with total power
	ax12.set_ylabel("Mean Power (r.u)", fontproperties=font1)
	ax12.set_xlabel("Burst", fontproperties=font1)
	ax13 = plt.subplot(3, 1, 3)
	ax13.set_title('Centroid Position Over The Pedal Cicle', fontproperties=font2) #limit from 0 and 1
	ax13.plot(np.multiply(BurstPos, 100))
	ax13.set_ylim((0, 100))
	ax13.set_ylabel("Centroid Position (% of pedal Cicle)", fontproperties=font1)
	ax13.set_xlabel("Burst", fontproperties=font1)

	fig2 = plt.figure(subplotpars=pars)
	fig2.set_dpi(96)
	fig2.set_figheight(1080 / 96)
	fig2.set_figwidth(1920 / 96)
	fig2.suptitle(Title)


	ax21 = plt.subplot(2, 1, 1)
	ax21.plot(width)
	ax21.set_title('Time Dispersion', fontproperties=font2) #limit with total power
	ax21.set_ylabel("Width Amplitude (r.u)", fontproperties=font1)
	ax21.set_xlabel("Burst", fontproperties=font1)
	ax22 = plt.subplot(2, 1, 2)
	ax22.plot(height)
	ax22.set_title('Frequency Dispersion', fontproperties=font2) #limit with total power
	ax22.set_ylabel("Frequency Range (Hz)", fontproperties=font1)
	ax22.set_xlabel("Burst", fontproperties=font1)

	fig3 = plt.figure(subplotpars=pars)
	fig3.set_dpi(96)
	fig3.set_figheight(1080 / 96)
	fig3.set_figwidth(1920 / 96)
	fig3.suptitle(Title)


	ax31 = plt.subplot(3, 1, 1)
	ax31.plot(PixelArea)
	ax31.set_title('Area in Pixels', fontproperties=font2) #limit with total power
	ax31.set_ylabel("Area (Pixels)", fontproperties=font1)
	ax31.set_xlabel("Burst", fontproperties=font1)
	ax32 = plt.subplot(3, 1, 2)
	ax32.plot(HullArea)
	ax32.set_title('Convex Hull Area', fontproperties=font2) #limit with total power
	ax32.set_ylabel("Area (r.u)", fontproperties=font1)
	ax32.set_xlabel("Burst", fontproperties=font1)
	ax33 = plt.subplot(3, 1, 3)
	ax33.plot(HullVolume)
	ax33.set_title('Convex Hull Volume', fontproperties=font2) #limit with total power
	ax33.set_ylabel("Volume (r.u)", fontproperties=font1)
	ax33.set_xlabel("Burst", fontproperties=font1)

	if show==False:
		pp.savefig(fig1)
		pp.savefig(fig2)
		pp.savefig(fig3)
	else:
		plt.show()

def PlotMap3(Begin, End, maxT, coorB, coorE, hullAB, hullAE, pointsB, pointsE, pp):
	# Specify plot parameters
	# color
	face_color_r = 248 / 255.0
	face_color_g = 247 / 255.0
	face_color_b = 249 / 255.0

	# pars
	left = 0.05  # the left side of the subplots of the figure
	right = 0.95  # the right side of the subplots of the figure
	bottom = 0.05  # the bottom of the subplots of the figure
	top = 0.92  # the top of the subplots of the figure
	wspace = 0.5  # the amount of width reserved for blank space between subplots
	hspace = 0.4  # the amount of height reserved for white space between subplots

	pars = SubplotParams(left, bottom, right, top, wspace, hspace)

	x = np.linspace(0, 100, len(Begin[0]))
	y = np.linspace(5, len(Begin)+5, len(Begin))
	X, Y = np.meshgrid(x, y)
	pointsB[:, 0] = np.multiply(np.divide(pointsB[:, 0], len(x)), 100)
	pointsE[:, 0] = np.multiply(np.divide(pointsE[:, 0], len(x)), 100)


	fig1 = plt.figure(subplotpars=pars)
	fig1.set_facecolor((face_color_r, face_color_g, face_color_b))
	fig1.set_dpi(96)
	fig1.set_figheight(1080 / 96)
	fig1.set_figwidth(1920 / 96)
	fig1.suptitle("Analysis of the Beggining and End of the Spectrum")


	ax1 = plt.subplot(2,1,1)
	im1 = ax1.pcolormesh(X, Y, Begin, cmap=cm.hot, vmax=maxT, vmin=0)
	fig1.colorbar(im1, ax=ax1)
	for simplex in hullAB.simplices:
		ax1.plot(pointsB[simplex, 0], pointsB[simplex, 1], 'b-')
	plt.legend(facecolor='b')
	ax1.set_xlabel('Pedal Cicle (%)')
	ax1.set_ylabel('Frequency (Hz)')
	# print(coorB)
	circ1 = Circle(coorB, 1, label="Weighted Centroid")
	ax1.add_patch(circ1)

	ax2 = plt.subplot(2,1,2)
	im2 = ax2.pcolormesh(X, Y, End, cmap=cm.hot, vmax=maxT, vmin=0)
	fig1.colorbar(im2, ax=ax2)

	for simplex in hullAE.simplices:
		ax2.plot(pointsE[simplex, 0], pointsE[simplex, 1], 'b-')
	plt.legend(facecolor='b')
	ax2.set_xlabel('Pedal Cicle (%)')
	ax2.set_ylabel('Frequency (Hz)')

	circ2 = Circle(coorE, 1, label="Weighted Centroid")
	ax2.add_patch(circ2)

	# plt.show()
	pp.savefig(fig1)

def PlotParam3(BeginParams, EndParams, pp):

	MFB, MaxFB, MP1B, MP2B, BPB, A1B, A2B, VolB, WB, HB, hullB, pointsB = BeginParams
	MFE, MaxFE, MP1E, MP2E, BPE, A1E, A2E, VolE, WE, HE, hullE, pointsE = EndParams

	bar_width = 0.35
	# color
	face_color_r = 248 / 255.0
	face_color_g = 247 / 255.0
	face_color_b = 249 / 255.0

	# pars
	left = 0.05  # the left side of the subplots of the figure
	right = 0.95  # the right side of the subplots of the figure
	bottom = 0.05  # the bottom of the subplots of the figure
	top = 0.92  # the top of the subplots of the figure
	wspace = 0.5  # the amount of width reserved for blank space between subplots
	hspace = 0.4  # the amount of height reserved for white space between subplots

	pars = SubplotParams(left, bottom, right, top, wspace, hspace)

	fig1 = plt.figure(subplotpars=pars)
	fig1.set_facecolor((face_color_r, face_color_g, face_color_b))
	fig1.set_dpi(96)
	fig1.set_figheight(1080 / 96)
	fig1.set_figwidth(1920 / 96)
	fig1.suptitle("Analysis of the Beggining and End of the Spectrum")
	#8 analises
	index = [0, 1]
	ax11 = plt.subplot(4, 2, 1)
	ax11.bar(0, MFB, color='b', label='Begin', width = bar_width)
	ax11.bar(1, MFE, color='orange', label='End', width = bar_width)
	ax11.set_title("Mean Frequency")

	ax12 = plt.subplot(4, 2, 2)
	ax12.bar(0, MP1B, color='b', label='Begin', width = bar_width)
	ax12.bar(1, MP1E, color='orange', label='End', width = bar_width)
	ax12.set_title("Mean Power")

	ax21 = plt.subplot(4, 2, 3)
	ax21.bar(0, BPB, color='b', label='Begin', width = bar_width)
	ax21.bar(1, BPE, color='orange', label='End', width = bar_width)
	ax21.set_title("Burst Position")

	ax22 = plt.subplot(4, 2, 4)
	ax22.bar(0, A1B, color='b', label='Begin', width = bar_width)
	ax22.bar(1, A1E, color='orange', label='End', width = bar_width)
	ax22.set_title("Area 1")

	ax31 = plt.subplot(4, 2, 5)
	ax31.bar(0, A2B, color='b', label='Begin', width = bar_width)
	ax31.bar(1, A2E, color='orange', label='End', width = bar_width)
	ax31.set_title("Area 2")

	ax32 = plt.subplot(4, 2, 6)
	ax32.bar(0, VolB, color='b', label='Begin', width = bar_width)
	ax32.bar(1, VolE, color='orange', label='End', width = bar_width)
	ax32.set_title("Volume")

	ax41 = plt.subplot(4, 2, 7)
	ax41.bar(0, WB, color='b', label='Begin', width = bar_width)
	ax41.bar(1, WE, color='orange', label='End', width = bar_width)
	ax41.set_title("Width of Spectrum Activation")

	ax42 = plt.subplot(4, 2, 8)
	lb, = ax42.bar(0, HB, color='b', label='Begin', width = bar_width)
	le, =ax42.bar(1, HE, color='orange', label='End', width = bar_width)
	ax42.set_title("Frequency of Spectrum Activation")

	plt.xlabel('Group')
	plt.ylabel('Scores')
	fig1.legend(handles=[lb, le], labels=['begin', 'end'], loc='upper right', shadow=True, fancybox = True)


	pp.savefig(fig1)

def plotEMG3D(cmap, pp):
	# color
	face_color_r = 248 / 255.0
	face_color_g = 247 / 255.0
	face_color_b = 249 / 255.0

	# pars
	left = 0.05  # the left side of the subplots of the figure
	right = 0.95  # the right side of the subplots of the figure
	bottom = 0.05  # the bottom of the subplots of the figure
	top = 0.92  # the top of the subplots of the figure
	wspace = 0.5  # the amount of width reserved for blank space between subplots
	hspace = 0.4  # the amount of height reserved for white space between subplots

	pars = SubplotParams(left, bottom, right, top, wspace, hspace)

	fig1 = plt.figure(subplotpars=pars)
	fig1.set_facecolor((face_color_r, face_color_g, face_color_b))
	fig1.set_dpi(96)
	fig1.set_figheight(1080 / 96)
	fig1.set_figwidth(1920 / 96)
	fig1.suptitle("Analysis of the Beggining and End of the Spectrum")
	x = np.linspace(0, len(cmap[0])/1000, len(cmap[0]))
	y = np.linspace(5, len(cmap)+5, len(cmap))
	X, Y = np.meshgrid(x, y)
	ax = p3.Axes3D(fig1)
	ax.plot_surface(X, Y, cmap, cmap=cm.hot)
	ax.set_xlabel('Time (s)')
	ax.set_ylabel('Frequency (Hz)')
	ax.set_zlabel('Amplitude (r.u.)')

	pp.savefig(fig1)

def plotBurst3D(cmapB, cmapE, pp):
	# color
	face_color_r = 248 / 255.0
	face_color_g = 247 / 255.0
	face_color_b = 249 / 255.0

	# pars
	left = 0.05  # the left side of the subplots of the figure
	right = 0.95  # the right side of the subplots of the figure
	bottom = 0.05  # the bottom of the subplots of the figure
	top = 0.92  # the top of the subplots of the figure
	wspace = 0.5  # the amount of width reserved for blank space between subplots
	hspace = 0.4  # the amount of height reserved for white space between subplots

	pars = SubplotParams(left, bottom, right, top, wspace, hspace)

	fig1 = plt.figure(subplotpars=pars)
	fig1.set_facecolor((face_color_r, face_color_g, face_color_b))
	fig1.set_dpi(96)
	fig1.set_figheight(1080 / 96)
	fig1.set_figwidth(1920 / 96)
	fig1.suptitle("Analysis of the Beggining and End of the Spectrum")
	x = np.linspace(0, 100, len(cmapB[0]))
	y = np.linspace(5, len(cmapB)+5, len(cmapB))
	X, Y = np.meshgrid(x, y)
	ax1 = fig1.add_subplot(1,2,1, projection='3d')
	ax1.plot_surface(X, Y, cmapB, cmap=cm.hot)
	ax1.set_xlabel('Pedal Cicle (%)')
	ax1.set_ylabel('Frequency (Hz)')
	ax1.set_zlabel('Amplitude (r.u.)')

	ax2 = fig1.add_subplot(1, 2, 2, projection='3d')
	ax2.plot_surface(X, Y, cmapE, cmap=cm.hot)
	ax2.set_xlabel('Pedal Cicle (%)')
	ax2.set_ylabel('Frequency (Hz)')
	ax2.set_zlabel('Amplitude (r.u.)')

	pp.savefig(fig1)