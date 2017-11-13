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


#ifndef INCLUDED_CLASSIFIER_COGNITIVE_ALLOCATOR_H
#define INCLUDED_CLASSIFIER_COGNITIVE_ALLOCATOR_H

#include <classifier/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace classifier {

    /*!
     * \brief Decides when and on which subchannel to send SU frames based on observation of PU frames and classification results
     * \ingroup classifier
     *
     */
    class CLASSIFIER_API cognitive_allocator : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<cognitive_allocator> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of classifier::cognitive_allocator.
       *
       * To avoid accidental use of raw pointers, classifier::cognitive_allocator's
       * constructor is in a private implementation
       * class. classifier::cognitive_allocator::make is the public interface for
       * creating new instances.
       */
      virtual void set_enable_tx(bool enable) = 0;
      virtual void set_always_send(bool always_send) = 0;
			virtual void set_aggro_mode(bool be_aggro) = 0;
      static sptr make(int su_frame_len, int pu_frame_len, int detection_rate, int baseband_rate, int nsamp_zeropadding, float delay_ms, bool enable_tx, int wait_time_unexpected_frame_ms);
    };

  } // namespace classifier
} // namespace gr

#endif /* INCLUDED_CLASSIFIER_COGNITIVE_ALLOCATOR_H */

