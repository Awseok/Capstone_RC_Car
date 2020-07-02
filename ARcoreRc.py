"""
Consume LIDAR measurement file and create an image for display.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""
import os
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar

class ReadRplidar(object):
    
    def __init__(self):
        self.PORT_NAME = '/dev/ttyUSB0'
        self.lidar = RPLidar(None, self.PORT_NAME)
        self.max_distance = 0
        self.scan_data = [0]*360

    def process_data(self, data):
        max_distance = 0
        for angle in range(360):
            distance = data[angle]
            if distance > 0:                  
                max_distance = max([min([5000, distance]), max_distance])
                radians = angle * pi / 180.0
                x = distance * cos(radians) / 10
                y = distance * sin(radians) / 10
                
                if angle <= 30:
                    print('angle[{}], x=[{}], y=[{}], distance=[{}]'.format(angle, x, y, distance - 30))
                
    def close(self):
        self.lidar.stop()
        self.lidar.disconnect()
    
    def run(self):
        try:
            print(self.lidar.info)
            for scan in self.lidar.iter_scans():
                for (_, angle, distance) in scan:
                    self.scan_data[min([359, floor(angle)])] = distance
                self.process_data(self.scan_data)
                
        except KeyboardInterrupt:
            print("Stoping.")
            self.close()
            
            
if __name__ == '__main__':
    try:
        readLidar = ReadRplidar()
        print(readLidar.lidar.info)
        for scan in readLidar.lidar.iter_scans():
            for (_, angle, distance) in scan:
                readLidar.scan_data[min([359, floor(angle)])] = distance
            readLidar.process_data(readLidar.scan_data)
    
    except KeyboardInterrupt:
        print("Stoping.")
    readLidar.lidar.stop()
    readLidar.lidar.disconnect()
