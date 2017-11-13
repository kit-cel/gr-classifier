"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, input_rate=1, window_len_ms=100, max_occupation=0.5, stepsize_ms=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.float32, np.float32, np.float32, np.float32],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.input_rate = input_rate
        self.window_len_ms = window_len_ms
        self.max_occupation = max_occupation
        self.stepsize_ms = stepsize_ms
        
        self.nchan = 4
        self.window_len = int(float(self.window_len_ms) / 1000 * self.input_rate)
        self.stepsize = int(float(self.stepsize_ms) / 1000 * self.input_rate)
        self.channel_state = None
        
        print self.window_len, self.stepsize
        
    def forecast(self, noutput_items, ninput_items_required):
        for i in range(self.nchan):
            ninput_items_required[i] = self.window_len
        
    def work(self, input_items, output_items):
        current_channel_state = [1 if input_items[i][:self.window_len].mean() > self.max_occupation else 0 for i in range(self.nchan)]
        if current_channel_state != self.channel_state:
          self.channel_state = current_channel_state
          print "Channel state:", self.channel_state
        return self.stepsize
