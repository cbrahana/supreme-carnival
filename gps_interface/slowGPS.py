#!/usr/bin/env python3
import socket
import pynmea2
import datetime
import threading
import time

class slowGPS:
    def __init__(self,IP_ADDRESS,PORT):
        self.IP_ADDRESS=IP_ADDRESS
        self.PORT=PORT
    
    def SG_check_GPS_connection(self):
        while True == True:
            print("IF INPUT IP/PORT INCORRECT, THIS WILL NEVER STOP.")
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.IP_ADDRESS,self.PORT))
            except:
                print("""Server not found. Waiting 5 seconds and trying again.""")
                time.sleep(5)
                continue
            break
        return 0
    
    def SG_getGPSlocationObject(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.IP_ADDRESS,self.PORT))
            s.recv(128)
            GPOTH = s.recv(512)
        
        print(GPOTH)
        gp1 = GPOTH.decode('ascii')
        gp2 = gp1.splitlines()
        gp3 = [i for i in gp2 if 'GPRMC' in i]
        return pynmea2.parse(gp3[0])
    
    def SG_getGPStimestamp(self):
        gps_obj = self.SG_getGPSlocationObject()
        return datetime.datetime.combine(gps_obj.datestamp,gps_obj.timestamp)
    
    def SG_getSingleGPSlocation(self):
        gps_obj = self.SG_getGPSlocationObject()
        return (gps_obj.latitude,gps_obj.longitude)
    
    def SG_generateAverageGPSlocation(self):
        t_list = []
        lat = 0.0
        lon = 0.0
        for _11 in range(60):
            t_list.append(self.SG_getSingleGPSlocation())
            time.sleep(1)
        for x in t_list:
            lat += x[0]
            lon += x[1]
        lat = lat/len(t_list)
        lon = lon/len(t_list)
        return (lat,lon)