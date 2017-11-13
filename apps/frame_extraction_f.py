"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Frame extraction',   # will show up in GRC
            in_sig=[np.float32]*4,#[np.float32, np.float32, np.float32, np.float32],
            out_sig=[np.uint32]*2#[np.uint64, np.uint8]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        
        self.nchan = 4
        
    def general_work(self, input_items, output_items):
        nitems_available_in = len(input_items[0])
        nitems_available_out = min(len(output_items[0]), len(output_items[1]))
        nitems_read = 0
        nitems_written = 0
        
        """ 
        output_items[0]: frame start index
        output_items[1]: channel index
        """
        
        for i in range(self.nchan):
            j = 0
            while j < nitems_available_in-1 and nitems_written < nitems_available_out:
                nitems_read += 1
                if input_items[i][j] == 0 and input_items[i][j+1] == 1:  # rising slope --> frame start
                    output_items[0][nitems_written] = self.nitems_read(i) + j + 1  # total sample index
                    output_items[1][nitems_written] = i
                    nitems_written += 1
                    
        self.consume_each(nitems_read)
        return nitems_written
