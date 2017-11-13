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
#include "energy_detection_vcf_impl.h"
#include <volk/volk.h>

namespace gr {
  namespace classifier {

    energy_detection_vcf::sptr
    energy_detection_vcf::make(int nfft, float threshold_delta_db)
    {
      return gnuradio::get_initial_sptr
        (new energy_detection_vcf_impl(nfft, threshold_delta_db));
    }

    /*
     * The private constructor
     */
    energy_detection_vcf_impl::energy_detection_vcf_impl(int nfft, float threshold_delta_db)
      : gr::sync_block("energy_detection_vcf",
              gr::io_signature::make(1, 1, sizeof(gr_complex)*nfft),
              gr::io_signature::make(2*d_nchan, 2*d_nchan, sizeof(float))),
	      d_nfft(nfft),
	      d_threshold_delta_db(threshold_delta_db),
	      d_nbins_subchan(nfft/d_nchan),
	      d_noisefloor(-1), // -1 signals that there is no prior estimation
	      d_noisefloor_db(0), // will be overwritten before first evaluation
	      d_avg_alpha(0.001)
    {
      if(nfft < 128)
      {
        std::cout << "WARNING: short FFT may lead to signal bandwidth leaking into noise observation interval!" << std::endl;
      }
      
      d_threshold_db = d_noisefloor_db + d_threshold_delta_db;
      
      d_magsquared.assign(d_nfft, 0);
      d_mean_power.assign(d_nchan, 0);
    }

    /*
     * Our virtual destructor.
     */
    energy_detection_vcf_impl::~energy_detection_vcf_impl()
    {
    }
    
    void
    energy_detection_vcf_impl::update_noisefloor()
    {
      // use the bin between the outer bands to estimate the noise floor.
      int left_band_gap_center = d_nfft/4;
      int right_band_gap_center = left_band_gap_center + d_nfft/2;
      int band_gap_indexes[2] = {left_band_gap_center, right_band_gap_center};
      float current_power = 0;
      for(int i=0; i<2; i++)
        current_power += d_magsquared[band_gap_indexes[i]];
      
      if(d_noisefloor < 0) // starting condition
      {
        d_noisefloor = current_power / 2;
      }
      else
      {
        d_noisefloor = d_noisefloor*(1-d_avg_alpha) + current_power / 2 * d_avg_alpha; // single-pole IIR for averaging, take number of bins into account
      }
      d_noisefloor_db = 10 * std::log10(d_noisefloor);            
    }

    int
    energy_detection_vcf_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      float* out[2*d_nchan];
      for(int i=0; i<2*d_nchan; i++)
      {
        out[i] = (float*) output_items[i];
      }
      
      for(int n = 0; n < noutput_items; n++)
      {
        // calculate magnitude squared input values
        //volk_32fc_magnitude_squared_32f(&d_magsquared[0], in + n * d_nfft, d_nfft);
        for(int i=0; i<d_nfft; i++)
          d_magsquared[i] = std::abs(in[n * d_nfft + i]) * std::abs(in[n * d_nfft + i]);
          
        update_noisefloor();
        d_threshold_db = d_noisefloor_db + d_threshold_delta_db;
        
        // sum the center half of each subchannel and convert to dB
        d_mean_power.assign(d_nchan, 0);
        for(int i=0; i<d_nchan; i++) 
        {
          //volk_32f_x2_add_32f(&d_mean_power[0]+i, &d_magsquared[0]+d_nbins_subchan/4+i*d_nbins_subchan, &d_magsquared[0]+d_nbins_subchan/2+i*d_nbins_subchan, d_nbins_subchan/4);
          for(int k=0; k<d_nbins_subchan/2; k++)
          {
            //std::cout << "i: " << i << "/" << d_nchan << ", k: " << k << "/" << d_nbins_subchan/2 << std::endl;
            d_mean_power[i] += d_magsquared[i*d_nbins_subchan+d_nbins_subchan/4+k];
          }
          d_mean_power[i] /= d_nbins_subchan/2; // take number of accumulated bins into account
          d_mean_power[i] = 10 * std::log10(d_mean_power[i]);
          out[i][n] = d_mean_power[i];
          if(out[i][n] > d_threshold_db)
          {
            out[i+d_nchan][n] = 1.0;
          }
          else
          {
            out[i+d_nchan][n] = 0.0;
          }
        } 
      }         
      
      //std::cout << std::endl;
      
      return noutput_items;
    }

  } /* namespace classifier */
} /* namespace gr */

