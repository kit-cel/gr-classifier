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
#include "frame_detection_f_impl.h"

namespace gr {
  namespace classifier {

    frame_detection_f::sptr
    frame_detection_f::make(int su_frame_len, int tolerance, int lookahead)
    {
      return gnuradio::get_initial_sptr
        (new frame_detection_f_impl(su_frame_len, tolerance, lookahead));
    }

    /*
     * The private constructor
     */
    frame_detection_f_impl::frame_detection_f_impl(int su_frame_len, int tolerance, int lookahead)
      : gr::block("frame_detection_f",
              gr::io_signature::make(4, 4, sizeof(float)),
              gr::io_signature::make(2, 2, sizeof(int))),
              d_su_frame_len(su_frame_len),
              d_tolerance(tolerance),
	      d_lookahead(lookahead)
    {
        message_port_register_out(pmt::intern("pu_frame_start"));
    }

    /*
     * Our virtual destructor.
     */
    frame_detection_f_impl::~frame_detection_f_impl()
    {
    }

    void
    frame_detection_f_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        for(int i=0; i<d_nchan; i++)
          ninput_items_required[i] = d_su_frame_len + 2 * d_tolerance + d_lookahead; // take multiples of the frame_len to reduce the processing load
    }
    
    bool
    frame_detection_f_impl::check_if_pu(float* ptr)
    {
        /* Sum the channel occupation values (1 or 0) for the lenght of a SU frame and some tolerance.
           If the result varies too much from the expectation, it's probably a PU frame or a result of interference.
           A requirement for this to work is of course that the frame lenghts differ enough.
        */
        int sum = 0;
        for(int i=0; i<d_su_frame_len+2*d_tolerance; i++){ sum += ptr[i]; }
        //std::cout << "sum: " << sum;
        if(sum >= d_su_frame_len-d_tolerance and sum <= d_su_frame_len+d_tolerance ) // SU frame
        {
            //std::cout << ", discard." << std::endl;
            return false;
        }
        else //  PU frame
        {
            //std::cout << ", propagate." << std::endl;
            return true;
        }
    }

    int
    frame_detection_f_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      float *in[d_nchan] = {(float *) input_items[0], (float *) input_items[1], (float *) input_items[2], (float *) input_items[3]};
      int *out[2] = {(int *) output_items[0], (int *) output_items[1]};
      int nitems_available_in = ninput_items[0];
      int nitems_available_out = noutput_items;
      int items_read = 0;
      int items_written = 0;
        
      /* 
      output_items[0]: frame start index
      output_items[1]: channel index
      */
      

        items_read = 0;
        while(items_read < nitems_available_in - 1 - d_su_frame_len - 2*d_tolerance and items_written < nitems_available_out)
        {    
            for(int i = 0; i < d_nchan; i++) // iterate sequentially over the channels
            {  
              if(in[i][items_read] == 0 and in[i][items_read+1] == 1)  // rising slope --> frame start
              {
                // check if the following frame is a PU frame based on its length            
                if(check_if_pu(&(in[i][items_read+1])))
                {
                    out[0][items_written] = nitems_read(i) + items_read + 1; // total sample index
                    out[1][items_written] = i;
                    //std::cout << "frame_detection: frame at " << out[0][items_written] << ", RT: " << boost::posix_time::microsec_clock::local_time().time_of_day().total_milliseconds() << std::endl;
                    message_port_pub(pmt::intern("pu_frame_start"), pmt::cons(pmt::from_long(out[0][items_written]), pmt::from_long(i)));
                    items_written++;
                }
              }
            }
            items_read++;
      }
                
      consume_each (items_read);
      return items_written;
    }

  } /* namespace classifier */
} /* namespace gr */

