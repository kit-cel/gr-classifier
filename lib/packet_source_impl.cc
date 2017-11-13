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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#include <stdio.h>
#include <gnuradio/io_signature.h>
#include "packet_source_impl.h"
extern "C" {
#include "packetLib.h"
}

namespace gr {
  namespace classifier {

    packet_source::sptr
    packet_source::make(int send_state, const std::string& len_tag_key, char* address, uint16_t port, uint16_t pkt_len, uint8_t isTransmitter)
    {
      return gnuradio::get_initial_sptr
        (new packet_source_impl(send_state, len_tag_key, address, port, pkt_len, isTransmitter));
    }

    /*
     * The private constructor
     */
    packet_source_impl::packet_source_impl(int send_state, const std::string& len_tag_key, char* address, uint16_t port, uint16_t pkt_len, uint8_t isTransmitter)
      : gr::tagged_stream_block("packet_source",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(1, 1, sizeof(uint8_t)),
              len_tag_key
              )
    {
      d_address = address;
      d_port = port;
      d_pkt_len = pkt_len;
      d_send_state = send_state;
      d_currentstate = 0;

      char d_errorBuf[32];

      d_demoTx = spectrum_init(0);

      d_retVal = spectrum_connect(d_demoTx, d_address, d_port, d_pkt_len, isTransmitter);
      spectrum_errorToText(d_demoTx, d_retVal, d_errorBuf, sizeof(d_errorBuf));
      printf("TX connect: %s\n", d_errorBuf);
      if(d_retVal != ERROR_OK){
	      throw std::runtime_error("Connection refused");
      }

      d_retVal = spectrum_getRadioNumber(d_demoTx);
      spectrum_errorToText(d_demoTx, d_retVal, d_errorBuf, sizeof(d_errorBuf));
      printf("radio number: %s\n", d_errorBuf);
      d_radionumber = d_retVal;

      //printf("waitstate successful: %d\n", d_retVal > 0);
      //printf("new state: %d\n", d_currentstate);*/
      
      message_port_register_in(pmt::intern("scenario"));
      set_msg_handler(pmt::intern("scenario"), boost::bind(&packet_source_impl::report_scenario, this, _1));
      
      message_port_register_out(pmt::intern("enable_tx"));
    }

    /*
     * Our virtual destructor.
     */
    packet_source_impl::~packet_source_impl()
    {
      spectrum_delete(d_demoTx);
    }
    
    void
    packet_source_impl::report_scenario(pmt::pmt_t msg)
    {
      uint8_t scenario = (uint8_t) pmt::to_long(pmt::dict_ref(msg, pmt::intern("scenario_number"), pmt::PMT_NIL));
      if(scenario < 10) // only report valid scenarios
      {
        std::cout << "Scenario report: " << int(scenario) << std::endl;
        d_retVal = spectrum_reportScenario(d_demoTx, scenario);
        spectrum_errorToText(d_demoTx, d_retVal, d_errorBuf, sizeof(d_errorBuf));

        if(d_retVal != ERROR_OK){
	        std::cout << "Scenario could'nt be reported!" << std::endl;
        }
      }
    }

    int
    packet_source_impl::calculate_output_stream_length(const gr_vector_int &ninput_items) {

      return d_pkt_len;
    }

      /*void
      packet_source_impl::set_state(int statenumber) {
          std::cout << "packet_sink: Attempt state change from " << d_currentstate << " to " << statenumber << ": ";
          if (d_currentstate <= statenumber) {
              d_retVal = spectrum_waitForState(d_demoTx, statenumber, -1);
              spectrum_errorToText(d_demoTx, d_retVal, d_errorBuf, sizeof(d_errorBuf));             
              d_currentstate = statenumber;
              std::cout << "Success." << std::endl;
          } else { std::cout << "Failed." << std::endl; }
      }*/

    int
    packet_source_impl::work(int noutput_items,
        gr_vector_int &ninput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        if(d_currentstate < d_send_state)
        {
          if(spectrum_waitForState(d_demoTx, d_send_state, 0) == d_send_state) // start retrieving packets in next call to work()
          { 
            std::cout << "Send state (" << d_send_state << ") reached. Start requesting packets, enable transmitter." << std::endl;
            d_currentstate = d_send_state; 
            message_port_pub(pmt::intern("enable_tx"), pmt::PMT_T);
          }
          boost::this_thread::sleep(boost::posix_time::milliseconds(100));
          return 0;
        }
        else
        {
          uint8_t *out = (uint8_t*) output_items[0];

          // Do <+signal processing+>
          uint8_t buffer[d_pkt_len+1];
          spectrum_eror_t err = spectrum_getPacket(d_demoTx, buffer, sizeof(buffer), -1);
  //        spectrum_errorToText(d_demoTx, err, d_errorBuf, sizeof(d_errorBuf));
  //        printf("Get Packet: %s:\n",d_errorBuf);

          memcpy(out,buffer,d_pkt_len);
          // Tell runtime system how many output items we produced.
          return d_pkt_len;
        }
    }

  } /* namespace classifier */
} /* namespace gr */

