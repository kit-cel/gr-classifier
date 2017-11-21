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
from scipy.misc import toimage, imsave

import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.image import img_to_array, array_to_img

class dl_class(gr.basic_block):
    """
    docstring for block dl_class
    """
    def __init__(self, modelfile):
        gr.basic_block.__init__(self,
            name="dl_class",
            in_sig=[(np.float32, 64)],
            out_sig=[(np.float32, 10)] * 2
            )
        self.model = load_model(modelfile)

        # predict function and graph workaround taken from
        # https://github.com/fchollet/keras/issues/2397
        # Used in the general_work function
        self.model._make_predict_function()
        self.graph = tf.get_default_graph()

        # [Debug variable] - Uncomment for saving images to disk
        self.count = 100

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        # We need 64 stacked items for 64x64 images
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = 64*noutput_items

    def general_work(self, input_items, output_items):
        pred_prob = output_items[0]
        scn = output_items[1]
        # scn = np.zeros(10, dtype=np.float32)
        # scn = np.ones(10, dtype=np.float32)
        for i in range(64):
            if i == 0:
                stacked = np.array(input_items[0][i])
            else:
                stacked = np.vstack([stacked, input_items[0][i]])

        # [Debug statements] - Uncomment to save image to disk
        imsave("/home/cuervo/test/test_image_{}.jpg".format(self.count), stacked)
        self.count += 1

        # Generate a image object from the received samples
        image = toimage(stacked, channel_axis=2)

        # Now pass it as an array for image classification
        sample = img_to_array(image)

        # The model requires dimensions (1, 64, 64, 1)
        sample = np.expand_dims(sample, axis=0)
        with self.graph.as_default():
            pred_prob[:] = self.model.predict(sample)
            scn[:] = (np.arange(10) == np.argmax(self.model.predict(sample))).astype(float)
            # a = (np.arange(10) == 4).astype(float)
        self.consume(0, len(input_items[0]))
        return len(output_items[0])
