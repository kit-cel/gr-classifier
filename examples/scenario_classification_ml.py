#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Scenario Classification Ml
# Generated: Fri Nov 17 18:20:34 2017
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
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import classifier
import numpy as np
import sip
import sys
from gnuradio import qtgui


class scenario_classification_ml(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Scenario Classification Ml")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Scenario Classification Ml")
        qtgui.util.check_set_qss()
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

        self.settings = Qt.QSettings("GNU Radio", "scenario_classification_ml")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.threshold_delta = threshold_delta = 4
        self.samp_rate = samp_rate = int(1e7)
        self.pu_frame_len = pu_frame_len = 80*5*9
        self.nfft = nfft = 256
        self.nchan = nchan = 4

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_raster_sink_x_0_1 = qtgui.time_raster_sink_f(
        	samp_rate,
        	100,
        	10,
        	([]),
        	([]),
        	"Adadada",
        	1,
        	)

        self.qtgui_time_raster_sink_x_0_1.set_update_time(0.10)
        self.qtgui_time_raster_sink_x_0_1.set_intensity_range(-1, 1)
        self.qtgui_time_raster_sink_x_0_1.enable_grid(False)
        self.qtgui_time_raster_sink_x_0_1.enable_axis_labels(True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [5, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_raster_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_raster_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_raster_sink_x_0_1.set_color_map(i, colors[i])
            self.qtgui_time_raster_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_raster_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_raster_sink_x_0_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_raster_sink_x_0_1_win)
        self.classifier_spectrogram_vc_vf_0 = classifier.spectrogram_vc_vf(64, samp_rate)
        self.classifier_dl_class_0 = classifier.dl_class()
        self.blocks_vector_to_stream_0_2 = blocks.vector_to_stream(gr.sizeof_float*1, 10)
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 8192/2 + 64 *0)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/cuervo/thesis/data/final_pu/with_dc/scn_2_snr_15.dat', True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.classifier_spectrogram_vc_vf_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.blocks_vector_to_stream_0_2, 0), (self.qtgui_time_raster_sink_x_0_1, 0))
        self.connect((self.classifier_dl_class_0, 0), (self.blocks_vector_to_stream_0_2, 0))
        self.connect((self.classifier_spectrogram_vc_vf_0, 0), (self.classifier_dl_class_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "scenario_classification_ml")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_threshold_delta(self):
        return self.threshold_delta

    def set_threshold_delta(self, threshold_delta):
        self.threshold_delta = threshold_delta

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)

    def get_pu_frame_len(self):
        return self.pu_frame_len

    def set_pu_frame_len(self, pu_frame_len):
        self.pu_frame_len = pu_frame_len

    def get_nfft(self):
        return self.nfft

    def set_nfft(self, nfft):
        self.nfft = nfft

    def get_nchan(self):
        return self.nchan

    def set_nchan(self, nchan):
        self.nchan = nchan


def main(top_block_cls=scenario_classification_ml, options=None):
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
