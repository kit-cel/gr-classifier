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

#include <gnuradio/io_signature.h>
#include "burst_tagger_cc_impl.h"

namespace gr {
    namespace classifier {

        burst_tagger_cc::sptr
        burst_tagger_cc::make(int burst_len) {
            return gnuradio::get_initial_sptr
                    (new burst_tagger_cc_impl(burst_len));
        }

        /*
         * The private constructor
         */
        burst_tagger_cc_impl::burst_tagger_cc_impl(int burst_len)
                : gr::block("burst_tagger_cc",
                            gr::io_signature::make(1, 1, sizeof(gr_complex)),
                            gr::io_signature::make(1, 1, sizeof(gr_complex))),
                  d_burst_len(burst_len)
        {
            set_output_multiple(d_burst_len);
        }

        /*
         * Our virtual destructor.
         */
        burst_tagger_cc_impl::~burst_tagger_cc_impl() {
        }

        void
        burst_tagger_cc_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required) {
            ninput_items_required[0] = d_burst_len;
        }

        void
        burst_tagger_cc_impl::add_SOB()
        {
            static const pmt::pmt_t sob_key = pmt::string_to_symbol("tx_sob");
            static const pmt::pmt_t value = pmt::PMT_T;
            static const pmt::pmt_t srcid = pmt::string_to_symbol(alias());
            add_item_tag(0, nitems_written(0), sob_key, value, srcid);
        }

        void
        burst_tagger_cc_impl::add_EOB()
        {
            static const pmt::pmt_t eob_key = pmt::string_to_symbol("tx_eob");
            static const pmt::pmt_t value = pmt::PMT_T;
            static const pmt::pmt_t srcid = pmt::string_to_symbol(alias());
            add_item_tag(0, nitems_written(0)+d_burst_len-1, eob_key, value, srcid);
        }

        int
        burst_tagger_cc_impl::general_work(int noutput_items,
                                           gr_vector_int &ninput_items,
                                           gr_vector_const_void_star &input_items,
                                           gr_vector_void_star &output_items) {
            const gr_complex *in = (const gr_complex *) input_items[0];
            gr_complex *out = (gr_complex *) output_items[0];

            memcpy(out, in, d_burst_len * sizeof(gr_complex));
            add_SOB();
            add_EOB();
            consume_each(d_burst_len);
            return d_burst_len;
        }

    } /* namespace classifier */
} /* namespace gr */

