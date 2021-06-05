#!/usr/bin/env python3
import Motor
from Hardware_Config import azMotorCfg as az_cfg
from Hardware_Config import altMotorCfg as alt_cfg

az_motor = Motor.Motor(az_cfg)
alt_motor = Motor.Motor(alt_cfg)

az_motor.actuate(36000)
alt_motor.actuate(-36000)
