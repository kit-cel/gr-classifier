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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "cognitive_allocator_impl.h"
#include <volk/volk.h>

namespace gr {
  namespace classifier {
  
    cognitive_allocator::sptr
    cognitive_allocator::make(int su_frame_len, int pu_frame_len, int detection_rate, int baseband_rate, int nsamp_zeropadding, float delay_ms, bool enable_tx, int wait_time_unexpected_frame_ms)
    {
      return gnuradio::get_initial_sptr
        (new cognitive_allocator_impl(su_frame_len, pu_frame_len, detection_rate, baseband_rate, nsamp_zeropadding, delay_ms, enable_tx, wait_time_unexpected_frame_ms));
    }

    /*
     * The private constructor
     */
    cognitive_allocator_impl::cognitive_allocator_impl(int su_frame_len, int pu_frame_len, int detection_rate, int baseband_rate, int nsamp_zeropadding, float delay_ms, bool enable_tx, int wait_time_unexpected_frame_ms)
      : gr::block("cognitive_allocator",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex))),
              d_su_frame_len(su_frame_len),
              d_pu_frame_len(pu_frame_len),
              d_nsamp_zeropadding(nsamp_zeropadding),
              d_scenario(10),
              d_scenario_tau(0),
              d_det_rate(detection_rate),
              d_bb_rate(baseband_rate),
              d_padded_su_frame_len(su_frame_len+nsamp_zeropadding),
              d_enable_tx(enable_tx),
              d_wait_time_unexpected_frame_ms(wait_time_unexpected_frame_ms),
              d_always_send(0),
							d_im_aggro(false)
    {
        message_port_register_in(pmt::intern("scenario"));
        set_msg_handler(pmt::intern("scenario"), boost::bind(&cognitive_allocator_impl::update_scenario, this, _1));
        
        message_port_register_in(pmt::intern("pu_frame_start"));
        set_msg_handler(pmt::intern("pu_frame_start"), boost::bind(&cognitive_allocator_impl::update_frame_arrivals, this, _1));
        
        message_port_register_in(pmt::intern("enable_tx"));
        set_msg_handler(pmt::intern("enable_tx"), boost::bind(&cognitive_allocator_impl::set_enable_tx, this, true));
        
        memset(d_su_channels, 0, d_nchan); // SU uses no channels; overwritten before first evaluation
        memset(d_channel_occupation, 1, d_nchan); //  conservative default: all channels are occupied
        d_nchan_occupied = d_nchan;
        
        memset(d_pu_frame_chan, 0, sizeof(bool)*d_nchan); // means "no frames arrived recently"
        memset(d_pseudotime_sendwindow_end_us, 0, sizeof(long)*d_nchan); // will be overwritten before first use
        
        d_delay = int(delay_ms / 1000 * d_bb_rate); // estimated delay in samples at bb_rate
        d_delay_us = long(delay_ms * 1000); // in us
        
        d_padded_su_frame_us = long(float(d_padded_su_frame_len) / d_bb_rate * 1000000);
        
        d_rate_ratio = d_bb_rate / d_det_rate; // assumed to be an integer
        
        // prepare the carrier waves; starting phase is irrelevant as the frames are not continuous
        gr_complex phase_increment[4] = {gr_complex(0, -3.0/8*2.0*M_PI), gr_complex(0, -1.0/8*2.0*M_PI), gr_complex(0, 1.0/8*2.0*M_PI), gr_complex(0, 3.0/8*2.0*M_PI)}; // corresponds to the center frequencies of the four channels
        for(int i=0; i<d_nchan; i++)
        {
          d_carrier_buf[i] = new gr_complex[d_su_frame_len];
          for(int n=0; n<d_su_frame_len; n++)
          {
            d_carrier_buf[i][n] = std::exp(phase_increment[i]*gr_complex(n, 0));
          }
          d_buf[i] = new gr_complex[d_su_frame_len];
        }
        
        set_output_multiple(d_padded_su_frame_len);
        
        set_tag_propagation_policy(TPP_DONT);
    }

    /*
     * Our virtual destructor.
     */
    cognitive_allocator_impl::~cognitive_allocator_impl()
    {
        for(int i=0; i<d_nchan; i++)
        {
          delete[] d_carrier_buf[i];
          delete[] d_buf[i];
        }
    }

    void
    cognitive_allocator_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      // output buffer of upstream block should be considerably larger to allow for buffering
      ninput_items_required[0] = d_su_frame_len * d_nchan;
    }
    
    void 
    cognitive_allocator_impl::update_scenario(pmt::pmt_t msg)
    {
      boost::mutex::scoped_lock lock(d_mutex);
			if(pmt::to_long(pmt::dict_ref(msg, pmt::intern("scenario_number"), pmt::PMT_NIL)) != 10)
			{
      d_scenario = pmt::to_long(pmt::dict_ref(msg, pmt::intern("scenario_number"), pmt::PMT_NIL));
      //std::cout << "cognitive_allocator_impl: scenario update: " << d_scenario;
      long scenario_tau_ms = pmt::to_long(pmt::dict_ref(msg, pmt::intern("scenario_tau"), pmt::PMT_NIL));
      d_scenario_tau = scenario_tau_ms * d_bb_rate / 1000;
      d_scenario_tau_us = scenario_tau_ms * 1000;
      //std::cout << ", tau: " << d_scenario_tau;
      uint8_t channels[d_nchan];
      d_nchan_occupied = 0;
      for(int i=0; i<d_nchan; i++)
      {
          bool is_occupied = pmt::to_bool(pmt::vector_ref(pmt::dict_ref(msg, pmt::intern("scenario_channels"), pmt::PMT_NIL), i));
          d_channel_occupation[i] = is_occupied;
          d_nchan_occupied += is_occupied;
          //std::cout << ", ch" << i << ": " << int(d_channel_occupation[i]);
      }
			}
      //std::cout << std::endl;
    }
    
    long long
    cognitive_allocator_impl::get_walltime_us()
    {
      return boost::posix_time::microsec_clock::local_time().time_of_day().total_microseconds();
    }
    
    void 
    cognitive_allocator_impl::update_frame_arrivals(pmt::pmt_t msg)
    {
      boost::mutex::scoped_lock lock(d_mutex);
      int chan_idx = pmt::to_long(pmt::cdr(msg));
      d_pu_frame_chan[chan_idx] = true;
      long long walltime = get_walltime_us();
      if(d_channel_occupation[chan_idx] == 1) // this is an expected PU frame
      {
        if(d_scenario == 2 or d_scenario == 3) // in the hopping scenarios, clear the other 1/3 channels too
        {
          for(int i=0; i < d_nchan; i++)
          {
            if(d_channel_occupation[i] == 1)
            {
              d_pseudotime_sendwindow_end_us[i] = walltime + d_scenario_tau_us - d_delay_us;
            }
          }
        }
        else
        {
          d_pseudotime_sendwindow_end_us[chan_idx] = walltime + d_scenario_tau_us - d_delay_us; // walltime at which the next frame is expected.
        }
      }
      else // unexpected PU frame, set some wait time before using the channel again
      {
        //std::cout << "unexpected PU, set sendwindow to " << d_pseudotime_sendwindow_end_us[chan_idx] << ", now it's " << d_pseudotime_sendwindow_end_us[chan_idx] - d_wait_time_unexpected_frame_ms * 1000 << std::endl;
        if(!d_im_aggro)
				{
								d_pseudotime_sendwindow_end_us[chan_idx] = walltime + d_wait_time_unexpected_frame_ms * 1000;
				}
      }
      //std::cout << "cognitive_allocator: received PU frame on ch" << chan_idx << " at " << d_pseudotime_sendwindow_end_us[chan_idx] - d_scenario_tau_us + d_delay_us << ", next frame expected to start at / waiting time until " << d_pseudotime_sendwindow_end_us[chan_idx] << " us." << std::endl;
    }
    
    void
    cognitive_allocator_impl::add_streamtags()
    {
        // this adds a set of streamtags to the output.
        static const pmt::pmt_t sob_key = pmt::string_to_symbol("tx_sob");
        static const pmt::pmt_t eob_key = pmt::string_to_symbol("tx_eob");
        static const pmt::pmt_t value = pmt::PMT_T;
        static const pmt::pmt_t srcid = pmt::string_to_symbol(alias());
        add_item_tag(0, nitems_written(0), sob_key, value, srcid);
        add_item_tag(0, nitems_written(0)+d_padded_su_frame_len-1, eob_key, value, srcid);
    }
    
    bool
    cognitive_allocator_impl::channel_can_be_used(int idx, long walltime)
    {      
      boost::mutex::scoped_lock lock(d_mutex);
      
      if(d_always_send){ return true; } // this causes transmissions on all channels irrespective of PU behavior
      
      if(d_scenario == 10){ return false; } // don't send if in unknown scenario
      
      if(d_channel_occupation[idx] == 1) // this channel is expected to be occupied due to the current scenario
      {
        //std::cout << "occ, ";
        if(d_pu_frame_chan[idx] == true) // a PU frame was registered in the recent past
        {
          if(d_pseudotime_sendwindow_end_us[idx] - walltime > d_padded_su_frame_us) // enough time left, send a frame
          {
            //std::cout << "time left." << std::endl;
            d_pseudotime_sendwindow_end_us[idx] -= d_padded_su_frame_us; // decrease the length of the send window by one frame including zero-padding
            //std::cout << "ch" << idx << ": SEND. Time left: " << d_padded_su_frame_us << " us." << std::endl;
            return true;
          }
          else // not enough time, dont send
          {
            //std::cout << "no time left." << std::endl;
            //std::cout << "ch" << idx << ": DON'T SEND. Wait for next frame." << std::endl;
            d_pu_frame_chan[idx] = false; // don't send on this channel until the next frame is received or the scenario update frees it.
            d_pseudotime_sendwindow_end_us[idx] = 0; // back to the default value
            return false;
          }
        }
        else // there has been no frame in the recent past, don't send to avoid interference.
        {
          //std::cout << "wait for frame." << std::endl;
          return false;
        }
      }
      else // according to the current scenario, this channel should be unused by the PU
      {
        if(d_im_aggro){ return true; }// FIXME: There is a bug when the scenario switches that leads to the lock-out of channels, the sendwindow gets really large and therefore no frames are sent
        
        //std::cout << "free, ";
        if(d_pu_frame_chan[idx] == false) // as expected, there has been no PU frame recently. Send.
        {
          //std::cout << "no PU." << std::endl;
          return true;
        }
        else // there is an unexpected PU frame. Be careful and don't send.
        {
          //std::cout << "unexpected PU, ";
          if(walltime > d_pseudotime_sendwindow_end_us[idx]) // this channel has not been used for a while, we assume it stays free
          {
            //std::cout << "wait time over." << std::endl;
            return true;
          }
          else // wait some time to be sure this was a spurious event
          {
           //std::cout << "wait. walltime/sendwindow_end: " << walltime << "/" << d_pseudotime_sendwindow_end_us[idx] << std::endl;
           return false;
          }
        }
      }
    }

    int
    cognitive_allocator_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      if(not(d_enable_tx)) // if TX is disabled, do nothing and return.
      {
        return 0; 
      } 
      
      //std::cout << "cognitive_allocator::work() with d_enable_tx==True, ninput_items[0]:" << ninput_items[0] << ", RT: " << boost::posix_time::microsec_clock::local_time().time_of_day().total_milliseconds() << std::endl;
      
      const gr_complex *frame_in = (const gr_complex*) input_items[0];
      
      gr_complex *out = (gr_complex*) output_items[0];
      
      int nchannels_used = 0; // channels used by the SU in this call to work()
      
      long long walltime = get_walltime_us(); // walltime
      
      //std::cout << "channel usage: ";
      for(int i=d_nchan-1; i>=0; i--) // fill channels from right to left (positive to negative frequencies)
      {
        if(channel_can_be_used(i, walltime))
        {
          //std::cout << i << " ";
          volk_32fc_x2_multiply_32fc(d_buf[i], &frame_in[nchannels_used*d_su_frame_len], d_carrier_buf[i], d_su_frame_len); // mix with the subchannel's carrier frequency
          nchannels_used += 1;
          d_su_channels[i] = 1;           
        }
        else
        {
          d_su_channels[i] = 0;
        }
      }
      //std::cout << std::endl;
      
      // if no channel could be used, return 0 instead of writing zeros into the output buffer
      if(nchannels_used == 0)
      {
        return 0;
      }
      
      // set the output buffer to zeros and then add the subchannel signals
      // FIXME: only add the signals and then set only the padded zeros
      memset(out, 0, sizeof(gr_complex) * d_padded_su_frame_len);
      for(int i=0; i < d_nchan; i++)
      {
        if(d_su_channels[i] == 1) 
        {
          volk_32f_x2_add_32f((float*) out, (float*) out, (float*) d_buf[i], d_su_frame_len * 2); // fake a complex addition by doing a double length float addition
        }
      }
      
      // set SOB and EOB streamtags
      add_streamtags();
        
      // continue here
      consume_each (d_su_frame_len * nchannels_used);

      // Tell runtime system how many output items we produced.
      //std::cout << "write " << d_su_frame_len + d_nsamp_zeropadding << " items in the output buffer" << std::endl;
      return d_padded_su_frame_len;
    }

  } /* namespace classifier */
} /* namespace gr */

