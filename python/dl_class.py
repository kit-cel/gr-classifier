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
from scipy.misc import toimage

import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.image import img_to_array, array_to_img

class dl_class(gr.basic_block):
    """
    docstring for block dl_class
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="dl_class",
            in_sig=[(np.float32, 64)],
            out_sig=[(np.float32, 10)]
            )
        self.model = load_model('/home/cuervo/thesis/cognitive_radio_ml/trained_models/keras/sgd_model_checkpoint.h5')
        self.model._make_predict_function()
        self.graph = tf.get_default_graph()

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = 64*noutput_items

    def general_work(self, input_items, output_items):
        out = output_items[0]
        #output_items[0][:] = input_items[0]
        #self.consume_each(len(input_items[0]))
        for i in range(64):
            if i == 0:
                stacked = np.array(input_items[0][i])
            else:
                stacked = np.vstack([stacked, input_items[0][i]])
        # The model requires dimensions (1, 64, 64, 1)
        # stacked = np.expand_dims(stacked, axis=2)
        # print(stacked)
        image = toimage(stacked, channel_axis=2)
        # image = array_to_img(stacked, scale=False)

        sample = img_to_array(image)
        # print(sample)
        sample = np.expand_dims(sample, axis=0)
        # print(sample.shape)
        with self.graph.as_default():
            out[:] = self.model.predict(sample)
            print(np.argmax(self.model.predict(sample)))

        self.consume(0, len(input_items[0]))
        return len(output_items[0])
