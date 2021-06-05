#!/usr/bin/env python3
import socket
import pynmea2
import datetime
import threading
import time

IP_ADDRESS = '192.168.1.155'
PORT = 2947

def getGPSlocationObjectSlow(IP_ADDRESS,PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP_ADDRESS,PORT))
        s.recv(128) # Precision values, not very useful
        GPOTH = s.recv(512) # Satelite info, useful posistion info in GPGGA
    # The socket should ideally close here, but we don't care either way.
    gp_hld = GPOTH.decode('ascii')
    gp1_hld = gp_hld.splitlines()
    gp2_hld = [i for i in gp1_hld if 'GPGGA' in i]
    return pynmea2.parse(gp2_hld[0])

def getGPSlocationObjectThreaded(IP_ADDRESS,PORT):
    x = threading.Thread(target=getGPSlocationObjectSlow, args = (IP_ADDRESS,PORT))
    x.start()

def getGPStimestamp(IP_ADDRESS, PORT):
    gps_obj = getGPSlocationObjectThreaded(IP_ADDRESS, PORT)
    #return datetime.datetime.combine(datetime.today(),gps_obj.timestamp)
    return gps_obj.timestamp
    
def getSingleGPSlocation(IP_ADDRESS, PORT):
    gps_obj = getGPSlocationObjectThreaded(IP_ADDRESS, PORT)
    return (gps_obj.latitude,gps_obj.longitude)

def getAverageGPSlocation(IP_ADDRESS,PORT):
    pass

def gAGPSlSLOW(IP_ADDRESS,PORT):
    pass

print(getGPSlocationObjectSlow(IP_ADDRESS, PORT))
