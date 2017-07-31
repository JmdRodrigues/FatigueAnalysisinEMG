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
from matplotlib.patches import Circle
from scipy import stats
from decimal import Decimal
from novainstrumentation import smooth
from RadarChart import radar_factory
from matplotlib.backends.backend_pdf import PdfPages


def plotEMG(pks_start, pks_end, emg, pp):
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

    # Graphical Illustration of the segmentation procedure.
    fig1 = plt.figure(subplotpars=pars)
    fig1.set_facecolor((face_color_r, face_color_g, face_color_b))
    fig1.set_dpi(96)
    fig1.set_figheight(1080 / 96)
    fig1.set_figwidth(1920 / 96)
    fig1.suptitle("EMG Segmentation")

    time = np.linspace(0, len(emg) / 1000, len(emg))

    plt.plot(time, emg)
    plt.vlines(x=np.divide(pks_start, 1000.0), ymin=min(emg), ymax=max(emg), colors='orange')
    # plt.vlines(x=np.divide(pks_end, 1000.0), ymin=min(emg), ymax=max(emg), colors='yellow')
    plt.xlim((100, 110))

    pp.savefig(fig1)

    # Release Memory.
    plt.close(fig1)


def plotParameters(MajorF, MeanP, BurstPos, width, height, PixelArea, HullArea, HullVolume, pp, Title, analysis,
                   nbr_Burst=None, show=False, txt_data_temp=None, txt_data_global=None):
    # Copy of reference axis.
    nbr_Burst_aux = list(nbr_Burst)

    # Fonts
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

    smooth_factor = 0.05
    scale_factor = 5

    # Major Frequency Plot.
    fig1 = plt.figure(subplotpars=pars)
    fig1.set_facecolor((face_color_r, face_color_g, face_color_b))
    fig1.set_dpi(96)
    fig1.set_figheight(1080 / 96)
    fig1.set_figwidth(1920 / 96)
    fig1.suptitle(Title)
    # fig1.subplotpars(pars)

    # Figure Structure.
    ax11 = plt.subplot(3, 1, 1)
    r, m, y, MajorF, nbr_Burst_aux = plotParam(nbr_Burst, MajorF, ax11, 'Major Frequency', 'Major Frequency', 'Hz',
                                               font1, font2)
    # r, m, y = plotParam(nbr_Burst, MajorF, ax11, 'Major Frequency', 'Major Frequency', 'Hz', font1, font2)

    # Txt data storage.
    if analysis in [2, 4, 5]:
        # Complete txt data array.
        txt_data_temp.append("Major Frequency")
        txt_data_temp.append(r)

    # Major Frequency Deviation from regression line.
    # Figure Segment 2.
    ax12 = plt.subplot(3, 1, 2)
    deviation = np.array(MajorF) - np.array(y)
    r, m, y = plotParam(nbr_Burst_aux, deviation, ax12, 'Major Frequency Deviation', 'Deviation', 'Hz', font1, font2)[
              :3]

    if analysis in [2, 4, 5]:
        # Complete txt data array.
        txt_data_temp.append("Major Frequency Deviation")
        txt_data_temp.append(r)

    # Figure Segment 3.
    ax13 = plt.subplot(3, 1, 3)
    absolute_deviation = np.absolute(deviation)
    r, m, y = plotParam(nbr_Burst_aux, absolute_deviation, ax13, 'Major Frequency Absolute Deviation',
                        'Absolute Deviation', 'Hz', font1, font2)[:3]

    if analysis in [2, 4, 5]:
        # Complete txt data array.
        txt_data_temp.append("Major Frequency Absolute Deviation")
        txt_data_temp.append(r)

    # Figure Creation.
    pp.savefig(fig1)
    # Release Memory.
    plt.close(fig1)

    # Smooth Phase.
    if smooth_thres_factor(len(MajorF), smooth_factor, scale_factor):
        fig10 = plt.figure(subplotpars=pars)
        fig10.set_facecolor((face_color_r, face_color_g, face_color_b))
        fig10.set_dpi(96)
        fig10.set_figheight(1080 / 96)
        fig10.set_figwidth(1920 / 96)
        # fig1.subplotpars(pars)

        # Major Frequency Plot Smooth Analysis.
        ax101 = plt.subplot(3, 1, 1)
        ax102 = plt.subplot(3, 1, 2)
        ax103 = plt.subplot(3, 1, 3)
        FlagValidation10 = plotSmooth(nbr_Burst_aux, MajorF, fig10, ax101, ax102, ax103, Title, 'Major Frequency',
                                      'Major Frequency', 'Hz', font1, font2, smooth_factor)

        if FlagValidation10 == True:
            # Figure Creation.
            pp.savefig(fig10)
            # Release Memory.
            plt.close(fig10)

    # Mean Power Plot.
    fig2 = plt.figure(subplotpars=pars)
    fig2.set_facecolor((face_color_r, face_color_g, face_color_b))
    fig2.set_dpi(96)
    fig2.set_figheight(1080 / 96)
    fig2.set_figwidth(1920 / 96)
    fig2.suptitle(Title)
    # fig1.subplotpars(pars)

    # Figure Structure.
    # Mean Power Plot.
    ax21 = plt.subplot(3, 1, 1)
    r, m, y, MeanP, nbr_Burst_aux = plotParam(nbr_Burst, MeanP, ax21, 'Mean Power', 'Mean Power', 'r.u.', font1, font2)

    # Txt data storage.
    if analysis in [2, 4, 5]:
        # Complete txt data array.
        txt_data_temp.append("Mean Power")
        txt_data_temp.append(r)

    # Mean Power Deviation from regression line.
    # Figure Segment 2.
    ax22 = plt.subplot(3, 1, 2)
    deviation = np.array(MeanP) - np.array(y)
    r, m, y = plotParam(nbr_Burst_aux, deviation, ax22, 'Mean Power Deviation', 'Deviation', 'r.u.', font1, font2)[:3]

    if analysis in [2, 4, 5]:
        # Complete txt data array.
        txt_data_temp.append("Mean Power Deviation")
        txt_data_temp.append(r)

    # Figure Segment 3.
    ax23 = plt.subplot(3, 1, 3)
    absolute_deviation = np.absolute(deviation)
    r, m, y = plotParam(nbr_Burst_aux, absolute_deviation, ax23, 'Mean Power Absolute Deviation', 'Absolute Deviation',
                        'r.u.', font1, font2)[:3]

    if analysis in [2, 4, 5]:
        # Complete txt data array.
        txt_data_temp.append("Mean Power Absolute Deviation")
        txt_data_temp.append(r)

    # Figure Creation.
    pp.savefig(fig2)
    # Release Memory.
    plt.close(fig2)

    # Smooth Phase.
    if smooth_thres_factor(len(MajorF), smooth_factor, scale_factor):
        fig20 = plt.figure(subplotpars=pars)
        fig20.set_facecolor((face_color_r, face_color_g, face_color_b))
        fig20.set_dpi(96)
        fig20.set_figheight(1080 / 96)
        fig20.set_figwidth(1920 / 96)
        # fig1.subplotpars(pars)

        # Mean Power Smooth Analysis.
        ax201 = plt.subplot(3, 1, 1)
        ax202 = plt.subplot(3, 1, 2)
        ax203 = plt.subplot(3, 1, 3)
        FlagValidation20 = plotSmooth(nbr_Burst_aux, MeanP, fig20, ax201, ax202, ax203, Title, 'Mean Power',
                                      'Mean Power', 'r.u.', font1, font2, smooth_factor)

        if FlagValidation20 == True:
            # Figure Creation.
            pp.savefig(fig20)
            # Release Memory.
            plt.close(fig20)

    # Centroid Position Plot.
    fig3 = plt.figure(subplotpars=pars)
    fig3.set_facecolor((face_color_r, face_color_g, face_color_b))
    fig3.set_dpi(96)
    fig3.set_figheight(1080 / 96)
    fig3.set_figwidth(1920 / 96)
    fig3.suptitle(Title)
    # fig1.subplotpars(pars)

    # Figure Structure.
    # Centroid Position Plot.
    # Final Stage of data manipulation (Removal of null [] entries).
    ax31 = plt.subplot(3, 1, 1)
    val_ent = np.where(np.array(BurstPos) != False)[0]
    nbr_Burst_aux = np.array(nbr_Burst)[val_ent]
    BurstPos_aux = np.multiply(np.array(BurstPos)[val_ent], 100)

    ax31.set_title('Centroid Position Over The Pedal Cycle', fontproperties=font2)  # limit from 0 and 1
    ax31.plot(nbr_Burst_aux, BurstPos_aux)
    ax31.set_ylim((0, 100))
    ax31.set_ylabel("Centroid Position (% of pedal Cycle)", fontproperties=font1)
    ax31.set_xlabel("Burst/Set of Bursts", fontproperties=font1)
    ax31.set_xlim(0)
    ax31.set_ylim(min(BurstPos_aux) - 0.10 * (max(BurstPos_aux) - min(BurstPos_aux)),
                  max(BurstPos_aux) + 0.10 * (max(BurstPos_aux) - min(BurstPos_aux)))

    # Plot of the regression line.
    x, y, r, m = plotRegline(nbr_Burst_aux, BurstPos_aux)
    ax31.plot(x, y)
    ax31.text(nbr_Burst_aux[len(nbr_Burst_aux) - 1], max(np.multiply(BurstPos, 100)),
              "Corr. Coeff. (r^2) = " + str(round(r, 2)) + "\nSlope (m) = " + str(round(m, 2)),
              bbox=dict(facecolor='white'), fontsize=8)

    if analysis in [2, 4, 5]:
        # Complete txt data array.
        txt_data_temp.append("Centroid Position (% of pedal cycle)")
        txt_data_temp.append(r)

    # Centroid Position Deviation from regression line.
    # Figure Segment 2.
    ax32 = plt.subplot(3, 1, 2)
    deviation = np.array(BurstPos_aux) - np.array(y)
    r, m, y = plotParam(nbr_Burst_aux, deviation, ax32, 'Centroid Position Deviation', 'Deviation', 'r.u.', font1,
                        font2)[:3]

    if analysis in [2, 4, 5]:
        # Complete txt data array.
        txt_data_temp.append("Centroid Position Deviation")
        txt_data_temp.append(r)

    # Figure Segment 3.
    ax33 = plt.subplot(3, 1, 3)
    absolute_deviation = np.absolute(deviation)
    r, m, y = plotParam(nbr_Burst_aux, absolute_deviation, ax33, 'Centroid Position Absolute Deviation',
                        'Absolute Deviation', 'r.u.', font1, font2)[:3]

    if analysis in [2, 4, 5]:
        # Complete txt data array.
        txt_data_temp.append("Centroid Position Absolute Deviation")
        txt_data_temp.append(r)

    # Figure Creation.
    pp.savefig(fig3)
    # Release Memory.
    plt.close(fig3)

    # Smooth Phase.
    if smooth_thres_factor(len(MajorF), smooth_factor, scale_factor):
        # Centroid Position Plot - Smooth Analysis.
        fig30 = plt.figure(subplotpars=pars)
        fig30.set_dpi(96)
        fig30.set_figheight(1080 / 96)
        fig30.set_figwidth(1920 / 96)

        ax301 = plt.subplot(3, 1, 1)
        ax302 = plt.subplot(3, 1, 2)
        ax303 = plt.subplot(3, 1, 3)
        FlagValidation30 = plotSmooth(nbr_Burst_aux, BurstPos_aux, fig30, ax301, ax302, ax303, Title,
                                      'Centroid Position', 'Centroid Position', '% of pedal Cycle', font1, font2,
                                      smooth_factor)

        if FlagValidation30 == True:
            # Figure Creation.
            pp.savefig(fig30)
            # Release Memory.
            plt.close(fig30)

    if analysis != 4:
        # Time Dispersion Plot.
        fig4 = plt.figure(subplotpars=pars)
        fig4.set_dpi(96)
        fig4.set_figheight(1080 / 96)
        fig4.set_figwidth(1920 / 96)
        fig4.suptitle(Title)

        # Figure Structure.
        ax41 = plt.subplot(3, 1, 1)
        r, m, y, width, nbr_Burst_aux = plotParam(nbr_Burst, width, ax41, 'Time Dispersion', 'Width Amplitude', 'r.u.',
                                                  font1, font2)

        # Txt Data Storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Time Dispersion")
            txt_data_temp.append(r)

        # Time Dispersion Deviation from regression line.
        # Figure Segment 2.
        ax42 = plt.subplot(3, 1, 2)
        deviation = np.array(width) - np.array(y)
        r, m, y = plotParam(nbr_Burst_aux, deviation, ax42, 'Time Dispersion Deviation', 'Deviation', 'r.u.', font1,
                            font2)[:3]

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Time Dispersion Deviation")
            txt_data_temp.append(r)

        # Figure Segment 3.
        ax43 = plt.subplot(3, 1, 3)
        absolute_deviation = np.absolute(deviation)
        r, m, y = plotParam(nbr_Burst_aux, absolute_deviation, ax43, 'Time Dispersion Absolute Deviation',
                            'Absolute Deviation', 'r.u.', font1, font2)[:3]

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Time Dispersion Absolute Deviation")
            txt_data_temp.append(r)

        # Figure Creation.
        pp.savefig(fig4)
        # Release Memory.
        plt.close(fig4)

        # Smooth Phase.
        if smooth_thres_factor(len(MajorF), smooth_factor, scale_factor):
            # Temporal Dispersion Plot - Smooth Analysis.
            fig40 = plt.figure(subplotpars=pars)
            fig40.set_dpi(96)
            fig40.set_figheight(1080 / 96)
            fig40.set_figwidth(1920 / 96)

            ax401 = plt.subplot(3, 1, 1)
            ax402 = plt.subplot(3, 1, 2)
            ax403 = plt.subplot(3, 1, 3)
            FlagValidation40 = plotSmooth(nbr_Burst_aux, width, fig40, ax401, ax402, ax403, Title, 'Time Dispersion',
                                          'Width Amplitude', 'r.u.', font1, font2, smooth_factor)

            if FlagValidation40 == True:
                # Figure Creation.
                pp.savefig(fig40)
                # Release Memory.
                plt.close(fig40)

        # Frequency Dispersion Plot.
        fig5 = plt.figure(subplotpars=pars)
        fig5.set_dpi(96)
        fig5.set_figheight(1080 / 96)
        fig5.set_figwidth(1920 / 96)
        fig5.suptitle(Title)

        # Figure Structure.
        ax51 = plt.subplot(3, 1, 1)
        r, m, y, height, nbr_Burst_aux = plotParam(nbr_Burst, height, ax51, 'Frequency Dispersion', 'Frequency Range',
                                                   'Hz', font1, font2)

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Frequency Dispersion")
            txt_data_temp.append(r)

        # Frequency Dispersion Deviation from regression line.
        # Figure Segment 2.
        ax52 = plt.subplot(3, 1, 2)
        deviation = np.array(height) - np.array(y)
        r, m, y = plotParam(nbr_Burst_aux, deviation, ax52, 'Frequency Dispersion Deviation', 'Deviation', 'Hz', font1,
                            font2)[:3]

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Frequency Dispersion Deviation")
            txt_data_temp.append(r)

        # Figure Segment 3.
        ax53 = plt.subplot(3, 1, 3)
        absolute_deviation = np.absolute(deviation)
        r, m, y = plotParam(nbr_Burst_aux, absolute_deviation, ax53, 'Frequency Dispersion Absolute Deviation',
                            'Absolute Deviation', 'Hz', font1, font2)[:3]

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Frequency Dispersion Absolute Deviation")
            txt_data_temp.append(r)

        # Figure Creation.
        pp.savefig(fig5)
        # Release Memory.
        plt.close(fig5)

        # Smooth Phase.
        if smooth_thres_factor(len(MajorF), smooth_factor, scale_factor):
            # Frequency Dispersion Plot - Smooth Analysis.
            fig50 = plt.figure(subplotpars=pars)
            fig50.set_dpi(96)
            fig50.set_figheight(1080 / 96)
            fig50.set_figwidth(1920 / 96)

            ax501 = plt.subplot(3, 1, 1)
            ax502 = plt.subplot(3, 1, 2)
            ax503 = plt.subplot(3, 1, 3)
            FlagValidation50 = plotSmooth(nbr_Burst_aux, height, fig50, ax501, ax502, ax503, Title,
                                          'Frequency Dispersion', 'Frequency Range', 'Hz', font1, font2, smooth_factor)

            if FlagValidation50 == True:
                # Figure Creation.
                pp.savefig(fig50)
                # Release Memory.
                plt.close(fig50)

        # Area in Pixels Plot.
        fig6 = plt.figure(subplotpars=pars)
        fig6.set_dpi(96)
        fig6.set_figheight(1080 / 96)
        fig6.set_figwidth(1920 / 96)
        fig6.suptitle(Title)

        # Figure Structure.
        ax61 = plt.subplot(3, 1, 1)
        r, m, y, PixelArea, nbr_Burst_aux = plotParam(nbr_Burst, PixelArea, ax61, 'Area in Pixels', 'Area', '#Pixels',
                                                      font1, font2)

        # Txt Data Storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Area in Pixels")
            txt_data_temp.append(r)

        # Area in Pixels Deviation from regression line.
        # Figure Segment 2.
        ax62 = plt.subplot(3, 1, 2)
        deviation = np.array(PixelArea) - np.array(y)
        r, m, y = plotParam(nbr_Burst_aux, deviation, ax62, 'Area in Pixels Deviation', 'Deviation', '#Pixels', font1,
                            font2)[:3]

        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Area in Pixels Deviation")
            txt_data_temp.append(r)

        # Figure Segment 3.
        ax63 = plt.subplot(3, 1, 3)
        absolute_deviation = np.absolute(deviation)
        r, m, y = plotParam(nbr_Burst_aux, absolute_deviation, ax63, 'Area in Pixels Absolute Deviation',
                            'Absolute Deviation', '#Pixels', font1, font2)[:3]

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Area in Pixels Absolute Deviation")
            txt_data_temp.append(r)

        # Figure Creation.
        pp.savefig(fig6)
        # Release Memory.
        plt.close(fig6)

        # Smooth Phase.
        if smooth_thres_factor(len(MajorF), smooth_factor, scale_factor):
            # Pixel Area Plot - Smooth Analysis.
            fig60 = plt.figure(subplotpars=pars)
            fig60.set_dpi(96)
            fig60.set_figheight(1080 / 96)
            fig60.set_figwidth(1920 / 96)

            ax601 = plt.subplot(3, 1, 1)
            ax602 = plt.subplot(3, 1, 2)
            ax603 = plt.subplot(3, 1, 3)
            FlagValidation60 = plotSmooth(nbr_Burst_aux, PixelArea, fig60, ax601, ax602, ax603, Title, 'Area in Pixels',
                                          'Area in Pixels', '#Pixels', font1, font2, smooth_factor)

            if FlagValidation60 == True:
                # Figure Creation.
                pp.savefig(fig60)
                # Release Memory.
                plt.close(fig60)

        # Convex Hull Area Plot.
        fig7 = plt.figure(subplotpars=pars)
        fig7.set_dpi(96)
        fig7.set_figheight(1080 / 96)
        fig7.set_figwidth(1920 / 96)
        fig7.suptitle(Title)

        # Figure Structure.
        ax71 = plt.subplot(3, 1, 1)
        r, m, y, HullArea, nbr_Burst_aux = plotParam(nbr_Burst, HullArea, ax71, 'Convex Hull Area', 'Area', 'r.u.',
                                                     font1, font2)

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Convex Hull Area")
            txt_data_temp.append(r)

        # Convex Hull Area Deviation from regression line.
        # Figure Segment 2.
        ax72 = plt.subplot(3, 1, 2)
        deviation = np.array(HullArea) - np.array(y)
        r, m, y = plotParam(nbr_Burst_aux, deviation, ax72, 'Convex Hull Area Deviation', 'Deviation', 'r.u.', font1,
                            font2)[:3]

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Convex Hull Area Deviation")
            txt_data_temp.append(r)

        # Figure Segment 3.
        ax73 = plt.subplot(3, 1, 3)
        absolute_deviation = np.absolute(deviation)
        r, m, y = plotParam(nbr_Burst_aux, absolute_deviation, ax73, 'Convex Hull Area Absolute Deviation',
                            'Absolute Deviation', 'r.u.', font1, font2)[:3]

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Convex Hull Area Absolute Deviation")
            txt_data_temp.append(r)

        # Figure Creation.
        pp.savefig(fig7)
        # Release Memory.
        plt.close(fig7)

        # Smooth Phase.
        if smooth_thres_factor(len(MajorF), smooth_factor, scale_factor):
            # Convex Hull Area Plot - Smooth Analysis.
            fig70 = plt.figure(subplotpars=pars)
            fig70.set_dpi(96)
            fig70.set_figheight(1080 / 96)
            fig70.set_figwidth(1920 / 96)

            ax701 = plt.subplot(3, 1, 1)
            ax702 = plt.subplot(3, 1, 2)
            ax703 = plt.subplot(3, 1, 3)
            FlagValidation70 = plotSmooth(nbr_Burst_aux, HullArea, fig70, ax701, ax702, ax703, Title, 'Area', 'Area',
                                          'r.u.', font1, font2, smooth_factor)

            if FlagValidation70 == True:
                # Figure Creation.
                pp.savefig(fig70)
                # Release Memory.
                plt.close(fig70)

        # Convex Hull Volume Plot.
        fig8 = plt.figure(subplotpars=pars)
        fig8.set_dpi(96)
        fig8.set_figheight(1080 / 96)
        fig8.set_figwidth(1920 / 96)
        fig8.suptitle(Title)

        # Figure Structure.
        ax81 = plt.subplot(3, 1, 1)
        r, m, y, HullVolume, nbr_Burst_aux = plotParam(nbr_Burst, HullVolume, ax81, 'Convex Hull Volume', 'Volume',
                                                       'r.u.', font1, font2)

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Convex Hull Volume")
            txt_data_temp.append(r)
            txt_data_global.append(txt_data_temp)

        # Convex Hull Volume Deviation from regression line.
        # Figure Segment 2.
        ax82 = plt.subplot(3, 1, 2)
        deviation = np.array(HullVolume) - np.array(y)
        r, m, y = plotParam(nbr_Burst_aux, deviation, ax82, 'Convex Hull Volume Deviation', 'Volume Deviation', 'r.u.',
                            font1, font2)[:3]

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Convex Hull Volume Deviation")
            txt_data_temp.append(r)

        # Figure Segment 3.
        ax83 = plt.subplot(3, 1, 3)
        absolute_deviation = np.absolute(deviation)
        r, m, y = plotParam(nbr_Burst_aux, absolute_deviation, ax83, 'Convex Hull Volume Absolute Deviation',
                            'Volume Absolute Deviation', 'r.u.', font1, font2)[:3]

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Convex Hull Volume Absolute Deviation")
            txt_data_temp.append(r)

        # Figure Creation.
        pp.savefig(fig8)
        # Release Memory.
        plt.close(fig8)

        # Smooth Phase.
        if smooth_thres_factor(len(MajorF), smooth_factor, scale_factor):
            # Hull Volume Plot - Smooth Analysis.
            fig80 = plt.figure(subplotpars=pars)
            fig80.set_dpi(96)
            fig80.set_figheight(1080 / 96)
            fig80.set_figwidth(1920 / 96)

            ax801 = plt.subplot(3, 1, 1)
            ax802 = plt.subplot(3, 1, 2)
            ax803 = plt.subplot(3, 1, 3)
            FlagValidation80 = plotSmooth(nbr_Burst_aux, HullVolume, fig80, ax801, ax802, ax803, Title,
                                          'Convex Hull Volume', 'Convex Hull Volume', 'r.u.', font1, font2,
                                          smooth_factor)

            if FlagValidation80 == True:
                # Figure Creation.
                pp.savefig(fig80)
                # Release Memory.
                plt.close(fig80)

    else:
        # Convex Hull Volume Plot.
        fig9 = plt.figure(subplotpars=pars)
        fig9.set_dpi(96)
        fig9.set_figheight(1080 / 96)
        fig9.set_figwidth(1920 / 96)
        fig9.suptitle(Title)

        # Figure Structure.
        ax91 = plt.subplot(3, 1, 1)
        r, m, y, HullVolume, nbr_Burst_aux = plotParam(nbr_Burst, HullVolume, ax91, 'Convex Hull Volume', 'Volume',
                                                       'r.u.', font1, font2)

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Convex Hull Volume")
            txt_data_temp.append(r)
            txt_data_global.append(txt_data_temp)

        # Convex Hull Volume Deviation from regression line.
        # Figure Segment 2.
        ax92 = plt.subplot(3, 1, 2)
        deviation = np.array(HullVolume) - np.array(y)
        r, m, y = plotParam(nbr_Burst_aux, deviation, ax92, 'Convex Hull Volume Deviation', 'Volume Deviation', 'r.u.',
                            font1, font2)[:3]

        # Txt data storage.
        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Convex Hull Volume Deviation")
            txt_data_temp.append(r)

        # Figure Segment 3.
        ax93 = plt.subplot(3, 1, 3)
        absolute_deviation = np.absolute(deviation)
        r, m, y = plotParam(nbr_Burst_aux, absolute_deviation, ax93, 'Convex Hull Volume Absolute Deviation',
                            'Volume Absolute Deviation', 'r.u.', font1, font2)[:3]

        if analysis in [2, 4, 5]:
            # Complete txt data array.
            txt_data_temp.append("Convex Hull Volume Absolute Deviation")
            txt_data_temp.append(r)

        # Figure Creation.
        pp.savefig(fig9)
        # Release Memory.
        plt.close(fig9)

        # Smooth Phase.
        if smooth_thres_factor(len(MajorF), smooth_factor, scale_factor):
            # Convex Hull Volume Plot - Smooth Analysis.
            fig90 = plt.figure(subplotpars=pars)
            fig90.set_dpi(96)
            fig90.set_figheight(1080 / 96)
            fig90.set_figwidth(1920 / 96)

            ax901 = plt.subplot(3, 1, 1)
            ax902 = plt.subplot(3, 1, 2)
            ax903 = plt.subplot(3, 1, 3)
            FlagValidation90 = plotSmooth(nbr_Burst_aux, HullVolume, fig90, ax901, ax902, ax903, Title,
                                          'Convex Hull Volume', 'Convex Hull Volume', 'r.u.', font1, font2,
                                          smooth_factor)

            if FlagValidation90 == True:
                # Figure Creation.
                pp.savefig(fig90)
                # Release Memory.
                plt.close(fig90)

    plt.close('all')
    if show == True:
        plt.show()

    return txt_data_global


