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
from sklearn.externals import joblib
import pmt

class ml_scn_classification_f(gr.sync_block):
    """
    docstring for block ml_scn_classification_f
    """
    def __init__(self, modelfile, scalerfile):
        gr.sync_block.__init__(self,
            name="ml scn classification",
            in_sig=[np.float32]*6,
            out_sig=None
            )
	self.scenario = 10
	self.message_port_register_out(pmt.intern("scenario"))
	self.modelfile = modelfile
	self.model = joblib.load(modelfile)
	self.scaler = joblib.load(scalerfile)

    def post_message(self):
        msg_dict = pmt.make_dict()
        msg_dict = pmt.dict_add(msg_dict, pmt.intern("scenario_number"), pmt.from_long(long(self.scenario)))
        self.message_port_pub(pmt.intern("scenario"), msg_dict)

    def work(self, input_items, output_items):
        """
        -Pack the samples in a numpy array
        -Scales them if needed based on the trained scaler
        -Predicts the used scenario
        -Posts the prediction at the message port
        """
        # Increase of dimension for the sample is important
        # see https://stackoverflow.com/questions/35082140/preprocessing-in-scikit-learn-single-sample-depreciation-warning
        sample = np.array([[input_items[i][0] for i in range(6)]])
        sample_scaled = self.scaler.transform(sample)
        detected_scenario = self.model.predict(sample_scaled)
        #if detected_scenario != self.scenario:
        #	self.scenario = detected_scenario
        #	self.post_message()
        self.scenario = detected_scenario
        self.post_message()
        return 1
