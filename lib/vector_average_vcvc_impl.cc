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
#include "vector_average_vcvc_impl.h"
#include <volk/volk.h>

namespace gr {
  namespace classifier {

    vector_average_vcvc::sptr
    vector_average_vcvc::make(int n_samples, size_t vlen)
    {
      return gnuradio::get_initial_sptr
        (new vector_average_vcvc_impl(n_samples, vlen));
    }

    /*
     * The private constructor
     */
    vector_average_vcvc_impl::vector_average_vcvc_impl(int n_samples, size_t vlen)
      : gr::block("vector_average_vcvc",
              gr::io_signature::make(1, 1, sizeof(float)*vlen),
              gr::io_signature::make(1, 1, sizeof(float)*vlen)),
        d_vlen(vlen), d_n_samples(n_samples)
    {
      average = new float[sizeof(float)*d_vlen]();
    }

    /*
     * Our virtual destructor.
     */
    vector_average_vcvc_impl::~vector_average_vcvc_impl()
    {
        delete[] average;
    }

    void
    vector_average_vcvc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        ninput_items_required[0] = d_n_samples * noutput_items;
    }

    int
    vector_average_vcvc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];

      for(unsigned int i = 0; i < d_n_samples; i++){
        volk_32f_x2_add_32f(average, &in[i*d_vlen], average, d_vlen * noutput_items);
      }

      volk_32f_s32f_multiply_32f(average, average, 1.0f/d_n_samples, d_vlen * noutput_items);
      for(unsigned int i = 0; i < d_vlen; i++){
          out[i] = average [i];
      }

      consume_each (d_n_samples * noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace classifier */
} /* namespace gr */

