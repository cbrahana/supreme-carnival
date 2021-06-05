import subprocess
init_pigpio = ["sudo", "pigpiod", "-t0"]
subprocess.Popen(init_pigpio, stdout = subprocess.PIPE, stderr = subprocess.DEVNULL)

# Gets API to work nicely. This may need modification on your setup
import sys
sys.path.insert(0,"/home/pi/supreme_carnival/API")

print("Initializing...")
from Telescope import Telescope
from basicTrack import basicTrack as angleFunc
from Pointing_Angle import getRA
from astropy.coordinates.name_resolve import NameResolveError

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

trackParams = {
    'bodyName': name,
    'LAT': Telescope.getLAT,
    'LON': Telescope.getLON,
    'currentTimeDt': Telescope.getCurrentTime,
    'currentAngle': Telescope.getAngles
    }
try:
    trackTime = float(input("How long would you like to track for (seconds, 0 for infinite track)? "))
except ValueError:
    trackTime = 0

if trackTime == 0:
    trackTime = None

terminateType = telescope.activeTrack(angleFunc, 5, trackTime, **trackParams)

if terminateType:
    print("Tracking terminated (timeout)")
else:
    print("Tracking terminated (user interrupt)")

telescope.shutdown()
print('Shutdown')
