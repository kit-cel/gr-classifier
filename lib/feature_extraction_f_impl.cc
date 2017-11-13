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
#include "feature_extraction_f_impl.h"

namespace gr {
  namespace classifier {

    feature_extraction_f::sptr
    feature_extraction_f::make(int sample_rate, int nframes, int frame_len, int stepsize)
    {
      return gnuradio::get_initial_sptr
        (new feature_extraction_f_impl(sample_rate, nframes, frame_len, stepsize));
    }

    /*
     * Outputs 0-3 denote inter frame times in ms, output 4 is the overall packet rate in seconds
     */
    feature_extraction_f_impl::feature_extraction_f_impl(int sample_rate, int nframes, int frame_len, int stepsize)
      : gr::sync_decimator("feature_extraction_f",
              gr::io_signature::make(2, 2, sizeof(int)),
              gr::io_signature::make(6, 6, sizeof(float)), stepsize),
          d_sample_rate(sample_rate),
          d_nframes(nframes),
          d_frame_len(frame_len),
          d_stepsize(stepsize),
          d_frame_len_ms(float(frame_len)/sample_rate*1000)
    {
        if(d_nframes < d_stepsize)
        {
          throw std::runtime_error("nframes must be greater or equal to stepsize");
        }
        set_output_multiple(nframes/stepsize);
        if(d_nframes < d_nchan * 5)
        {
          std::cout << "WARNING: choosing nframes too small may lead to unreliable estimations, especially for the variance" << std::endl;
        }
        set_history(std::max(0, d_nframes - d_stepsize)+1); // make sure there are enough items in the input buffer if stepsize < nframes
    }

    /*
     * Our virtual destructor.
     */
    feature_extraction_f_impl::~feature_extraction_f_impl()
    {
    }
    
    void
    feature_extraction_f_impl::clear_arrival_times()
    {
      for(int i = 0; i < d_nchan; i++)
      {
        d_arrival_times_ms[i].clear();
        d_inter_arrival_times_ms[i].clear();
      }
    }

    int
    feature_extraction_f_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const int *frame_start_idx = (const int *) input_items[0];
      const int *frame_chan_idx = (const int *) input_items[1];
      float *ift[d_nchan] = {(float *) output_items[0], (float *) output_items[1], (float *) output_items[2], (float *) output_items[3]}; //  inter frame time in ms
      float *pu_rate = (float *) output_items[4]; // packet rate in packets per second
      float *frame_arrival_variance = (float *) output_items[5]; // variance of the inter frame delay
      
      for(int n = 0; n < noutput_items; n++)
      {
        clear_arrival_times(); // reset the vectors
        
        // sort the frames into the corresponding vectors
        for(int i = 0; i < d_nframes; i++)
        {
          d_arrival_times_ms[frame_chan_idx[i + n * d_stepsize]].push_back(float(frame_start_idx[i + n * d_stepsize]) * 1000 / d_sample_rate);
          //std::cout << "pushed back IFT: " << d_arrival_times_ms[frame_chan_idx[i + n * d_stepsize]].back() << std::endl;
        }
        
        // FEATURE 1: average interframe time
        float window_len_ms = float(frame_start_idx[n * d_stepsize + d_nframes-1] + d_frame_len - frame_start_idx[n * d_stepsize]) * 1000 / d_sample_rate; // window length depends on the packet rate
        //std::cout << "ch";
        for(int i = 0; i < d_nchan; i++)
        {
          //std::cout << i << ": ";
          int num_frames = d_arrival_times_ms[i].size(); // number of frames detected in the i'th channel
          if(num_frames == 0) // no frame detected
          {
            //std::cout << "no frame." << std::endl;
            ift[i][n] = -1;
          }
          else if(num_frames == 1) // only one frame detected, interframe time >= observation interval, assume the minimum
          {
            //std::cout << "1 frame." << std::endl;
            ift[i][n] = window_len_ms - d_frame_len_ms;
          }
          else // more than one frame, take the mean
          {
            //std::cout << num_frames << " frames." << std::endl;
            //std::cout << d_arrival_times_ms[i][0] - d_arrival_times_ms[i][num_frames-1] << std::endl;
            ift[i][n] = (d_arrival_times_ms[i][num_frames-1] - d_arrival_times_ms[i][0] - d_frame_len_ms * (num_frames - 1)) / (num_frames - 1);            
          }
        }
        
        // FEATURE 2: total packet rate
        int total_frames = 0;
        for(int i = 0; i < d_nchan; i++)
        {
          total_frames += d_arrival_times_ms[i].size();
        }
        pu_rate[n] = float(total_frames) / (window_len_ms / 1000);
        
        // FEATURE 3: inter frame time variance
        for(int i = 0; i < d_nchan; i++) // determine the inter arrival times per channel
        {
          for(int k = 1; k < d_arrival_times_ms[i].size(); k++)
          {
            d_inter_arrival_times_ms[i].push_back(d_arrival_times_ms[i][k] - d_arrival_times_ms[i][k-1]);
          }
        }
        
        // calculate the variance for channels with more than one received packet (set to -1, if no variance can be calculated)
        int num_estimations = 0;
        frame_arrival_variance[n] = 0;
        for(int i = 0; i < d_nchan; i++) 
        {
          for(int k = 0; k < d_inter_arrival_times_ms[i].size(); k++)
          {
            frame_arrival_variance[n] += std::pow(d_inter_arrival_times_ms[i][k] - ift[i][n], 2);
            num_estimations++;
          }
        }
        if(num_estimations > 0)
        {
          frame_arrival_variance[n] /= num_estimations; // average over the number of estimations available (should be the same for all channels)
        }
        else
        {
          frame_arrival_variance[n] = -1;
        }
      }
      
      return noutput_items;
    }

  } /* namespace classifier */
} /* namespace gr */

