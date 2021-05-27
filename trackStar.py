# To be tested on pi
# from subprocess import run
# rc = run("sudo pigpiod -t 0", shell=True)
# print(rc)

from Telescope import Telescope
from basicTrack import basicTrack as angleFunc
from Pointing_Angle import getRA
from astropy.coordinates.name_resolve import NameResolveError

print('Initializing...')

# Server IP and port placeholders
telescope = Telescope(1,1) 

name = input('Input name of celestial body to be tracked: ')
while True:
    try:
        getRA(name)
        print("Located!")
        break
    except NameResolveError:
        print("Input name could not be resolved")
        name = input("Please try again: ")

# Using datetime.now as a placeholder
trackParams = {
    'bodyName': name,
    'LAT': Telescope.getLAT,
    'LON': Telescope.getLON,
    'currentTimeDt': Telescope.getCurrentTime,
    'currentAngle': Telescope.getAngles
    }

trackTime = float(input("How long would you like to track for (seconds)? "))

terminateType = telescope.activeTrack(angleFunc, 5, trackTime, **trackParams)

if terminateType:
    print("Tracking terminated (timeout)")
else:
    print("Tracking terminated (user interrupt)")
    
telescope.shutdown()
print('Shutdown')