def PlotMap3(Begin, End, maxT, coorB, coorE, hullAB, hullAE, pointsB, pointsE, pp, nbr):
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
    y = np.linspace(5, len(Begin) + 5, len(Begin))
    X, Y = np.meshgrid(x, y)
    pointsB[:, 0] = np.multiply(np.divide(pointsB[:, 0], len(x)), 100)
    pointsE[:, 0] = np.multiply(np.divide(pointsE[:, 0], len(x)), 100)

    fig1 = plt.figure(subplotpars=pars)
    fig1.set_facecolor((face_color_r, face_color_g, face_color_b))
    fig1.set_dpi(96)
    fig1.set_figheight(1080 / 96)
    fig1.set_figwidth(1920 / 96)
    fig1.suptitle("Analysis of the Beginning and End of the Spectrum " + "(Average sets of " + str(nbr) + " Scalogram)")

    ax1 = plt.subplot(2, 1, 1)
    # im1 = ax1.pcolormesh(X, Y, Begin, cmap=cm.hot, vmax=maxT, vmin=0)
    im1 = ax1.pcolormesh(X, Y, Begin / maxT, cmap=cm.hot, vmax=1.0, vmin=0)
    fig1.colorbar(im1, ax=ax1)
    for simplex in hullAB.simplices:
        ax1.plot(pointsB[simplex, 0], pointsB[simplex, 1], 'b-')
    #plt.legend(facecolor='b')
    ax1.set_xlabel('Pedal Cycle (%)')
    ax1.set_ylabel('Frequency (Hz)')
    # print(coorB)
    circ1 = Circle(coorB, 1, label="Weighted Centroid")
    ax1.add_patch(circ1)

    ax2 = plt.subplot(2, 1, 2)
    # im2 = ax2.pcolormesh(X, Y, End, cmap=cm.hot, vmax=maxT, vmin=0)
    im2 = ax2.pcolormesh(X, Y, End / maxT, cmap=cm.hot, vmax=1.0, vmin=0)
    fig1.colorbar(im2, ax=ax2)

    for simplex in hullAE.simplices:
        ax2.plot(pointsE[simplex, 0], pointsE[simplex, 1], 'b-')
    #plt.legend(facecolor='b')
    ax2.set_xlabel('Pedal Cycle (%)')
    ax2.set_ylabel('Frequency (Hz)')

    circ2 = Circle(coorE, 1, label="Weighted Centroid")
    ax2.add_patch(circ2)

    # plt.show()
    pp.savefig(fig1)
    # Release Memory.
    plt.close(fig1)


