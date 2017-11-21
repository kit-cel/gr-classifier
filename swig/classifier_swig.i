/* -*- c++ -*- */

#define CLASSIFIER_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "classifier_swig_doc.i"

%{
#include "classifier/frame_detection_f.h"
#include "classifier/feature_extraction_f.h"
#include "classifier/cognitive_allocator.h"
#include "classifier/burst_tagger_cc.h"
#include "classifier/energy_detection_vcf.h"
#include "classifier/packet_source.h"
#include "classifier/packet_sink.h"
#include "classifier/vector_average_vcvc.h"
%}


%include "classifier/frame_detection_f.h"
GR_SWIG_BLOCK_MAGIC2(classifier, frame_detection_f);
%include "classifier/feature_extraction_f.h"
GR_SWIG_BLOCK_MAGIC2(classifier, feature_extraction_f);
%include "classifier/cognitive_allocator.h"
GR_SWIG_BLOCK_MAGIC2(classifier, cognitive_allocator);
%include "classifier/burst_tagger_cc.h"
GR_SWIG_BLOCK_MAGIC2(classifier, burst_tagger_cc);
%include "classifier/energy_detection_vcf.h"
GR_SWIG_BLOCK_MAGIC2(classifier, energy_detection_vcf);
%include "classifier/packet_source.h"
GR_SWIG_BLOCK_MAGIC2(classifier, packet_source);
%include "classifier/packet_sink.h"
GR_SWIG_BLOCK_MAGIC2(classifier, packet_sink);
%include "classifier/vector_average_vcvc.h"
GR_SWIG_BLOCK_MAGIC2(classifier, vector_average_vcvc);
