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

#ifndef INCLUDED_CLASSIFIER_FRAME_DETECTION_F_IMPL_H
#define INCLUDED_CLASSIFIER_FRAME_DETECTION_F_IMPL_H

#include <classifier/frame_detection_f.h>

namespace gr {
  namespace classifier {

    class frame_detection_f_impl : public frame_detection_f
    {
     private:
      static const int d_nchan = 4; // number of channels
      int d_su_frame_len; // SU frame len in samples
      int d_tolerance; // tolerance for the SU frame length to vary due to estimation errors
      int d_lookahead; // number of samples to look ahead (translates directly to increased latency, so handle with care!)
      
      bool check_if_pu(float* ptr);

     public:
      frame_detection_f_impl(int su_frame_len, int tolerance, int lookahead);
      ~frame_detection_f_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace classifier
} // namespace gr

#endif /* INCLUDED_CLASSIFIER_FRAME_DETECTION_F_IMPL_H */

