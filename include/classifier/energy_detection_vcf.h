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


#ifndef INCLUDED_CLASSIFIER_ENERGY_DETECTION_VCF_H
#define INCLUDED_CLASSIFIER_ENERGY_DETECTION_VCF_H

#include <classifier/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace classifier {

    /*!
     * \brief <+description of block+>
     * \ingroup classifier
     *
     */
    class CLASSIFIER_API energy_detection_vcf : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<energy_detection_vcf> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of classifier::energy_detection_vcf.
       *
       * To avoid accidental use of raw pointers, classifier::energy_detection_vcf's
       * constructor is in a private implementation
       * class. classifier::energy_detection_vcf::make is the public interface for
       * creating new instances.
       */
      static sptr make(int nfft, int buff_size, float threshold_delta_db);
      virtual void set_threshold_delta_db(float threshold_delta_db) = 0;
      virtual float get_threshold_db() = 0;
      virtual float get_noisefloor_db() = 0;
      virtual float get_SNR_1() = 0;
      virtual float get_SNR_2() = 0;
      virtual float get_SNR_3() = 0;
      virtual float get_SNR_4() = 0;
    };

  } // namespace classifier
} // namespace gr

#endif /* INCLUDED_CLASSIFIER_ENERGY_DETECTION_VCF_H */

