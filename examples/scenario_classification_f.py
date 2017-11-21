"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import scipy.stats as st
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Classify scenarios"""

    def __init__(self, tconst=2, tau1=5, tau2=10, lambda1=20, lambda2=50, lambda3=100):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Scenario classification',   # will show up in GRC
            in_sig=[np.float32]*6,
            out_sig=[(np.float32, 10)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.tconst = tconst
        self.tau1 = tau1
        self.tau2 = tau2
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.lambda3 = lambda3
        self.nchan = 4
        self.scenario_tau = np.array([self.tau1, self.tau2, 2*self.tau1, 4*self.tau2, self.tau1, self.tau1, self.tconst, self.lambda1, self.lambda2, self.lambda3, 0])  # scenario 10 is "unsure, don't send"
        self.scenario_send_window = self.scenario_tau.copy()  # the send window for the hopping and Poisson scenarios differs from the deterministic ones
        self.scenario_send_window[2] = self.tau1
        self.scenario_send_window[3] = self.tau2
        for i in range(7, 10):
          self.scenario_send_window[i] = st.poisson.ppf(0.05, self.scenario_tau[i])
        print "expected mean inter frame times: ", self.scenario_tau
        print "send windows: ", self.scenario_send_window
        
        self.max_confidence = 3
        self.confidence = 0
        
        self.scenario = 10
        self.chan_occupied = [False] * self.nchan  # list of true/false values
        self.tau = None
        
        self.message_port_register_out(pmt.intern("scenario"))
        
    def get_scenario(self):
        return self.scenario
        
    def get_chan_occupied(self):
            return [i for i in range(self.nchan) if self.chan_occupied[i]]
        
    def get_tau(self):
        return self.tau
        
    def run_decision_tree(self, inter_frame_times, inter_frame_time_variance):
        chan_occupied = list(inter_frame_times >= 0)  # all channels that have an inter frame arrival time > 0 are regarded as being occupied FIXME: handle wildly different values as being false (e.g., due to one channel no longer being used)
        nchan_occupied = sum(chan_occupied)  # number of occupied channels
        self.tau = np.mean([inter_frame_times[i] for i in range(self.nchan) if chan_occupied[i]])  # inter arrival time averaged over occupied channels
        delta_tau = abs(self.tau - self.scenario_tau)
        
        if nchan_occupied == 1:  # possible scenarios: 0 or 1 (deterministic transmission with tau1 or tau2 on a single channel, respectively)
            possible_scenarios = [0, 1]
            idx = np.argmin([delta_tau[i] for i in possible_scenarios])
            s = possible_scenarios[idx]
        elif nchan_occupied == 2:  # possible scenarios: 2 or 4 (hopping or deterministic with tau1 on two channels, respectively)
            possible_scenarios = [2, 4]
            idx = np.argmin([delta_tau[i] for i in possible_scenarios])
            s = possible_scenarios[idx]
        elif nchan_occupied == 4:  # possible scenarios: 6 (all channels deterministic with tconst), 5 (all channels deterministic with tau1), 3 (all channels hopping with tau1), 7-9 (all channels, Poisson process with different lambdas)
            possible_scenarios = [3, 5, 6, 7, 8, 9]
            idx = np.argmin([delta_tau[i] for i in possible_scenarios])
            if possible_scenarios[idx] == 5 or possible_scenarios[idx] == 9:  # they have the same mean interarrival time, decide based on the variance
              if inter_frame_time_variance > float(self.scenario_tau[9])/2:  # considerable variance indicates the non-deterministic Poisson scenario (expected variance is equal to the mean interframe time)
                s = 9
              else:
                s = 5
            else:
              s = possible_scenarios[idx]
        else:  # 0 or 3 occupied channels is not a valid scenario
            s = 10  # stick with the last estimation
            
        return s, chan_occupied
        
    def post_message(self):
        msg_dict = pmt.make_dict()
        msg_dict = pmt.dict_add(msg_dict, pmt.intern("scenario_number"), pmt.from_long(long(self.scenario)))
        msg_dict = pmt.dict_add(msg_dict, pmt.intern("scenario_channels"), pmt.to_pmt([bool(c) for c in self.chan_occupied]))
        msg_dict = pmt.dict_add(msg_dict, pmt.intern("scenario_tau"), pmt.from_long(long(self.scenario_send_window[self.scenario])))
        self.message_port_pub(pmt.intern("scenario"), msg_dict)

    def work(self, input_items, output_items):
	scn = output_items[0]
        inter_frame_times = np.array([input_items[i][0] for i in range(self.nchan)])  # current inter frame arrival time per channel
        packet_rate = input_items[4][0]  # not used at the moment
        inter_frame_time_variance = input_items[5][0]  # variance of the inter frame arrival time (averaged over all channels)
        detected_scenario, chan_occupied = self.run_decision_tree(inter_frame_times, inter_frame_time_variance)
	scn[:] = (np.arange(10) == detected_scenario).astype(float)
        if detected_scenario != self.scenario or chan_occupied != self.chan_occupied:
            self.confidence -= 1
            if self.confidence < 0:
                self.scenario = detected_scenario
		
                self.chan_occupied = chan_occupied
                self.confidence = 0
                self.post_message()
        else:
           self.confidence = min(self.confidence + 1, self.max_confidence)
        return 1
