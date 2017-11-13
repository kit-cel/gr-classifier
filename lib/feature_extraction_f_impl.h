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

#ifndef INCLUDED_CLASSIFIER_FEATURE_EXTRACTION_F_IMPL_H
#define INCLUDED_CLASSIFIER_FEATURE_EXTRACTION_F_IMPL_H

#include <classifier/feature_extraction_f.h>

namespace gr {
  namespace classifier {
  
        /*
        Feature extraction based on frame start events
        ==============================================
        
        args:
            - sample_rate: rate corresponding to the frame start index (usually NOT USRP sample rate)
            - nframes: number of frames to take into account for estimating one set of features. Every snapshot should incorporate enough frames to make a solid guess
            - stepsize: number of frames to advance between estimations. Can be smaller than nframes to have some overlap.
            
        input:
            - input_items[0]: frame start index
            - input_items[1]: corresponding channel index
            
        output:
            - output_items[0:4]: average inter frame time in ms
            - output_items[4]: overall packet rate in packets/second
        */
        
    class feature_extraction_f_impl : public feature_extraction_f
    {
     private:
      int d_sample_rate;
      int d_nframes;
      int d_frame_len;
      float d_frame_len_ms;
      int d_stepsize;
      static const int d_nchan = 4;
      std::vector<float> d_arrival_times_ms[d_nchan]; // PU frame arrival times 
      std::vector<float> d_inter_arrival_times_ms[d_nchan]; // PU inter frame arrival times
      void clear_arrival_times(); // clears d_mean_interframe_times and d_mean_arrival_times

     public:
      feature_extraction_f_impl(int sample_rate, int nframes, int frame_len, int stepsize);
      ~feature_extraction_f_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace classifier
} // namespace gr

#endif /* INCLUDED_CLASSIFIER_FEATURE_EXTRACTION_F_IMPL_H */