def PlotParam3(BeginParams, EndParams, pp, nbr):
    MFB, MaxFB, MP1B, MP2B, BPB, A1B, A2B, VolB, WB, HB, hullB, pointsB, nbr_Burst = BeginParams
    MFE, MaxFE, MP1E, MP2E, BPE, A1E, A2E, VolE, WE, HE, hullE, pointsE, nbr_Burst = EndParams

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
    fig1.suptitle("Analysis of the Beginning and End of the Spectrum " + "(Average sets of " + str(nbr) + " Scalogram)")
    # 8 analises
    index = [0, 1]
    ax11 = plt.subplot(4, 2, 1)
    ax11.bar(0, MFB, color='b', label='Begin', width=bar_width)
    ax11.bar(1, MFE, color='orange', label='End', width=bar_width)
    ax11.set_title("Mean Frequency")

    ax12 = plt.subplot(4, 2, 2)
    ax12.bar(0, MP1B, color='b', label='Begin', width=bar_width)
    ax12.bar(1, MP1E, color='orange', label='End', width=bar_width)
    ax12.set_title("Mean Power")

    ax21 = plt.subplot(4, 2, 3)
    ax21.bar(0, BPB, color='b', label='Begin', width=bar_width)
    ax21.bar(1, BPE, color='orange', label='End', width=bar_width)
    ax21.set_title("Burst Position")

    ax22 = plt.subplot(4, 2, 4)
    ax22.bar(0, A1B, color='b', label='Begin', width=bar_width)
    ax22.bar(1, A1E, color='orange', label='End', width=bar_width)
    ax22.set_title("Area 1")

    ax31 = plt.subplot(4, 2, 5)
    ax31.bar(0, A2B, color='b', label='Begin', width=bar_width)
    ax31.bar(1, A2E, color='orange', label='End', width=bar_width)
    ax31.set_title("Area 2")

    ax32 = plt.subplot(4, 2, 6)
    ax32.bar(0, VolB, color='b', label='Begin', width=bar_width)
    ax32.bar(1, VolE, color='orange', label='End', width=bar_width)
    ax32.set_title("Volume")

    ax41 = plt.subplot(4, 2, 7)
    ax41.bar(0, WB, color='b', label='Begin', width=bar_width)
    ax41.bar(1, WE, color='orange', label='End', width=bar_width)
    ax41.set_title("Width of Spectrum Activation")

    ax42 = plt.subplot(4, 2, 8)
    lb, = ax42.bar(0, HB, color='b', label='Begin', width=bar_width)
    le, = ax42.bar(1, HE, color='orange', label='End', width=bar_width)
    ax42.set_title("Frequency of Spectrum Activation")

    plt.xlabel('Group')
    plt.ylabel('Scores')
    fig1.legend(handles=[lb, le], labels=['begin', 'end'], loc='upper right', shadow=True, fancybox=True)

    pp.savefig(fig1)
    # Release Memory.
    plt.close(fig1)


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
    fig1.suptitle("Analysis of the Beginning and End of the Spectrum")
    x = np.linspace(0, len(cmap[0]) / 1000, len(cmap[0]))
    y = np.linspace(5, len(cmap) + 5, len(cmap))
    X, Y = np.meshgrid(x, y)
    ax = p3.Axes3D(fig1)
    ax.plot_surface(X, Y, cmap, cmap=cm.hot)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_zlabel('Amplitude (r.u.)')

    pp.savefig(fig1)
    # Release Memory.
    plt.close(fig1)


