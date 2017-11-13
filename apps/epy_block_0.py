"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Classify scenarios"""

    def __init__(self, tconst=2, tau1=5, tau2=10, lambda1=20, lambda2=50, lambda3=100):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Scenario classification',   # will show up in GRC
            in_sig=[np.float32]*4,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.tconst = tconst
        self.tau1 = tau1
        self.tau2 = tau2
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.lambda3 = lambda3
        
        self.scenario = None
        cchan_occupied = None
        self.tau = None
        
    def run_decision_tree(self, features):
        self.chan_occupied = features >= 0
        nchan_occupied = sum(self.chan_occupied)
        self.tau = np.mean([features[i] for i in range(4) if chan_occupied[i]])
        
        if nchan_occupied == 1:
            if self.tau < float(self.tau1 + self.tau2) / 2:
                s = 0
            else:
                s = 1
        elif nchan_occupied == 2:
            if self.tau < float(3 * self.tau1) / 2:
                s = 4
            else:
                s = 2
        elif nchan_occupied == 4:
            if self.tau < float(self.tconst + self.tau1) / 2:
                s = 6
            elif self.tau < float(5 * self.tau2) / 2:
                s = 5
            elif self.tau < float(4 * self.tau2 + self.lambda1) / 2:
                s = 3
            elif self.tau < float(self.lambda1 + self.lambda2) / 2:
                s = 7
            elif self.tau < float(self.lambda2 + self.lambda3) / 2:
                s = 8
            else:
                s = 9
        else:
            s = self.scenario  # stick with the last estimation
            
        self.scenario = s
        
        print "nchan_occupied:", nchan_occupied, ", tau:", tau
            
        return self.scenario

    def work(self, input_items, output_items):
        features = np.array([input_items[i][0] for i in range(4)])
        self.run_decision_tree(features)
        print "Detected scenario:", self.scenario
        return 1
