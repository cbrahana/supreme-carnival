import numpy as np
import time #We're going to want to pull this from somewhere better than time? The GPS module, maybe? Otherwise, we're asking for trouble. We can keep the formatting, though. - CB
from Motor import Motor  
from Encoder import Encoder
from GPS_API import GPS #This may cause program to hang until GPS is found.

class Telescope():
    
    # Class variables, these are static variables just in case multiple instances of Telescope are created
    # Otherwise, we may have two instances of azMotor pointing to the same hardware, which would be very bad    
    
    azMotor = Motor()
    altMotor = Motor()
    azEncoder = Encoder()
    altEncoder = Encoder()
    targetAngle = np.array([])
    
    def __init__(self):
        initialAzAngle = self.getAzAngle()
        initialAltAngle = self.getAltAngle()
        initialAngle = np.array([initialAzAngle, initialAltAngle]) # This is a np array for better floating point handling, right? Are you sure we don't want to use arc-time for degree measurement? - CB
        Telescope.targetAngle = initialAngle
        
    
    def main(self):
        # Calls on the motors to rotate the telescope to point at the current Telescope.targetAngle
        # Will also include safety features like a constraint test to make sure the target angle is within hardware capabilities
        return
    
    
    def activeTrack(self, angleFunc, timeDelta=1, trackTime=None, *args):
        # Begins a loop over either a certain trackTime (float) or until user override (None)
        # Takes in a function angleFunc which must return the desired tracking angle as an ndArray in [az, alt] form and runs this angleFunc every timeDelta
        # This function then sets Telescope.targetAngle accordingly and runs self.main() to actuate the motors in the desired manner
        # The *args allow for runtime parameters to be passed into angleFunc (may need to change to *kwargs)
        return
    
        
    def setTarget(self, angle):
        # Sets a target angle
        return
    
    def getAngles(self):
        azAngle = self.getAzAngle()
        altAngle = self.getAltAngle()
        angle = np.array([azAngle, altAngle])
        return angle
    
    def getAzAngle(self):
        azAngle = Telescope.azEncoder.getAngle()
        return azAngle
        
    def getAltAngle(self):
        altAngle = Telescope.altEncoder.getAngle()
        return altAngle
    
    def calculateDeclination(latitude,altAngle,azAngle):
        declination = np.arcsin(np.sin(latitude)*np.sin(altAngle)+np.cos(latitude)*np.cos(altAngle)*np.cos(azAngle))
        return declination

    def calculateHourAngle(altAngle,latitude,declination,):
        hourAngle = np.arccos((np.sin(altAngle)-np.sin(latitude)*np.sin(declination)) / (np.cos(latitude)*np.cos(declination)))
        return hourAngle

    def calculateLocalSiderialTime():
        LST = hourAngle + rightAscension
        return LST