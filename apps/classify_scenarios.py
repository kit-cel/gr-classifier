#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Classify Scenarios
# Generated: Wed Mar  8 07:34:39 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import classifier
import fbmc
import numpy as np
import scenario_classification_f
import sip
import sys
import threading
import time


class classify_scenarios(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Classify Scenarios")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Classify Scenarios")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "classify_scenarios")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.mod_order = mod_order = 2
        self.samp_rate = samp_rate = int(1e7)
        self.packetlen_base = packetlen_base = 256 * 12 * mod_order
        self.tap_factor = tap_factor = 1.8
        self.equiripple_118m_132m_500m_70dB = equiripple_118m_132m_500m_70dB = np.array([0.00053615,0.0010861,0.0017619,0.0022328,0.0021874,0.0014325,2.9264e-05,-0.0016642,-0.0030955,-0.0037401,-0.0033511,-0.0021099,-0.00058037,0.00053299,0.00072394,-5.1054e-05,-0.001331,-0.0023721,-0.0025379,-0.0016543,-0.00013335,0.0012239,0.0016569,0.00088322,-0.00070579,-0.0022217,-0.0027558,-0.0019039,-4.0075e-05,0.0018411,0.0026556,0.0018563,-0.0002048,-0.0024103,-0.0034702,-0.002663,-0.00030483,0.0023525,0.0037801,0.0030472,0.00041551,-0.0027175,-0.0045473,-0.0038893,-0.00092515,0.0027923,0.0051404,0.0046284,0.0013257,-0.0030504,-0.0060086,-0.0056856,-0.0019949,0.0031728,0.0068949,0.0068505,0.0027389,-0.003367,-0.0080334,-0.0083676,-0.0037726,0.0034906,0.0093696,0.010241,0.0050885,-0.0036372,-0.011116,-0.012756,-0.0069285,0.0037421,0.013449,0.016255,0.0095811,-0.0038442,-0.016891,-0.021618,-0.013821,0.0039147,0.022614,0.031023,0.021695,-0.0039703,-0.034568,-0.052565,-0.041904,0.0040005,0.077685,0.15899,0.22218,0.24598,0.22218,0.15899,0.077685,0.0040005,-0.041904,-0.052565,-0.034568,-0.0039703,0.021695,0.031023,0.022614,0.0039147,-0.013821,-0.021618,-0.016891,-0.0038442,0.0095811,0.016255,0.013449,0.0037421,-0.0069285,-0.012756,-0.011116,-0.0036372,0.0050885,0.010241,0.0093696,0.0034906,-0.0037726,-0.0083676,-0.0080334,-0.003367,0.0027389,0.0068505,0.0068949,0.0031728,-0.0019949,-0.0056856,-0.0060086,-0.0030504,0.0013257,0.0046284,0.0051404,0.0027923,-0.00092515,-0.0038893,-0.0045473,-0.0027175,0.00041551,0.0030472,0.0037801,0.0023525,-0.00030483,-0.002663,-0.0034702,-0.0024103,-0.0002048,0.0018563,0.0026556,0.0018411,-4.0075e-05,-0.0019039,-0.0027558,-0.0022217,-0.00070579,0.00088322,0.0016569,0.0012239,-0.00013335,-0.0016543,-0.0025379,-0.0023721,-0.001331,-5.1054e-05,0.00072394,0.00053299,-0.00058037,-0.0021099,-0.0033511,-0.0037401,-0.0030955,-0.0016642,2.9264e-05,0.0014325,0.0021874,0.0022328,0.0017619,0.0010861,0.00053615])
        self.cfg = cfg = fbmc.fbmc_config(channel_map=([1,]*128), num_payload_bits=packetlen_base, num_overlap_sym=4, samp_rate=int(samp_rate)/4)
        self.taps = taps = equiripple_118m_132m_500m_70dB * tap_factor
        self.phydyas_taps_time = phydyas_taps_time = np.array(cfg.phydyas_impulse_taps(cfg.num_total_subcarriers(), cfg.num_overlap_sym()))
        self.nguard_bins = nguard_bins = 8
        self.nchan = nchan = 4
        self.sync = sync = fbmc.sync_config(taps=(phydyas_taps_time[1:]/np.sqrt(phydyas_taps_time.dot(phydyas_taps_time))), N=cfg.num_total_subcarriers(), overlap=4, L=cfg.num_total_subcarriers()-1, pilot_A=2, pilot_timestep=4, pilot_carriers=(range(8, 118, 4) + [119]), subbands=nchan, bits=packetlen_base, pos=4, u=1, q=4, A=2, fft_len=2**13, guard=nguard_bins, order=4)
        self.tau = tau = None
        self.su_throughput = su_throughput = 0
        self.su_providedthroughput = su_providedthroughput = 0
        self.su_frame_len_low_rate = su_frame_len_low_rate = sync.get_frame_samps(True)
        self.scenario = scenario = -1
        self.pu_throughput = pu_throughput = 0
        self.pu_providedthroughput = pu_providedthroughput = 0
        self.ed_noisefloor = ed_noisefloor = 0
        self.channel_occupation = channel_occupation = None
        self.variable_qtgui_label_2_0_1 = variable_qtgui_label_2_0_1 = su_throughput
        self.variable_qtgui_label_2_0_0_0 = variable_qtgui_label_2_0_0_0 = su_providedthroughput
        self.variable_qtgui_label_2_0_0 = variable_qtgui_label_2_0_0 = pu_providedthroughput
        self.variable_qtgui_label_2_0 = variable_qtgui_label_2_0 = pu_throughput
        self.variable_qtgui_label_2 = variable_qtgui_label_2 = ed_noisefloor
        self.variable_qtgui_label_0_1 = variable_qtgui_label_0_1 = channel_occupation
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = scenario
        self.tx_gain = tx_gain = .85
        self.threshold_delta = threshold_delta = 15
        self.tau_label = tau_label = tau
        self.su_frame_len = su_frame_len = (su_frame_len_low_rate + len(taps))* 4
        self.rx_gain = rx_gain = .5
        self.pu_frame_len = pu_frame_len = 80*5*9
        self.num_interp_taps = num_interp_taps = len(taps)
        self.nsamp_zeropadding = nsamp_zeropadding = 2320
        self.nfft = nfft = 512
        self.firdes_taps = firdes_taps = np.array([0.003524782368913293, 0.002520402194932103, -3.532667373554307e-17, -0.0025783423334360123, -0.0036887258756905794, -0.0026390093844383955, -3.7046301165340785e-18, 0.0027025998570024967, 0.003868663916364312, 0.0027693307492882013, -9.712380039780164e-18, -0.0028394402470439672, -0.004067056812345982, -0.0029131921473890543, 2.454170927498071e-17, 0.0029908770229667425, 0.004286897834390402, 0.0030728192068636417, -9.712380039780164e-18, -0.0031593774911016226, -0.004531863145530224, -0.0032509532757103443, -6.861573196148834e-18, 0.0033479968551546335, 0.004806521814316511, 0.003451012307778001, -9.712380039780164e-18, -0.0035605679731816053, -0.005116619635373354, -0.0036773078609257936, 2.849619674016194e-17, 0.003801962360739708, 0.005469490308314562, 0.003935364540666342, -9.712380039780164e-18, -0.004078468773514032, -0.0058746375143527985, -0.004232373554259539, -1.196125168755972e-17, 0.004398348741233349, 0.006344608962535858, 0.004577873274683952, -9.712380039780164e-18, -0.004772676154971123, -0.0068963137455284595, -0.004984795115888119, 3.532667373554307e-17, 0.005216646008193493, 0.00755310570821166, 0.005471116863191128, -9.712380039780164e-18, -0.0057516866363584995, -0.00834816973656416, -0.00606258912011981, 9.712380039780164e-18, 0.006409022491425276, 0.009330307133495808, 0.006797448266297579, -9.712380039780164e-18, -0.007235993165522814, -0.010574348270893097, -0.007735027000308037, 9.712380039780164e-18, 0.008307991549372673, 0.012201170437037945, 0.008972631767392159, -9.712380039780164e-18, -0.00975286029279232, -0.014419564977288246, -0.010681704618036747, 9.712380039780164e-18, 0.011806094087660313, 0.017623912543058395, 0.013195047155022621, -9.712380039780164e-18, -0.01495438627898693, -0.022659316658973694, -0.017255060374736786, 9.712380039780164e-18, 0.020392345264554024, 0.03172304481267929, 0.02492397651076317, -9.712380039780164e-18, -0.03204511106014252, -0.052871737629175186, -0.04486315697431564, 9.712380039780164e-18, 0.0747719332575798, 0.15861520171165466, 0.22431577742099762, 0.24915219843387604, 0.22431577742099762, 0.15861520171165466, 0.0747719332575798, 9.712380039780164e-18, -0.04486315697431564, -0.052871737629175186, -0.03204511106014252, -9.712380039780164e-18, 0.02492397651076317, 0.03172304481267929, 0.020392345264554024, 9.712380039780164e-18, -0.017255060374736786, -0.022659316658973694, -0.01495438627898693, -9.712380039780164e-18, 0.013195047155022621, 0.017623912543058395, 0.011806094087660313, 9.712380039780164e-18, -0.010681704618036747, -0.014419564977288246, -0.00975286029279232, -9.712380039780164e-18, 0.008972631767392159, 0.012201170437037945, 0.008307991549372673, 9.712380039780164e-18, -0.007735027000308037, -0.010574348270893097, -0.007235993165522814, -9.712380039780164e-18, 0.006797448266297579, 0.009330307133495808, 0.006409022491425276, 9.712380039780164e-18, -0.00606258912011981, -0.00834816973656416, -0.0057516866363584995, -9.712380039780164e-18, 0.005471116863191128, 0.00755310570821166, 0.005216646008193493, 3.532667373554307e-17, -0.004984795115888119, -0.0068963137455284595, -0.004772676154971123, -9.712380039780164e-18, 0.004577873274683952, 0.006344608962535858, 0.004398348741233349, -1.196125168755972e-17, -0.004232373554259539, -0.0058746375143527985, -0.004078468773514032, -9.712380039780164e-18, 0.003935364540666342, 0.005469490308314562, 0.003801962360739708, 2.849619674016194e-17, -0.0036773078609257936, -0.005116619635373354, -0.0035605679731816053, -9.712380039780164e-18, 0.003451012307778001, 0.004806521814316511, 0.0033479968551546335, -6.861573196148834e-18, -0.0032509532757103443, -0.004531863145530224, -0.0031593774911016226, -9.712380039780164e-18, 0.0030728192068636417, 0.004286897834390402, 0.0029908770229667425, 2.454170927498071e-17, -0.0029131921473890543, -0.004067056812345982, -0.0028394402470439672, -9.712380039780164e-18, 0.0027693307492882013, 0.003868663916364312, 0.0027025998570024967, -3.7046301165340785e-18, -0.0026390093844383955, -0.0036887258756905794, -0.0025783423334360123, -3.532667373554307e-17, 0.002520402194932103])*1.0
        self.equiripple_200m_40dB = equiripple_200m_40dB = np.array([0.0017203,-0.004888,-0.0024169,-0.0013149,-0.00035127,0.00055231,0.0011133,0.0010843,0.00046479,-0.00045283,-0.0012066,-0.0013874,-0.00085657,0.00016435,0.0011789,0.001658,0.0013103,0.00025461,-0.0010137,-0.0018499,-0.0017879,-0.00079281,0.0006859,0.0019168,0.0022418,0.0014288,-0.00018291,-0.0018133,-0.0026201,-0.0021266,-0.00049929,0.0015001,0.0028602,0.0028359,0.001342,-0.00094639,-0.0029033,-0.0034896,-0.0023145,0.00014095,0.0026852,0.0040158,0.0033609,0.00091993,-0.0021549,-0.0043271,-0.004412,-0.0022211,0.0012706,0.0043435,0.0053822,0.0037083,-3.0831e-07,-0.0039704,-0.0061663,-0.0053269,-0.0016675,0.0031223,0.0066475,0.0069883,0.0037295,-0.0017154,-0.0066927,-0.0085864,-0.0061668,-0.00033908,0.006154,0.0099952,0.0089582,0.0031476,-0.0048458,-0.011063,-0.012088,-0.0068683,0.0025123,0.011591,0.015577,0.011788,0.0012693,-0.011299,-0.019564,-0.018543,-0.0073709,0.0096666,0.024518,0.028832,0.018109,-0.0053388,-0.032129,-0.048718,-0.042578,-0.0076338,0.052308,0.12374,0.18744,0.22492,0.22492,0.18744,0.12374,0.052308,-0.0076338,-0.042578,-0.048718,-0.032129,-0.0053388,0.018109,0.028832,0.024518,0.0096666,-0.0073709,-0.018543,-0.019564,-0.011299,0.0012693,0.011788,0.015577,0.011591,0.0025123,-0.0068683,-0.012088,-0.011063,-0.0048458,0.0031476,0.0089582,0.0099952,0.006154,-0.00033908,-0.0061668,-0.0085864,-0.0066927,-0.0017154,0.0037295,0.0069883,0.0066475,0.0031223,-0.0016675,-0.0053269,-0.0061663,-0.0039704,-3.0831e-07,0.0037083,0.0053822,0.0043435,0.0012706,-0.0022211,-0.004412,-0.0043271,-0.0021549,0.00091993,0.0033609,0.0040158,0.0026852,0.00014095,-0.0023145,-0.0034896,-0.0029033,-0.00094639,0.001342,0.0028359,0.0028602,0.0015001,-0.00049929,-0.0021266,-0.0026201,-0.0018133,-0.00018291,0.0014288,0.0022418,0.0019168,0.0006859,-0.00079281,-0.0017879,-0.0018499,-0.0010137,0.00025461,0.0013103,0.001658,0.0011789,0.00016435,-0.00085657,-0.0013874,-0.0012066,-0.00045283,0.00046479,0.0010843,0.0011133,0.00055231,-0.00035127,-0.0013149,-0.0024169,-0.004888,0.0017203])
        self.equiripple_120m_130m_500m_50dB = equiripple_120m_130m_500m_50dB = np.array([-0.0014851,0.00086212,0.0020139,0.003371,0.0042945,0.004268,0.0031519,0.0012954,-0.00058469,-0.0017292,-0.0017127,-0.00067235,0.00074655,0.0017187,0.0016794,0.00063719,-0.00081917,-0.0018427,-0.0018094,-0.0006915,0.0008993,0.0020404,0.0020269,0.00080008,-0.00098081,-0.0022875,-0.0023114,-0.00095804,0.0010524,0.0025628,0.0026417,0.0011508,-0.0011227,-0.0028746,-0.0030269,-0.0013845,0.0011891,0.0032208,0.0034656,0.001662,-0.001252,-0.0036075,-0.0039676,-0.0019853,0.001312,0.004044,0.0045452,0.0023677,-0.0013677,-0.0045376,-0.0052119,-0.0028195,0.0014214,0.005105,0.0059931,0.0033593,-0.0014706,-0.0057662,-0.0069199,-0.0040127,0.001516,0.0065517,0.0080409,0.0048166,-0.0015575,-0.0075094,-0.0094308,-0.005832,0.0015943,0.008713,0.01121,0.0071543,-0.0016267,-0.010291,-0.013587,-0.0089568,0.0016543,0.012479,0.016957,0.011572,-0.0016769,-0.015764,-0.022168,-0.015745,0.0016946,0.021346,0.031424,0.023544,-0.0017072,-0.033161,-0.052806,-0.04366,0.001715,0.076153,0.15907,0.22384,0.24828,0.22384,0.15907,0.076153,0.001715,-0.04366,-0.052806,-0.033161,-0.0017072,0.023544,0.031424,0.021346,0.0016946,-0.015745,-0.022168,-0.015764,-0.0016769,0.011572,0.016957,0.012479,0.0016543,-0.0089568,-0.013587,-0.010291,-0.0016267,0.0071543,0.01121,0.008713,0.0015943,-0.005832,-0.0094308,-0.0075094,-0.0015575,0.0048166,0.0080409,0.0065517,0.001516,-0.0040127,-0.0069199,-0.0057662,-0.0014706,0.0033593,0.0059931,0.005105,0.0014214,-0.0028195,-0.0052119,-0.0045376,-0.0013677,0.0023677,0.0045452,0.004044,0.001312,-0.0019853,-0.0039676,-0.0036075,-0.001252,0.001662,0.0034656,0.0032208,0.0011891,-0.0013845,-0.0030269,-0.0028746,-0.0011227,0.0011508,0.0026417,0.0025628,0.0010524,-0.00095804,-0.0023114,-0.0022875,-0.00098081,0.00080008,0.0020269,0.0020404,0.0008993,-0.0006915,-0.0018094,-0.0018427,-0.00081917,0.00063719,0.0016794,0.0017187,0.00074655,-0.00067235,-0.0017127,-0.0017292,-0.00058469,0.0012954,0.0031519,0.004268,0.0042945,0.003371,0.0020139,0.00086212,-0.0014851])
        self.enable_tx = enable_tx = False
        self.always_send = always_send = False
        self.aggro_mode = aggro_mode = False
        self.T_disp_ms = T_disp_ms = 100

        ##################################################
        # Blocks
        ##################################################
        self._threshold_delta_range = Range(0, 30, 1, 15, 200)
        self._threshold_delta_win = RangeWidget(self._threshold_delta_range, self.set_threshold_delta, 'threshold_delta', "counter", float)
        self.top_grid_layout.addWidget(self._threshold_delta_win, 1, 1, 1, 1)
        self._tx_gain_range = Range(0, 1, .01, .85, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, 'TX gain (normalized)', "counter", float)
        self.top_grid_layout.addWidget(self._tx_gain_win, 0, 1, 1, 1)
        self.scenario_classification_f = scenario_classification_f.blk(tconst=2, tau1=5, tau2=10, lambda1=20, lambda2=10, lambda3=5)
        self._rx_gain_range = Range(0, 1, .05, .5, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX gain (normalized)', "counter", float)
        self.top_grid_layout.addWidget(self._rx_gain_win, 0, 0, 1, 1)
        self.classifier_packet_source_0 = classifier.packet_source(3, "packet_len","192.168.52.1",5003,64,1)
        self.classifier_energy_detection_vcf_0 = classifier.energy_detection_vcf(nfft, threshold_delta)
        self._variable_qtgui_label_2_0_1_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._variable_qtgui_label_2_0_1_formatter = None
        else:
          self._variable_qtgui_label_2_0_1_formatter = lambda x: x
        
        self._variable_qtgui_label_2_0_1_tool_bar.addWidget(Qt.QLabel('SU throughput'+": "))
        self._variable_qtgui_label_2_0_1_label = Qt.QLabel(str(self._variable_qtgui_label_2_0_1_formatter(self.variable_qtgui_label_2_0_1)))
        self._variable_qtgui_label_2_0_1_tool_bar.addWidget(self._variable_qtgui_label_2_0_1_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_2_0_1_tool_bar, 0, 3, 1, 1, )
          
        self._variable_qtgui_label_2_0_0_0_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._variable_qtgui_label_2_0_0_0_formatter = None
        else:
          self._variable_qtgui_label_2_0_0_0_formatter = lambda x: x
        
        self._variable_qtgui_label_2_0_0_0_tool_bar.addWidget(Qt.QLabel('SU provided throughput'+": "))
        self._variable_qtgui_label_2_0_0_0_label = Qt.QLabel(str(self._variable_qtgui_label_2_0_0_0_formatter(self.variable_qtgui_label_2_0_0_0)))
        self._variable_qtgui_label_2_0_0_0_tool_bar.addWidget(self._variable_qtgui_label_2_0_0_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_2_0_0_0_tool_bar, 1, 3, 1, 1)
          
        self._variable_qtgui_label_2_0_0_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._variable_qtgui_label_2_0_0_formatter = None
        else:
          self._variable_qtgui_label_2_0_0_formatter = lambda x: x
        
        self._variable_qtgui_label_2_0_0_tool_bar.addWidget(Qt.QLabel('PU provided throughput'+": "))
        self._variable_qtgui_label_2_0_0_label = Qt.QLabel(str(self._variable_qtgui_label_2_0_0_formatter(self.variable_qtgui_label_2_0_0)))
        self._variable_qtgui_label_2_0_0_tool_bar.addWidget(self._variable_qtgui_label_2_0_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_2_0_0_tool_bar, 1, 2, 1, 1)
          
        self._variable_qtgui_label_2_0_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._variable_qtgui_label_2_0_formatter = None
        else:
          self._variable_qtgui_label_2_0_formatter = lambda x: x
        
        self._variable_qtgui_label_2_0_tool_bar.addWidget(Qt.QLabel('PU throughput'+": "))
        self._variable_qtgui_label_2_0_label = Qt.QLabel(str(self._variable_qtgui_label_2_0_formatter(self.variable_qtgui_label_2_0)))
        self._variable_qtgui_label_2_0_tool_bar.addWidget(self._variable_qtgui_label_2_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_2_0_tool_bar, 0, 2, 1, 1)
          
        self._variable_qtgui_label_2_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._variable_qtgui_label_2_formatter = None
        else:
          self._variable_qtgui_label_2_formatter = lambda x: x
        
        self._variable_qtgui_label_2_tool_bar.addWidget(Qt.QLabel('Noise floor [dB]'+": "))
        self._variable_qtgui_label_2_label = Qt.QLabel(str(self._variable_qtgui_label_2_formatter(self.variable_qtgui_label_2)))
        self._variable_qtgui_label_2_tool_bar.addWidget(self._variable_qtgui_label_2_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_2_tool_bar, 1, 0, 1, 1)
          
        self._variable_qtgui_label_0_1_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._variable_qtgui_label_0_1_formatter = None
        else:
          self._variable_qtgui_label_0_1_formatter = lambda x: x
        
        self._variable_qtgui_label_0_1_tool_bar.addWidget(Qt.QLabel('Channel occupation'+": "))
        self._variable_qtgui_label_0_1_label = Qt.QLabel(str(self._variable_qtgui_label_0_1_formatter(self.variable_qtgui_label_0_1)))
        self._variable_qtgui_label_0_1_tool_bar.addWidget(self._variable_qtgui_label_0_1_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_1_tool_bar, 6, 3, 1, 1)
          
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._variable_qtgui_label_0_formatter = None
        else:
          self._variable_qtgui_label_0_formatter = lambda x: x
        
        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel('Scenario'+": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_tool_bar, 6, 1, 1, 1)
          
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
        	",".join(('type=b200', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0_0.set_clock_source('gpsdo', 0)
        self.uhd_usrp_source_0_0.set_time_source('gpsdo', 0)
        self.uhd_usrp_source_0_0.set_subdev_spec('A:B', 0)
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_0.set_center_freq(uhd.tune_request(3.195e9, samp_rate), 0)
        self.uhd_usrp_source_0_0.set_normalized_gain(rx_gain, 0)
        self.uhd_usrp_source_0_0.set_antenna('RX2', 0)
        self.uhd_usrp_sink_1_0 = uhd.usrp_sink(
        	",".join(('type=b200', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_1_0.set_clock_source('gpsdo', 0)
        self.uhd_usrp_sink_1_0.set_time_source('gpsdo', 0)
        self.uhd_usrp_sink_1_0.set_subdev_spec('A:A', 0)
        self.uhd_usrp_sink_1_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_1_0.set_center_freq(uhd.tune_request(3.195e9, samp_rate), 0)
        self.uhd_usrp_sink_1_0.set_normalized_gain(tx_gain, 0)
        self.uhd_usrp_sink_1_0.set_antenna('TX/RX', 0)
        self._tau_label_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._tau_label_formatter = None
        else:
          self._tau_label_formatter = lambda x: x
        
        self._tau_label_tool_bar.addWidget(Qt.QLabel('Average Tau'+": "))
        self._tau_label_label = Qt.QLabel(str(self._tau_label_formatter(self.tau_label)))
        self._tau_label_tool_bar.addWidget(self._tau_label_label)
        self.top_grid_layout.addWidget(self._tau_label_tool_bar, 6, 2, 1, 1)
          
        
        def _tau_probe():
            while True:
                val = self.scenario_classification_f.get_tau()
                try:
                    self.set_tau(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _tau_thread = threading.Thread(target=_tau_probe)
        _tau_thread.daemon = True
        _tau_thread.start()
            
        self._tap_factor_range = Range(0.5, 2.0, 0.1, 1.8, 200)
        self._tap_factor_win = RangeWidget(self._tap_factor_range, self.set_tap_factor, 'Scale Tx Ampl.', "counter_slider", float)
        self.top_layout.addWidget(self._tap_factor_win)
        
        def _su_throughput_probe():
            while True:
                val = self.classifier_packet_source_0.get_throughput()
                try:
                    self.set_su_throughput(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _su_throughput_thread = threading.Thread(target=_su_throughput_probe)
        _su_throughput_thread.daemon = True
        _su_throughput_thread.start()
            
        
        def _su_providedthroughput_probe():
            while True:
                val = self.classifier_packet_source_0.get_providedthroughput()
                try:
                    self.set_su_providedthroughput(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _su_providedthroughput_thread = threading.Thread(target=_su_providedthroughput_probe)
        _su_providedthroughput_thread.daemon = True
        _su_providedthroughput_thread.start()
            
        
        def _scenario_probe():
            while True:
                val = self.scenario_classification_f.get_scenario()
                try:
                    self.set_scenario(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _scenario_thread = threading.Thread(target=_scenario_probe)
        _scenario_thread.daemon = True
        _scenario_thread.start()
            
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	128, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"Input signal", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.05)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)
        
        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)
        
        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 2, 0, 2, 2)
        self.qtgui_time_sink_x_3 = qtgui.time_sink_c(
        	su_frame_len + nsamp_zeropadding, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_3.set_update_time(0.10)
        self.qtgui_time_sink_x_3.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_3.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_3.enable_tags(-1, True)
        self.qtgui_time_sink_x_3.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_3.enable_autoscale(False)
        self.qtgui_time_sink_x_3.enable_grid(False)
        self.qtgui_time_sink_x_3.enable_axis_labels(True)
        self.qtgui_time_sink_x_3.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_3.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2*1):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_3.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_3.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_3.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_3.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_3.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_3.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_3.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_3.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_3_win = sip.wrapinstance(self.qtgui_time_sink_x_3.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_3_win)
        self.qtgui_time_sink_x_0_0_0_0 = qtgui.time_sink_f(
        	5000, #size
        	samp_rate // nfft, #samp_rate
        	"Averaged power per subchannel", #name
        	4 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0.set_y_axis(-50, 20)
        
        self.qtgui_time_sink_x_0_0_0_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0_0_0_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(4):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_0_win, 4, 0, 2, 2)
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_f(
        	5000, #size
        	1 + 0 * samp_rate/nfft, #samp_rate
        	"Binary subchannel occupation", #name
        	4 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(-1, 2)
        
        self.qtgui_time_sink_x_0_0_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.5, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0_0_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(4):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_win, 4, 2, 2, 2)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2, 2, 2, 2)
        
        def _pu_throughput_probe():
            while True:
                val = self.classifier_packet_source_0.get_PU_throughput()
                try:
                    self.set_pu_throughput(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _pu_throughput_thread = threading.Thread(target=_pu_throughput_probe)
        _pu_throughput_thread.daemon = True
        _pu_throughput_thread.start()
            
        
        def _pu_providedthroughput_probe():
            while True:
                val = self.classifier_packet_source_0.get_PU_providedthroughput()
                try:
                    self.set_pu_providedthroughput(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _pu_providedthroughput_thread = threading.Thread(target=_pu_providedthroughput_probe)
        _pu_providedthroughput_thread.daemon = True
        _pu_providedthroughput_thread.start()
            
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(nchan, (taps))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        (self.interp_fir_filter_xxx_0).set_min_output_buffer(227820)
        self.fft_vxx_0 = fft.fft_vcc(nfft, True, (window.blackmanharris(nfft)), True, 1)
        self.fbmc_tx_sdft_vcc_0 = fbmc.tx_sdft_vcc((phydyas_taps_time/np.sqrt(phydyas_taps_time.dot(phydyas_taps_time))/10), cfg.num_total_subcarriers())
        self.fbmc_subchannel_frame_generator_bvc_0 = fbmc.subchannel_frame_generator_bvc(cfg.num_total_subcarriers(), nguard_bins, cfg.num_payload_bits(), cfg.num_overlap_sym(), (sync.get_preamble_symbols()), sync.get_pilot_amplitude(), sync.get_pilot_timestep(), (sync.get_pilot_carriers()), sync.get_syms_frame(), True, sync.get_bps())
        _enable_tx_check_box = Qt.QCheckBox('enable_tx')
        self._enable_tx_choices = {True: True, False: False}
        self._enable_tx_choices_inv = dict((v,k) for k,v in self._enable_tx_choices.iteritems())
        self._enable_tx_callback = lambda i: Qt.QMetaObject.invokeMethod(_enable_tx_check_box, "setChecked", Qt.Q_ARG("bool", self._enable_tx_choices_inv[i]))
        self._enable_tx_callback(self.enable_tx)
        _enable_tx_check_box.stateChanged.connect(lambda i: self.set_enable_tx(self._enable_tx_choices[bool(i)]))
        self.top_layout.addWidget(_enable_tx_check_box)
        
        def _ed_noisefloor_probe():
            while True:
                val = self.classifier_energy_detection_vcf_0.get_noisefloor_db()
                try:
                    self.set_ed_noisefloor(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _ed_noisefloor_thread = threading.Thread(target=_ed_noisefloor_probe)
        _ed_noisefloor_thread.daemon = True
        _ed_noisefloor_thread.start()
            
        self.classifier_frame_detection_f_0 = classifier.frame_detection_f((su_frame_len - nchan * len(taps) - 2 * nchan * cfg.num_total_subcarriers())/nfft - 2, 5, 5)
        self.classifier_feature_extraction_f_0 = classifier.feature_extraction_f(samp_rate / nfft, 50, pu_frame_len / nfft - 1, 5)
        self.classifier_cognitive_allocator_0 = classifier.cognitive_allocator(su_frame_len, pu_frame_len, samp_rate / nfft, samp_rate , nsamp_zeropadding, 1.5 + float(su_frame_len + nsamp_zeropadding) / samp_rate * 1000, False, 50)
        
        def _channel_occupation_probe():
            while True:
                val = self.scenario_classification_f.get_chan_occupied()
                try:
                    self.set_channel_occupation(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _channel_occupation_thread = threading.Thread(target=_channel_occupation_probe)
        _channel_occupation_thread.daemon = True
        _channel_occupation_thread.start()
            
        self.blocks_vector_insert_x_1_0 = blocks.vector_insert_c(([0,] * len(taps)), su_frame_len_low_rate + len(taps), len(taps))
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, nfft)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(sync.get_bps(), gr.GR_LSB_FIRST)
        _always_send_check_box = Qt.QCheckBox("always_send")
        self._always_send_choices = {True: True, False: False}
        self._always_send_choices_inv = dict((v,k) for k,v in self._always_send_choices.iteritems())
        self._always_send_callback = lambda i: Qt.QMetaObject.invokeMethod(_always_send_check_box, "setChecked", Qt.Q_ARG("bool", self._always_send_choices_inv[i]))
        self._always_send_callback(self.always_send)
        _always_send_check_box.stateChanged.connect(lambda i: self.set_always_send(self._always_send_choices[bool(i)]))
        self.top_grid_layout.addWidget(_always_send_check_box, 6, 0, 1, 1)
        _aggro_mode_check_box = Qt.QCheckBox("aggro_mode")
        self._aggro_mode_choices = {True: True, False: False}
        self._aggro_mode_choices_inv = dict((v,k) for k,v in self._aggro_mode_choices.iteritems())
        self._aggro_mode_callback = lambda i: Qt.QMetaObject.invokeMethod(_aggro_mode_check_box, "setChecked", Qt.Q_ARG("bool", self._aggro_mode_choices_inv[i]))
        self._aggro_mode_callback(self.aggro_mode)
        _aggro_mode_check_box.stateChanged.connect(lambda i: self.set_aggro_mode(self._aggro_mode_choices[bool(i)]))
        self.top_layout.addWidget(_aggro_mode_check_box)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.classifier_frame_detection_f_0, 'pu_frame_start'), (self.classifier_cognitive_allocator_0, 'pu_frame_start'))    
        self.msg_connect((self.classifier_packet_source_0, 'enable_tx'), (self.classifier_cognitive_allocator_0, 'enable_tx'))    
        self.msg_connect((self.scenario_classification_f, 'scenario'), (self.classifier_cognitive_allocator_0, 'scenario'))    
        self.msg_connect((self.scenario_classification_f, 'scenario'), (self.classifier_packet_source_0, 'scenario'))    
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.fbmc_subchannel_frame_generator_bvc_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.blocks_vector_insert_x_1_0, 0), (self.interp_fir_filter_xxx_0, 0))    
        self.connect((self.classifier_cognitive_allocator_0, 0), (self.qtgui_time_sink_x_3, 0))    
        self.connect((self.classifier_cognitive_allocator_0, 0), (self.uhd_usrp_sink_1_0, 0))    
        self.connect((self.classifier_energy_detection_vcf_0, 4), (self.classifier_frame_detection_f_0, 0))    
        self.connect((self.classifier_energy_detection_vcf_0, 7), (self.classifier_frame_detection_f_0, 3))    
        self.connect((self.classifier_energy_detection_vcf_0, 5), (self.classifier_frame_detection_f_0, 1))    
        self.connect((self.classifier_energy_detection_vcf_0, 6), (self.classifier_frame_detection_f_0, 2))    
        self.connect((self.classifier_energy_detection_vcf_0, 4), (self.qtgui_time_sink_x_0_0_0, 0))    
        self.connect((self.classifier_energy_detection_vcf_0, 5), (self.qtgui_time_sink_x_0_0_0, 1))    
        self.connect((self.classifier_energy_detection_vcf_0, 6), (self.qtgui_time_sink_x_0_0_0, 2))    
        self.connect((self.classifier_energy_detection_vcf_0, 7), (self.qtgui_time_sink_x_0_0_0, 3))    
        self.connect((self.classifier_energy_detection_vcf_0, 0), (self.qtgui_time_sink_x_0_0_0_0, 0))    
        self.connect((self.classifier_energy_detection_vcf_0, 1), (self.qtgui_time_sink_x_0_0_0_0, 1))    
        self.connect((self.classifier_energy_detection_vcf_0, 2), (self.qtgui_time_sink_x_0_0_0_0, 2))    
        self.connect((self.classifier_energy_detection_vcf_0, 3), (self.qtgui_time_sink_x_0_0_0_0, 3))    
        self.connect((self.classifier_feature_extraction_f_0, 0), (self.scenario_classification_f, 0))    
        self.connect((self.classifier_feature_extraction_f_0, 1), (self.scenario_classification_f, 1))    
        self.connect((self.classifier_feature_extraction_f_0, 2), (self.scenario_classification_f, 2))    
        self.connect((self.classifier_feature_extraction_f_0, 3), (self.scenario_classification_f, 3))    
        self.connect((self.classifier_feature_extraction_f_0, 4), (self.scenario_classification_f, 4))    
        self.connect((self.classifier_feature_extraction_f_0, 5), (self.scenario_classification_f, 5))    
        self.connect((self.classifier_frame_detection_f_0, 0), (self.classifier_feature_extraction_f_0, 0))    
        self.connect((self.classifier_frame_detection_f_0, 1), (self.classifier_feature_extraction_f_0, 1))    
        self.connect((self.classifier_packet_source_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))    
        self.connect((self.fbmc_subchannel_frame_generator_bvc_0, 0), (self.fbmc_tx_sdft_vcc_0, 0))    
        self.connect((self.fbmc_tx_sdft_vcc_0, 0), (self.blocks_vector_insert_x_1_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.classifier_energy_detection_vcf_0, 0))    
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.classifier_cognitive_allocator_0, 0))    
        self.connect((self.uhd_usrp_source_0_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.uhd_usrp_source_0_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.uhd_usrp_source_0_0, 0), (self.qtgui_waterfall_sink_x_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "classify_scenarios")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_mod_order(self):
        return self.mod_order

    def set_mod_order(self, mod_order):
        self.mod_order = mod_order
        self.set_packetlen_base(256 * 12 * self.mod_order)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0_0.set_center_freq(uhd.tune_request(3.195e9, self.samp_rate), 0)
        self.uhd_usrp_sink_1_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_1_0.set_center_freq(uhd.tune_request(3.195e9, self.samp_rate), 0)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_3.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_0.set_samp_rate(self.samp_rate // self.nfft)
        self.qtgui_time_sink_x_0_0_0.set_samp_rate(1 + 0 * self.samp_rate/self.nfft)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_packetlen_base(self):
        return self.packetlen_base

    def set_packetlen_base(self, packetlen_base):
        self.packetlen_base = packetlen_base

    def get_tap_factor(self):
        return self.tap_factor

    def set_tap_factor(self, tap_factor):
        self.tap_factor = tap_factor
        self.set_taps(self.equiripple_118m_132m_500m_70dB * self.tap_factor)

    def get_equiripple_118m_132m_500m_70dB(self):
        return self.equiripple_118m_132m_500m_70dB

    def set_equiripple_118m_132m_500m_70dB(self, equiripple_118m_132m_500m_70dB):
        self.equiripple_118m_132m_500m_70dB = equiripple_118m_132m_500m_70dB
        self.set_taps(self.equiripple_118m_132m_500m_70dB * self.tap_factor)

    def get_cfg(self):
        return self.cfg

    def set_cfg(self, cfg):
        self.cfg = cfg

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.set_su_frame_len((self.su_frame_len_low_rate + len(self.taps))* 4)
        self.set_num_interp_taps(len(self.taps))
        self.interp_fir_filter_xxx_0.set_taps((self.taps))

    def get_phydyas_taps_time(self):
        return self.phydyas_taps_time

    def set_phydyas_taps_time(self, phydyas_taps_time):
        self.phydyas_taps_time = phydyas_taps_time

    def get_nguard_bins(self):
        return self.nguard_bins

    def set_nguard_bins(self, nguard_bins):
        self.nguard_bins = nguard_bins

    def get_nchan(self):
        return self.nchan

    def set_nchan(self, nchan):
        self.nchan = nchan

    def get_sync(self):
        return self.sync

    def set_sync(self, sync):
        self.sync = sync

    def get_tau(self):
        return self.tau

    def set_tau(self, tau):
        self.tau = tau
        self.set_tau_label(self._tau_label_formatter(self.tau))

    def get_su_throughput(self):
        return self.su_throughput

    def set_su_throughput(self, su_throughput):
        self.su_throughput = su_throughput
        self.set_variable_qtgui_label_2_0_1(self._variable_qtgui_label_2_0_1_formatter(self.su_throughput))

    def get_su_providedthroughput(self):
        return self.su_providedthroughput

    def set_su_providedthroughput(self, su_providedthroughput):
        self.su_providedthroughput = su_providedthroughput
        self.set_variable_qtgui_label_2_0_0_0(self._variable_qtgui_label_2_0_0_0_formatter(self.su_providedthroughput))

    def get_su_frame_len_low_rate(self):
        return self.su_frame_len_low_rate

    def set_su_frame_len_low_rate(self, su_frame_len_low_rate):
        self.su_frame_len_low_rate = su_frame_len_low_rate
        self.set_su_frame_len((self.su_frame_len_low_rate + len(self.taps))* 4)

    def get_scenario(self):
        return self.scenario

    def set_scenario(self, scenario):
        self.scenario = scenario
        self.set_variable_qtgui_label_0(self._variable_qtgui_label_0_formatter(self.scenario))

    def get_pu_throughput(self):
        return self.pu_throughput

    def set_pu_throughput(self, pu_throughput):
        self.pu_throughput = pu_throughput
        self.set_variable_qtgui_label_2_0(self._variable_qtgui_label_2_0_formatter(self.pu_throughput))

    def get_pu_providedthroughput(self):
        return self.pu_providedthroughput

    def set_pu_providedthroughput(self, pu_providedthroughput):
        self.pu_providedthroughput = pu_providedthroughput
        self.set_variable_qtgui_label_2_0_0(self._variable_qtgui_label_2_0_0_formatter(self.pu_providedthroughput))

    def get_ed_noisefloor(self):
        return self.ed_noisefloor

    def set_ed_noisefloor(self, ed_noisefloor):
        self.ed_noisefloor = ed_noisefloor
        self.set_variable_qtgui_label_2(self._variable_qtgui_label_2_formatter(self.ed_noisefloor))

    def get_channel_occupation(self):
        return self.channel_occupation

    def set_channel_occupation(self, channel_occupation):
        self.channel_occupation = channel_occupation
        self.set_variable_qtgui_label_0_1(self._variable_qtgui_label_0_1_formatter(self.channel_occupation))

    def get_variable_qtgui_label_2_0_1(self):
        return self.variable_qtgui_label_2_0_1

    def set_variable_qtgui_label_2_0_1(self, variable_qtgui_label_2_0_1):
        self.variable_qtgui_label_2_0_1 = variable_qtgui_label_2_0_1
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_2_0_1_label, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.variable_qtgui_label_2_0_1)))

    def get_variable_qtgui_label_2_0_0_0(self):
        return self.variable_qtgui_label_2_0_0_0

    def set_variable_qtgui_label_2_0_0_0(self, variable_qtgui_label_2_0_0_0):
        self.variable_qtgui_label_2_0_0_0 = variable_qtgui_label_2_0_0_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_2_0_0_0_label, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.variable_qtgui_label_2_0_0_0)))

    def get_variable_qtgui_label_2_0_0(self):
        return self.variable_qtgui_label_2_0_0

    def set_variable_qtgui_label_2_0_0(self, variable_qtgui_label_2_0_0):
        self.variable_qtgui_label_2_0_0 = variable_qtgui_label_2_0_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_2_0_0_label, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.variable_qtgui_label_2_0_0)))

    def get_variable_qtgui_label_2_0(self):
        return self.variable_qtgui_label_2_0

    def set_variable_qtgui_label_2_0(self, variable_qtgui_label_2_0):
        self.variable_qtgui_label_2_0 = variable_qtgui_label_2_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_2_0_label, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.variable_qtgui_label_2_0)))

    def get_variable_qtgui_label_2(self):
        return self.variable_qtgui_label_2

    def set_variable_qtgui_label_2(self, variable_qtgui_label_2):
        self.variable_qtgui_label_2 = variable_qtgui_label_2
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_2_label, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.variable_qtgui_label_2)))

    def get_variable_qtgui_label_0_1(self):
        return self.variable_qtgui_label_0_1

    def set_variable_qtgui_label_0_1(self, variable_qtgui_label_0_1):
        self.variable_qtgui_label_0_1 = variable_qtgui_label_0_1
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_1_label, "setText", Qt.Q_ARG("QString", repr(self.variable_qtgui_label_0_1)))

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", str(self.variable_qtgui_label_0)))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_1_0.set_normalized_gain(self.tx_gain, 0)
        	

    def get_threshold_delta(self):
        return self.threshold_delta

    def set_threshold_delta(self, threshold_delta):
        self.threshold_delta = threshold_delta
        self.classifier_energy_detection_vcf_0.set_threshold_delta_db(self.threshold_delta)

    def get_tau_label(self):
        return self.tau_label

    def set_tau_label(self, tau_label):
        self.tau_label = tau_label
        Qt.QMetaObject.invokeMethod(self._tau_label_label, "setText", Qt.Q_ARG("QString", repr(self.tau_label)))

    def get_su_frame_len(self):
        return self.su_frame_len

    def set_su_frame_len(self, su_frame_len):
        self.su_frame_len = su_frame_len

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0_0.set_normalized_gain(self.rx_gain, 0)
        	

    def get_pu_frame_len(self):
        return self.pu_frame_len

    def set_pu_frame_len(self, pu_frame_len):
        self.pu_frame_len = pu_frame_len

    def get_num_interp_taps(self):
        return self.num_interp_taps

    def set_num_interp_taps(self, num_interp_taps):
        self.num_interp_taps = num_interp_taps

    def get_nsamp_zeropadding(self):
        return self.nsamp_zeropadding

    def set_nsamp_zeropadding(self, nsamp_zeropadding):
        self.nsamp_zeropadding = nsamp_zeropadding

    def get_nfft(self):
        return self.nfft

    def set_nfft(self, nfft):
        self.nfft = nfft
        self.qtgui_time_sink_x_0_0_0_0.set_samp_rate(self.samp_rate // self.nfft)
        self.qtgui_time_sink_x_0_0_0.set_samp_rate(1 + 0 * self.samp_rate/self.nfft)

    def get_firdes_taps(self):
        return self.firdes_taps

    def set_firdes_taps(self, firdes_taps):
        self.firdes_taps = firdes_taps

    def get_equiripple_200m_40dB(self):
        return self.equiripple_200m_40dB

    def set_equiripple_200m_40dB(self, equiripple_200m_40dB):
        self.equiripple_200m_40dB = equiripple_200m_40dB

    def get_equiripple_120m_130m_500m_50dB(self):
        return self.equiripple_120m_130m_500m_50dB

    def set_equiripple_120m_130m_500m_50dB(self, equiripple_120m_130m_500m_50dB):
        self.equiripple_120m_130m_500m_50dB = equiripple_120m_130m_500m_50dB

    def get_enable_tx(self):
        return self.enable_tx

    def set_enable_tx(self, enable_tx):
        self.enable_tx = enable_tx
        self._enable_tx_callback(self.enable_tx)

    def get_always_send(self):
        return self.always_send

    def set_always_send(self, always_send):
        self.always_send = always_send
        self.classifier_cognitive_allocator_0.set_always_send(self.always_send)
        self._always_send_callback(self.always_send)

    def get_aggro_mode(self):
        return self.aggro_mode

    def set_aggro_mode(self, aggro_mode):
        self.aggro_mode = aggro_mode
        self.classifier_cognitive_allocator_0.set_aggro_mode(self.aggro_mode)
        self._aggro_mode_callback(self.aggro_mode)

    def get_T_disp_ms(self):
        return self.T_disp_ms

    def set_T_disp_ms(self, T_disp_ms):
        self.T_disp_ms = T_disp_ms


def main(top_block_cls=classify_scenarios, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
