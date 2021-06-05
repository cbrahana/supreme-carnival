# Config

# clockSpeeds in Hz, talk to me if you want to change these values, not all values will work
clockSpeeds = [10,20,40,50,80,100,160,200,250,320,400,500,800,1000,1600,2000,4000,8000]


# Everything below is mutable and precise values are up to Collin
azMotorCfg = {
    'PUL': 14,          # Broadcom pin number connected to PUL- on the stepper motor
    'DIR': 15,          # Broadcom pin number connected to DIR- on the stepper motor
    'PWMCLOCKS': clockSpeeds,
    'MCSTP': 400,       # Microstep stetting, pulses per revolution (400 minimum)
    'MXACC': 300,       # Max motor acceleration in degrees/sec^2.
    'MXSPD': 1800,      # Max motor rotation speed in degrees/sec. Will automatically 
                        # floor to an element of clockSpeeds / MCSTP * 360 (1800 recommended)
    }

altMotorCfg = {
    'PUL': 23,
    'DIR': 24,
    'PWMCLOCKS': clockSpeeds,
    'MCSTP': 400,
    'MXACC': 300,
    'MXSPD': 1800,
    }
