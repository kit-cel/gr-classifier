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


#ifndef INCLUDED_CLASSIFIER_FRAME_DETECTION_F_H
#define INCLUDED_CLASSIFIER_FRAME_DETECTION_F_H

#include <classifier/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace classifier {

    /*!
     * \brief Detects PU frames and filters out SU frames.
     * \ingroup classifier
     *
     */
    class CLASSIFIER_API frame_detection_f : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<frame_detection_f> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of classifier::frame_detection_f.
       *
       * To avoid accidental use of raw pointers, classifier::frame_detection_f's
       * constructor is in a private implementation
       * class. classifier::frame_detection_f::make is the public interface for
       * creating new instances.
       */
      static sptr make(int su_frame_len, int tolerance, int lookahead);
    };

  } // namespace classifier
} // namespace gr

#endif /* INCLUDED_CLASSIFIER_FRAME_DETECTION_F_H */

