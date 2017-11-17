#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy as np
from gnuradio import gr
from scipy import signal
from scipy import fftpack

class spectrogram_vc_vf(gr.sync_block):
    """
    docstring for block spectrogram_vc_vf
    """
    def __init__(self, nfft, samp_rate):
        gr.sync_block.__init__(self,
            name="spectrogram_vc_vf",
            in_sig=[(np.complex64, 4096)],
            out_sig=[(np.float32, 64)])
        self.nfft = nfft
        self.samp_rate = samp_rate

    def spectrogram(self, input_items):
        """
        takes a certain amount of data from the input and generates a
        64x64 spectrogram
        """
        for i in range(64):
            _, _, Sxx = signal.spectrogram(input_items,
                                           fs=self.samp_rate,
                                           mode='magnitude',
                                           return_onesided=False,
                                           nperseg=self.nfft,
                                           detrend=False,
                                           noverlap=0)
            # The spectrum will be reversed, so we shift it
            Sxx = fftpack.fftshift(Sxx, axes=0)
            # calculate the mean power
            Sxx = 20 * np.log10(Sxx)
            mean_power = np.average(Sxx, axis=1)
            # We stack the spectograms
            specgram = np.array(mean_power)
        return specgram

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        for i in range(len(in0)):
            out[i] = self.spectrogram(in0[i])
        return len(output_items[0])

