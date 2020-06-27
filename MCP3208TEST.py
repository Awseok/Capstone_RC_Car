from mcp3208 import MCP3208
import time

adc = MCP3208()

while True:
    
    for i in range(4):
        volts = adc.read(i) * (5/1024)
        
        try:
            distance = (61.573 * (volts)**-1.10) * 4
        except:
            distance = 0

        print('ADC[{}]: {:.2f}'.format(i, distance))
    time.sleep(1)