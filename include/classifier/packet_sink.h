/* -*- c++ -*- */
/* 
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
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


#ifndef INCLUDED_CLASSIFIER_PACKET_SINK_H
#define INCLUDED_CLASSIFIER_PACKET_SINK_H

#include <classifier/api.h>
#include <gnuradio/tagged_stream_block.h>

namespace gr {
  namespace classifier {

    /*!
     * \brief <+description of block+>
     * \ingroup classifier
     *
     */
    class CLASSIFIER_API packet_sink : virtual public tagged_stream_block
    {
     public:
      typedef boost::shared_ptr<packet_sink> sptr;
      virtual double get_throughput() = 0;
      virtual double get_providedthroughput() = 0;
      virtual double get_PU_throughput() = 0;
      virtual double get_PU_providedthroughput() = 0;
      //virtual void set_state(int statenumber) = 0;
      //virtual int get_state() = 0;
      /*!
       * \brief Return a shared_ptr to a new instance of classifier::packet_sink.
       *
       * To avoid accidental use of raw pointers, classifier::packet_sink's
       * constructor is in a private implementation
       * class. classifier::packet_sink::make is the public interface for
       * creating new instances.
       */
      static sptr make(const std::string& len_tag_key, char* address, uint16_t port, uint16_t pkt_len, uint8_t isTransmitter);
    };

  } // namespace classifier
} // namespace gr

#endif /* INCLUDED_CLASSIFIER_PACKET_SINK_H */

