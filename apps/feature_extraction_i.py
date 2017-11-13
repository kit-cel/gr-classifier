"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.decim_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, sample_rate=1, nframes=100, stepsize=100):  # only default arguments here
        """
        Feature extraction based on frame start events
        ==============================================
        
        args:
            - sample_rate: rate corresponding to the frame start index (usually NOT USRP sample rate)
            - nframes: number of frames to take into account for estimating one set of features
            - stepsize: number of frames to advance between estimations. Can be smaller than nframes to have some overlap.
            
        input:
            - input_items[0]: frame start index
            - input_items[1]: corresponding channel index
            
        output:
            - output_items[0:4]: average channel occupation
            - output_items[4:8]: average inter frame arrival time
            - output_items[8:12]: variance between inter frame arrival times (might also be averaged over all channels)
        """
        gr.decim_block.__init__(
            self,
            name='Feature extraction',   # will show up in GRC
            in_sig=[np.uint32]*2,
            out_sig=[np.float32]*4,
            decim=stepsize
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.sample_rate = sample_rate
        self.nframes = nframes
        self.stepsize = stepsize
        
        self.nchan = 4
        
    def forecast(self, noutput_items, ninput_items_required):
        for i in range(2):
            ninput_items_required[i] = max(self.nframes, self.stepsize)

    def work(self, input_items, output_items):
        # feature 1: average channel usage
        avg_channel_occupation = np.zeros(self.nchan, dtype=float)
        for i in range(self.chan):
            for f in input_items[1]:  # go through the channel list and count frames
                avg_channel_occupation[f] += 1.0
            avg_channel_occupation[i] /= len(input_items[1])
            output_items[i][0] = avg_channel_occupation[i]
        
        return self.stepsize
