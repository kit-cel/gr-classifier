/* -*- c++ -*- */
#include <stdint.h>

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
//typedef uint8_t packet[1489];

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#include <stdio.h>
#include <gnuradio/io_signature.h>
#include "packet_sink_impl.h"
extern "C" {
#include "packetLib.h"
}

namespace gr {
  namespace classifier {

    packet_sink::sptr
    packet_sink::make(const std::string& len_tag_key, char* address, uint16_t port, uint16_t pkt_len, uint8_t isTransmitter)
    {
      return gnuradio::get_initial_sptr
        (new packet_sink_impl(len_tag_key, address, port, pkt_len, isTransmitter));
    }

    /*
     * The private constructor
     */
    packet_sink_impl::packet_sink_impl(const std::string& len_tag_key, char* address, uint16_t port, uint16_t pkt_len, uint8_t isTransmitter)
      : gr::tagged_stream_block("packet_sink",
              gr::io_signature::make(1, 1, sizeof(uint8_t)),
              gr::io_signature::make(0, 0, 0),
              len_tag_key)
    {
      d_address = address;
      d_port = port;
      d_pkt_len = pkt_len;

      char d_errorBuf[32];

      d_demoRx = spectrum_init(0);

      d_retVal = spectrum_connect(d_demoRx, d_address, d_port, d_pkt_len, isTransmitter);
      spectrum_errorToText(d_demoRx, d_retVal, d_errorBuf, sizeof(d_errorBuf));
      printf("RX connect: %s\n", d_errorBuf);
      if(d_retVal != ERROR_OK){
	      throw std::runtime_error("Connection refused");
      }

      d_retVal = spectrum_getRadioNumber(d_demoRx);
      spectrum_errorToText(d_demoRx, d_retVal, d_errorBuf, sizeof(d_errorBuf));
      printf("#radio: %s\n", d_errorBuf);
      d_radionumber = d_retVal;

      d_currentstate = 0;

      //printf("waitstate successful: %d\n", d_retVal > 0);
      //printf("new state: %d\n", d_currentstate);

    }

    /*
     * Our virtual destructor.
     */
    packet_sink_impl::~packet_sink_impl()
    {
      spectrum_delete(d_demoRx);
    }

    int
    packet_sink_impl::calculate_output_stream_length(const gr_vector_int &ninput_items) {

        return d_pkt_len;

    }

    /*void
    packet_sink_impl::set_state(int statenumber) {
        std::cout << "packet_sink: Attempt state change from " << d_currentstate << " to " << statenumber << ": ";
        if (d_currentstate <= statenumber) {
            d_retVal = spectrum_waitForState(d_demoRx, statenumber, -1);
            spectrum_errorToText(d_demoRx, d_retVal, d_errorBuf, sizeof(d_errorBuf));
            d_currentstate = statenumber;
            std::cout << "Success." << std::endl;
        } else { std::cout << "Failed." << std::endl; }
    }*/

    int
    packet_sink_impl::work(int noutput_items,
        gr_vector_int &ninput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        const uint8_t *in = (const uint8_t *) input_items[0];

        d_retVal = spectrum_putPacket(d_demoRx, (uint8_t*)in, d_pkt_len);

        return d_pkt_len;
    }

  } /* namespace classifier */
} /* namespace gr */

