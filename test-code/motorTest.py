
import sys
sys.path.insert(0,"/home/pi/supreme_carnival/API")

import Motor
from Hardware_Config import azMotorCfg as az_cfg
from Hardware_Config import altMotorCfg as alt_cfg

az_motor = Motor.Motor(az_cfg)
alt_motor = Motor.Motor(alt_cfg)

az_motor.actuate(18000)
alt_motor.actuate(18000)