def plotBurst3D(cmapB, cmapE, pp, maxT, nbr):
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
    fig1.suptitle("Analysis of the Beginning and End of the Spectrum " + "(Average sets of " + str(nbr) + " Scalogram)")

    x = np.linspace(0, 100, len(cmapB[0]))
    y = np.linspace(5, len(cmapB) + 5, len(cmapB))
    X, Y = np.meshgrid(x, y)

    ax1 = fig1.add_subplot(1, 2, 1, projection='3d')
    im1 = ax1.plot_surface(X, Y, cmapB / maxT, cmap=cm.hot, vmin=0, vmax=maxT / maxT)
    ax1.set_xlabel('Pedal Cycle (%)')
    ax1.set_ylabel('Frequency (Hz)')
    ax1.set_zlabel('Amplitude (r.u.)')

    ax2 = fig1.add_subplot(1, 2, 2, projection='3d')
    im2 = ax2.plot_surface(X, Y, cmapE / maxT, cmap=cm.hot, vmin=0, vmax=maxT / maxT)
    ax2.set_xlabel('Pedal Cycle (%)')
    ax2.set_ylabel('Frequency (Hz)')
    ax2.set_zlabel('Amplitude (r.u.)')

    if np.max(cmapE) > np.max(cmapB):
        fig1.colorbar(im2, ax=ax2)
        fig1.colorbar(im2, ax=ax1)
    else:
        fig1.colorbar(im1, ax=ax1)
        fig1.colorbar(im1, ax=ax2)

    pp.savefig(fig1)
    # Release Memory.
    plt.close(fig1)


