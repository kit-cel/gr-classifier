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

import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.image import img_to_array, array_to_img

class dl_scn_classification_c(gr.sync_block):
    """
    docstring for block dl_scn_classification_c
    """
    def __init__(self, nfft, samp_rate):
        gr.sync_block.__init__(self,
                               name="dl_scn_classification_c",
                               in_sig=[(np.complex64, 4096)],
                               out_sig=[(np.float32, 10)],
                               )
        self.model = load_model('/home/cuervo/thesis/cognitive_radio_ml/weights/adadelta_default_es_model.h5')
        # predict function and graph workaround taken from
        # https://github.com/fchollet/keras/issues/2397
        self.model._make_predict_function()
        self.graph = tf.get_default_graph()
        self.nfft = nfft
        self.samp_rate = samp_rate
        self.count = 0

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
            if i == 0:
                stacked = np.array(mean_power)
            else:
                stacked = np.vstack([stacked, mean_power])
        # The model requires dimensions (1, 64, 64, 1)
        stacked = np.expand_dims(stacked, axis=2)
        # print(stacked)
        image = array_to_img(stacked, scale=False)
        return image

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        for i in range(len(in0)):
            image = self.spectrogram(in0[i])
            sample = img_to_array(image)
            print(sample)
            sample = np.expand_dims(sample, axis=0)
            self.count =+ 1
            with self.graph.as_default():
                out[i] = self.model.predict(sample)
                print(self.model.predict(sample))
        return len(out)

