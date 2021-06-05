import subprocess
init_pigpio = ["sudo", "pigpiod", "-t0"]
subprocess.Popen(init_pigpio, stdout = subprocess.PIPE, stderr = subprocess.DEVNULL)

import sys
sys.path.insert(0,"/home/pi/supreme_carnival")

import numpy as np
from Telescope import Telescope
import Pointing_Angle as pointer
from Pointing_Angle import getRA
from astropy.coordinates.name_resolve import NameResolveError

print("This script will attempt to calibrate the positioning of the telescope.")
print("You select a star to point at, and the telescope will try to point at that star.")
print("Then you provide a list of fine adjustments until the star is centered in the telescope's field of view")

t = Telescope(1,2)

name = input('Input name of celestial body to calibrate against: ')
while True:
    try:
        getRA(name)
        print("Located!")
        angle = pointer.calcAngle(name, t.LAT, t.LON, Telescope.getCurrentTime(), Telescope.getAltAngle(), Telescope.getAzAngle())
        check = True #t.checkConstraints(angle)
        if check:
            print("Star is within viewing constraints!")
            break
        else:
            print("That star exceeds the physical constraints of the Telescope")
            name = input("Please try again: ")
    except NameResolveError:
        print("Input name could not be resolved")
        name = input("Please try again: ")
        
print("Actuating to assumed position...")
t.actuate(angle)
print("Completed. Now we begin the calibration, you will be prompted for two fields, the azimuthal and altitudinal angle you want to calibrate by (positive or negative numbers correspond to different directions).")
print(f"You will continue to be prompted by these until you enter 0 into both fields, at this point, the telescope should be pointing directly at the body {name}")
print("Beginning calibration...")

calibrationAngle = Telescope.calibrationAngle
while True:
    try:
        azAngle = float(input("az: "))
        altAngle  = float(input("alt: "))
        if not (azAngle or altAngle):
            check = input("Are you sure you are done calibrating? [y/n]: ")
            if check =='y':
                break
            
        dAngle = np.array([altAngle, azAngle])
        calibrationAngle += dAngle
        t.actuate(dAngle)
    
    except:
        print("Error, please enter again")

Telescope.calibrationAngle = calibrationAngle
Telescope.currentAngle -= calibrationAngle
# This is a terrible calibration technique so far. Should need to be run every time the telescope is restarted

file = open('calibrationAngle.csv', 'w')
file.write(f"{calibrationAngle[0]},{calibrationAngle[1]}")
file.close()

print("Calibration complete")
t.shutdown()