def plotRegline(time_axis, sample_axis):
    if time_axis != [] and sample_axis != []:
        # Generation of regression line points.
        m_slope, b_intercept, r_value = stats.linregress(time_axis, sample_axis)[:3]

        regress_line = []

        for counter_line in range(0, len(time_axis)):
            regress_line.append(m_slope * time_axis[counter_line] + b_intercept)

        r2 = r_value ** 2

        return time_axis, regress_line, r2, m_slope
    else:
        return [], [], 0, 0


def plotSmooth(nbr_Burst, data, fig, axis1, axis2, axis3, figTitle, plot_title, axis1Title, units, font1, font2,
               smooth_factor):
    fig.suptitle(figTitle)
    # fig1.subplotpars(pars)

    # Final Stage of data manipulation (Removal of null [] entries).
    val_ent = np.where(np.array(data) != False)[0]
    nbr_Burst = np.array(nbr_Burst)[val_ent]
    data = np.array(data)[val_ent]

    axis1.plot(nbr_Burst, data)  # limit from min and max frequencies
    # ax11.plot(nbr_Burst, MajorF, '.', linewidth=0)  # limit from min and max frequencies
    axis1.set_title(plot_title, fontproperties=font2)
    axis1.set_ylabel(axis1Title + " " + "(" + units + ")", fontproperties=font1)
    axis1.set_xlabel("Burst/Set of Bursts", fontproperties=font1)
    axis1.set_xlim(0)

    # Plot of the smooth line.
    smooth_line = smooth(data, int(len(data) * smooth_factor))
    axis1.plot(nbr_Burst, smooth_line)

    # Major Frequency Deviation from regression line.
    deviation = data - smooth_line
    absolute_deviation = np.absolute(deviation)

    axis2.plot(nbr_Burst, deviation)  # limit from min and max frequencies
    # ax11.plot(nbr_Burst, MajorF, '.', linewidth=0)  # limit from min and max frequencies
    axis2.set_title(plot_title + " " + 'Deviation', fontproperties=font2)
    axis2.set_ylabel("Deviation" + " " + "(" + units + ")", fontproperties=font1)
    axis2.set_xlabel("Burst/Set of Bursts", fontproperties=font1)
    axis2.set_xlim(0)

    axis3.plot(nbr_Burst, absolute_deviation)  # limit from min and max frequencies
    # ax11.plot(nbr_Burst, MajorF, '.', linewidth=0)  # limit from min and max frequencies
    axis3.set_title(plot_title + " " + 'Absolute Deviation', fontproperties=font2)
    axis3.set_ylabel("Absolute Deviation" + " " + "(" + units + ")", fontproperties=font1)
    axis3.set_xlabel("Burst/Set of Bursts", fontproperties=font1)
    axis3.set_xlim(0)

    if list(smooth_line) == list(data):
        FlagValidation = False
    else:
        FlagValidation = True

    return FlagValidation


