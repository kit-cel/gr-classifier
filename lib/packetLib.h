#ifndef SPECTRUM_H_
#define SPECTRUM_H_

#include <stdint.h>

#define NUM_ELEMENTS_BASE 1000
#define NUM_BUFFERS 10

typedef void spectrum;

typedef enum {ERROR_OK=0, ERROR_INVALID=-1, ERROR_AUTH=-2,
                ERROR_TIMEOUT=-3, ERROR_CONNECT_REFUSED=-4,
                ERROR_OTHER=-5, ERROR_BUF=-6} spectrum_eror_t;

spectrum* spectrum_init(char debug);
void spectrum_delete(spectrum* ctx);
spectrum_eror_t spectrum_getRadioNumber(spectrum* ctx);
spectrum_eror_t spectrum_connect(spectrum* ctx, char* hostname, uint16_t port, uint16_t requestedPacketLen, uint8_t isTransmitter);
void spectrum_errorToText(spectrum* ctx, spectrum_eror_t error, char* output, uint32_t len);
spectrum_eror_t spectrum_getPacket(spectrum* ctx, uint8_t* buffer, uint32_t bufferLength, int32_t timeoutMs);
spectrum_eror_t spectrum_putPacket(spectrum* ctx, uint8_t* buffer, uint32_t bufferLength);
spectrum_eror_t spectrum_waitForState(spectrum* ctx, uint32_t wantedState, int32_t timeoutMs);
double spectrum_getThroughput(spectrum* ctx, uint8_t radioNumber, int durationMs);
double spectrum_getProvidedThroughput(spectrum* ctx, uint8_t radioNumber, int durationMs);
spectrum_eror_t spectrum_reportScenario(spectrum* ctx, uint8_t scenario);

void spectrum_getStatusMessage(spectrum* ctx, spectrum_eror_t error, char* output, uint32_t len);
uint64_t spectrum_getTotalBytes(spectrum* ctx, uint8_t radioNumber);
uint64_t spectrum_getTotalProvidedBytes(spectrum* ctx, uint8_t radioNumber);

#endif /* SPECTRUM_H_ */
