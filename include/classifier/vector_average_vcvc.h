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


#ifndef INCLUDED_CLASSIFIER_VECTOR_AVERAGE_VCVC_H
#define INCLUDED_CLASSIFIER_VECTOR_AVERAGE_VCVC_H

#include <classifier/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace classifier {

    /*!
     * \brief <+description of block+>
     * \ingroup classifier
     *
     */
    class CLASSIFIER_API vector_average_vcvc : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<vector_average_vcvc> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of classifier::vector_average_vcvc.
       *
       * To avoid accidental use of raw pointers, classifier::vector_average_vcvc's
       * constructor is in a private implementation
       * class. classifier::vector_average_vcvc::make is the public interface for
       * creating new instances.
       * \param n_samples   number of vector samples to average
       * \param vlen        input vector lenght
       */
      static sptr make(int n_samples=1, size_t vlen=1);
    };

  } // namespace classifier
} // namespace gr

#endif /* INCLUDED_CLASSIFIER_VECTOR_AVERAGE_VCVC_H */