def plotParam(nburst, data, axis, title, ylabel, units, font1, font2):
    # Final Stage of data manipulation (Removal of null [] entries).
    val_ent = np.where(np.array(data) != False)[0]
    nbr_Burst_aux = np.array(nburst)[val_ent]
    data = np.array(data)[val_ent]

    if len(nbr_Burst_aux) != 0 and len(data) != 0:
        axis.plot(nbr_Burst_aux, data)  # limit from min and max frequencies
        axis.set_title(title, fontproperties=font2)
        axis.set_ylabel(ylabel + " " + "(" + units + ")", fontproperties=font1)
        axis.set_xlabel("Burst/Set of Bursts", fontproperties=font1)
        axis.set_xlim(0)

        # Plot of the regression line.
        x, y, r, m = plotRegline(nbr_Burst_aux, data)
        axis.plot(x, y)
        axis.text(nbr_Burst_aux[len(nbr_Burst_aux) - 1], max(data),
                  "Corr. Coeff. (r^2) = " + str(round(r, 2)) + "\nSlope (m) = " + str(round(m, 2)),
                  bbox=dict(facecolor='white'), fontsize=8)

        return r, m, y, data, nbr_Burst_aux
    else:
        return 0, 0, [], data, nbr_Burst_aux


# Smooth threshold parameter.
def smooth_thres_factor(length, smooth_factor, scale_factor):
    return scale_factor * np.ceil(smooth_factor * length) < length and np.ceil(smooth_factor * length) > 1


