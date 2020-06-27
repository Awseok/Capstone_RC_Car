#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>

#define CS_MCP3208 8
#define SPI_CHANNEL 0
#define SPI_SPEED 1000000

int read_mcp3208_adc(unsigned char adcChannel)
{
	unsigned char buff[3];
	int adcValue = 0;
	
	buff[0] = 0x06 | ((adcChannel & 0x07) >> 2);
	buff[1] = ((adcChannel & 0x07) << 6);
	buff[2] = 0x00;
	
	digitalWrite(CS_MCP3208, 0);
	wiringPiSPIDataRW(SPI_CHANNEL, buff, 3);
	
	buff[1] = 0x0f & buff[1];
	adcValue = (buff[1] << 8) | buff[2];
	
	digitalWrite(CS_MCP3208, 1);
	
	return adcValue;
}


int main()
{
	unsigned char adcChannel_distance = 0;

	int adcValue_distance = 0;
	
	float vout_distance;
	float vout_oftemp;
	float percentrh = 0;
	float supsiondo = 0;
	
	printf("start");
	
	if(wiringPiSetupGpio() == -1)
	{
		fprintf(stdout, "Unable to start wiringPi :%s\n", strerror(errno));
		return 1;
	}
	
	if(wiringPiSPISetup(SPI_CHANNEL, SPI_SPEED) == -1)
	{
		fprintf(stdout, "wiringPiSPISetup Failed  :%s\n", strerror(errno));
		return 1;
	}
	pinMode(CS_MCP3208, OUTPUT);
	while(1)
	{
		adcValue_distance = read_mcp3208_adc(adcChannel_distance);
		printf("read =", adcValue_distance);
		delay(100);
	}
	return 0;
}

