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

class np_average_vf_vf(gr.basic_block):
    """
    docstring for block np_average_vf_vf
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="np_average_vf_vf",
            in_sig=[(np.float32, 64)],
            out_sig=[(np.float32, 64)])

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = 120 * noutput_items

    def general_work(self, input_items, output_items):
        output_items[0][:] = np.average(input_items[0][:120].T, axis=1)
        self.consume_each(len(input_items[0]))
        return len(output_items[0])