# Function responsible for the Grid Representation of the parameter evolution plots.
def SynthesisGrid(pandaData, pp, colIn="PName", rowIn="Msc"):
    sns.set(style="ticks", color_codes=True)

    # Data Conversion (Work Around because of conversion of int to string when the panda data is created).
    pandaData['#Set'] = pandaData['#Set'].astype('int')
    pandaData['PValue'] = pandaData['PValue'].astype('float64')
    maxTime = np.max(pandaData['#Set'])

    # Analysis per Subject - Data Frame Creation.
    dataFrame = sns.FacetGrid(pandaData, col=colIn, row=rowIn, sharex=False, sharey=False)
    dataFrame = dataFrame.map(sns.regplot, "#Set", "PValue").set(xticks=list(np.arange(0, maxTime + 2, 2)))

    # Legend Text.
    figText = plt.figure()
    plt.text(0, 0,
             'Legend' + '\n\n' + '----- Muscles (Msc) -----' + '\n' + '\tRF - Rectus Femoris\n\tVL - Vastus Lateralis\n\tVM - Vastus Medialis\n\tST - Semitendinosus\n\tBF - Biceps Femoris\n\n' + '----- Parameters (PName) ----- ' + '\n\tMF - Major Frequency (Hz)\n\tMP - Mean Power (r.u.)\n\tCP - Centroid Position (Fraction of Cycle)\n\tAP - Area in Pixels (#Pixels)\n\t CHA - Convex Hull Area (r.u.)\n\tCHV - Convex Hull Volume (r.u.)\n\tTD - Time Dispersion (r.u.)\n\tFD - Frequency Dispersion (Hz)\n\n' + 'Note ---> [Some indexes may not be present in the graphical representation]' + '\n\n')
    plt.axis('off')

    pp.savefig(dataFrame.fig)
    pp.savefig(figText)

    plt.close(dataFrame.fig)
    plt.close(figText)


