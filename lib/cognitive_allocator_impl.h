/* -*- c++ -*- */
/* 
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_CLASSIFIER_COGNITIVE_ALLOCATOR_IMPL_H
#define INCLUDED_CLASSIFIER_COGNITIVE_ALLOCATOR_IMPL_H

#include <classifier/cognitive_allocator.h>


namespace gr {
  namespace classifier {

    class cognitive_allocator_impl : public cognitive_allocator
    {
     private:
      static const int d_nchan = 4; // number of channels
      int d_su_frame_len; // in samples respective to the samp_rate
      int d_pu_frame_len; // in samples respective to the samp_rate
      int d_scenario; // current scenario FIXME: work with the expected frame arrivals as cross-check
      uint8_t d_channel_occupation[d_nchan]; // vector of length d_nchan with 1 for occupied and 0 for free channels (regarding the PU)
      uint8_t d_su_channels[d_nchan]; // vector of length d_nchan with 1 for used and 0 for unused/occupied channels (regarding the SU)
      int d_nchan_occupied; // number of occupied channels regarding the estimated scenario
      int d_nsamp_zeropadding; // pad some zeros respective to the samp_rate at the end of the frame to create visible and detectable frames
      int d_wait_time_unexpected_frame_ms; // wait time to clear a channel which has unexpectedly received a PU frame
      int d_scenario_tau; // expected inter frame time in samples at bb_rate. Equals the minimum inter frame time for one channel in hopping scenarios.
      long d_scenario_tau_us; // same as above, in us
      int d_det_rate; // rate at which the detector runs
      int d_bb_rate; // rate at which the baseband signal runs (effectively the USRP samp_rate)
      int d_rate_ratio; // ratio between bb_rate and det_rate (effectively the FFT length), used to translate sample times
      int d_padded_su_frame_len; // SU frame length with zeropadding in samples respective to the samp_rate
      int d_padded_su_frame_us; // same as above, in us
      int d_delay; // delay in samples at bb_rate to take into account when tx'ing frames between PU frames
      long d_delay_us; // same as above, in us
      long long d_pseudotime_sendwindow_end_us[d_nchan]; // pseudo-time at which the next PU frame is expected to begin (in microseconds) on the respective channel
      bool d_pu_frame_chan[d_nchan]; // true if a PU frame arrived on the respective channel
      bool d_enable_tx; // used to enable or disable SU TX
      bool d_always_send; // used to forcibly send without caring about the PU
      gr_complex* d_carrier_buf[d_nchan]; // buffer for carrier waves corresponding to the d_nchan subchannels
      gr_complex* d_buf[d_nchan]; // intermediate buffer for working with the subchannels; alternatively, directly work in the input buffer (DANGER ZONE)
			bool d_im_aggro; // aggro mode!!!
      
      boost::mutex d_mutex; // used to avoid race conditions with the callbacks
      
      void update_scenario(pmt::pmt_t msg);
      void update_frame_arrivals(pmt::pmt_t msg);      
      void add_streamtags();
      long long get_walltime_us();
      bool channel_can_be_used(int idx, long walltime);


     public:
      cognitive_allocator_impl(int su_frame_len, int pu_frame_len, int detection_rate, int baseband_rate, int nsamp_zeropadding, float delay_ms, bool enable_tx, int wait_time_unexpected_frame_ms);
      ~cognitive_allocator_impl();
      
      virtual void set_enable_tx(bool enable){ d_enable_tx = enable; }
      virtual void set_always_send(bool always_send){ d_always_send = always_send; }
			virtual void set_aggro_mode(bool be_aggro){ d_im_aggro = be_aggro; }

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace classifier
} // namespace gr

#endif /* INCLUDED_CLASSIFIER_COGNITIVE_ALLOCATOR_IMPL_H */

