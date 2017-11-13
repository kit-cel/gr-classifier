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

#ifndef INCLUDED_CLASSIFIER_PACKET_SOURCE_IMPL_H
#define INCLUDED_CLASSIFIER_PACKET_SOURCE_IMPL_H
extern "C"{
#include "packetLib.h"
}
#include <classifier/packet_source.h>

namespace gr {
  namespace classifier {

    class packet_source_impl : public packet_source
    {
     private:
      // Nothing to declare in this block.
      char* d_address;
      uint16_t d_port;
      uint16_t d_pkt_len;
      int d_send_state;

     public:
      packet_source_impl(int send_state, const std::string& len_tag_key, char* address, uint16_t port, uint16_t pkt_len, uint8_t isTransmitter);
      ~packet_source_impl();
      spectrum* d_demoTx;
      char d_errorBuf[32];
      int d_currentstate;
      spectrum_eror_t d_retVal;
      uint8_t d_radionumber;
      //void set_state(int statenumber);
      int get_state(){return d_currentstate;}
      double get_throughput() { return spectrum_getThroughput(d_demoTx, 1, 1000); } //returns the throughput for the given radio
      double get_providedthroughput() { return spectrum_getProvidedThroughput(d_demoTx, 1, 1000); } //returns the provided throughput for the given radio
      double get_PU_throughput(){return spectrum_getThroughput(d_demoTx, 0, 1000);}
      double get_PU_providedthroughput(){return spectrum_getProvidedThroughput(d_demoTx, 0, 1000);}
      void report_scenario(pmt::pmt_t msg); // return scenario to the database

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_int &ninput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
      int calculate_output_stream_length(const gr_vector_int &ninput_items);
    };

  } // namespace classifier
} // namespace gr

#endif /* INCLUDED_CLASSIFIER_PACKET_SOURCE_IMPL_H */