# Radar Plot Generation Function.
def PlotRadar(data, sbjOrder):
    # Variable Definition.
    tempData = []

    # Figure Parameters (labels of axes).
    labelsMscName = data[0][0]
    colors = ['b', 'r', 'g', 'm', 'y']

    # Definition of Radar format and number of vertices.
    nbrMuscles = 5
    theta = radar_factory(nbrMuscles, frame='polygon')

    # Generation of a pdf File.
    pp = PdfPages('Signals' + '/' + 'RadarPlotMeanPower.pdf')

    # In each page will be ploted the Mean Power Evolution of 5 Subjects.
    nbrSets = np.ceil(len(data) / 5)

    for set in range(0, int(nbrSets)):
        remainingSbj = len(data) - 5 * set
        # Figure and Axis Generation.
        if remainingSbj >= 5:
            fig, axes = plt.subplots(nrows=5, ncols=6, subplot_kw=dict(projection='radar'))
        else:
            fig, axes = plt.subplots(nrows=remainingSbj, ncols=6, subplot_kw=dict(projection='radar'))

        fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

        # Fill Phase of the Subplots in the Axis Grid.
        # Range Definition.
        if 5 * set + 5 < len(data):
            rng = range(5 * set, 5 * set + 5)
        else:
            rng = range(5 * set, 5 * set + remainingSbj)

        for subject in rng:
            # Title of each column (Number of the quintile part of the acquisition).
            axes[0][1].set_title('1st Quintile', weight='bold', size='medium', position=(0.5, 1.1),
                                 horizontalalignment='center', verticalalignment='center')
            axes[0][2].set_title('2nd Quintile', weight='bold', size='medium', position=(0.5, 1.1),
                                 horizontalalignment='center', verticalalignment='center')
            axes[0][3].set_title('3rd Quintile', weight='bold', size='medium', position=(0.5, 1.1),
                                 horizontalalignment='center', verticalalignment='center')
            axes[0][4].set_title('4th Quintile', weight='bold', size='medium', position=(0.5, 1.1),
                                 horizontalalignment='center', verticalalignment='center')
            axes[0][5].set_title('5th Quintile', weight='bold', size='medium', position=(0.5, 1.1),
                                 horizontalalignment='center', verticalalignment='center')

            # Determination of the maximum value registered for Mean Power (With the purpose of scale normalization).
            for instant in range(0, 10, 2):
                for muscle in range(0, 5):
                    if subject < len(data):
                        tempData.append(np.mean((data[subject][muscle + 1][1][instant], data[subject][muscle + 1][1][instant + 1])))


            maxMP = np.max(tempData)
            tempData = []

            # Plot of the Results.
            for instant in range(0, 10, 2):
                for muscle in range(0, 5):
                    # We need to congregate in one array the data of Mean Power of the five muscles at the instant t.
                    tempData.append(
                        np.mean((data[subject][muscle + 1][1][instant], data[subject][muscle + 1][1][instant + 1])))

                tempData = tempData / maxMP

                # Plot of Data into the Radar Strucutre.
                axes[subject - (5 * set)][int(instant / 2) + 1].plot(theta, tempData, color=colors[subject - set * 5])
                axes[subject - (5 * set)][int(instant / 2) + 1].fill(theta, tempData,
                                                                     facecolor=colors[subject - set * 5], alpha=0.25)
                axes[subject - (5 * set)][int(instant / 2) + 1].set_varlabels(labelsMscName)
                axes[subject - (5 * set)][int(instant / 2) + 1].set_ylim(0, 1)
                axes[subject - (5 * set)][int(instant / 2) + 1].set_rgrids([0.20, 0.60, 1.0, 1.25],
                                                                           labels=[0.20, 0.60, 1.0], angle=45,
                                                                           fontsize='5')
                axes[subject - (5 * set)][0].axis('off')
                axes[subject - (5 * set)][0].text(0, 0, str(sbjOrder[subject]), rotation=90)

                # Reboot of arrays for the next iteration.
                tempData = []

        # Transposition of the Figure to a new Pdf Page.
        pp.savefig(fig)
        # Memory Release.
        plt.close(fig)

        # Informational Pages of Pdf File.
        figText = plt.figure()
        strAux = 'Subject Order' + '\n\n'
        for i in rng:
            strAux = strAux + '----- Row ' + str(i) + ' -----' + '\n' + '\t' + str(sbjOrder[i]) + '\n'

        plt.text(0, 0.5, strAux)
        plt.axis('off')

        # Figure Storage.
        pp.savefig(figText)
        # Memory Release.
        plt.close(figText)

    # Common Page.
    figText1 = plt.figure()
    plt.text(0, 0.5,
             'Legend' + '\n\n' + '----- Muscles (Msc) -----' + '\n' + '\tRF - Rectus Femoris\n\tVL - Vastus Lateralis\n\tVM - Vastus Medialis\n\tST - Semitendinosus\n\tBF - Biceps Femoris\n\n' + '----- Parameters (PName) ----- ' + '\n\tMP - Mean Power (r.u.)\n\n' + 'Note ---> [Some indexes may not be present in the graphical representation]' + '\n\n')
    plt.axis('off')

    # Figure Storage.
    pp.savefig(figText1)
    # Memory Release.
    plt.close(figText1)

    pp.close()
    plt.show()

    # Provisional Version of 8th of July of 2017 :) *-* (:
