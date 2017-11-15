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

#ifndef INCLUDED_CLASSIFIER_ENERGY_DETECTION_VCF_IMPL_H
#define INCLUDED_CLASSIFIER_ENERGY_DETECTION_VCF_IMPL_H

#include <vector>
#include <classifier/energy_detection_vcf.h>
#include <boost/circular_buffer.hpp>

namespace gr {
  namespace classifier {

    class energy_detection_vcf_impl : public energy_detection_vcf
    {
     private:
      int d_nfft; // FFT length
      float d_threshold_db; // total threshold in dB
      float d_threshold_delta_db; // threshold over noise in dB
      static const int d_nchan = 4; // number of channels
      int d_nbins_subchan; // number of bins per subchannel
      std::vector<float> d_magsquared; // buffer for storing the magnitude squared input values
      std::vector<float> d_mean_power; // buffer for storing the mean power values per subchannel
      std::vector<float> d_max_mean_power; // buffer for storing the max mean power values per subchannel
      std::vector<boost::circular_buffer<float> > d_SNR_buffer;
      std::vector< boost::circular_buffer<float>::iterator > max_SNR;
      int d_buff_size; // Amount of FFT realizations in which the maximum SNR is to be held
      std::vector<float> d_SNR; // buffer for storing the max SNR per subchannel
      float d_noisefloor; // noisefloor (linear)
      float d_noisefloor_db; // noisefloor (dB)
      float d_avg_alpha; // single-pole IIR coefficient for averaging the noise floor

      void update_noisefloor();

     public:
      energy_detection_vcf_impl(int nfft, int buff_size, float threshold_delta_db);
      ~energy_detection_vcf_impl();

      virtual void set_threshold_delta_db(float threshold_delta_db){ d_threshold_delta_db = threshold_delta_db; }
      virtual float get_threshold_db(){ return d_threshold_db; }
      virtual float get_noisefloor_db(){ return d_noisefloor_db; }
      virtual float get_SNR_1(){ return d_SNR[0]; }
      virtual float get_SNR_2(){ return d_SNR[1]; }
      virtual float get_SNR_3(){ return d_SNR[2]; }
      virtual float get_SNR_4(){ return d_SNR[3]; }

      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace classifier
} // namespace gr

#endif /* INCLUDED_CLASSIFIER_ENERGY_DETECTION_VCF_IMPL_H */

