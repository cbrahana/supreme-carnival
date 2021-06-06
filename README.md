# Automatic Telescope Control
Welcome to the project page of the automatic pointing telescope. The goal of this project was to design, build, and program a computerized mounting system for a telescope that is free to rotate in all directions without the need for the user to physically intervene. Such a system is more accurate, less finicky, and able to view the night sky remotely, without constant user monitoring. This project required us to design the hardware necessary for a maneuverable yet precise mounting system, the electronics necessary to rotate a 5 kg telescope and mounting system with about 30 arcseconds of precision, as well as the software which controls the motors, calculation of required pointing angle, and the telescope as a whole.
<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/Telescope_Setup.jpg">

## Table of Contents
- [Components and Budget](#components-and-budget)
- [Design](#design)
  * [Mounting System](#mounting-system)
  * [Electronics](#electronics)
    + [Circuit Diagram](#circuit-diagram)
- [Code](#code)
  * [Pointing Angle Calculation](#pointing-angle-calculation)
    + [Star Database](#star-database)
  * [Motor Control](#motor-control)
  * [Telescope Control](#telescope-control)
    + [Tracking](#tracking)
    + [Calibration](#calibration)
- [Results](#results)
  * [Raw Images](#raw-images)
  * [Z-Scaled Images](#z-scaled-images)
- [Conclusion](#conclusion)
- [Contributors and Acknowldegements](#contributors-and-acknowldegements)


## Components and Budget
These are the electrical and mechanical parts that we used for this design. Many of the electrical parts could be substituted for parts with comparable specifications, but these are the ones we used for this design.

\# | Part | Subtotal ($)
---------|------|------
1 | ALITOVE 110VAC to 24VDC 10A Power Supply | 20.99
2 | DM542 Stepper Motor Controller | 45.98
2 | NEMA 23 Stepper Motor | 58.00
1 | Raspberry Pi 2B | —
1 | MH Level Converter | ~0.60
1 | Nexstar 127 SLT Telescope* | —
4 | Worm Gear Set 27:1 | 86.96
10| 1/4-inch Thrust Bearings |32.54
3 | 1/4-inch D-shaft, 12 in | 15.16

\* Optical part of the telescope only

— Part was on hand, no purchase necessary

Also used, from available resources:
~$20 PLA Printer Filament
~$2 assorted nuts, bolts
~$5 hollow curtain rod

Total Construction Cost, not counting unbilled resources: $260.23

Including a basic Raspberry Pi and the necessary mechanical parts, the total cost of this project comes out to $300.21 plus the cost of whatever optical telescope is chosen. For comparison, many similar commercial telescopes with these capabilities sell closer to the $500-$1500 range, though they usually also include the optical part of the telescope itself.

### Extra Parts
In the interest of full disclosure, we list here the parts that we bought but did not end up using, and the parts that we bought to facilitate remote work on this project (such as multiple Raspberry Pis so that each of us could test code on them individually)
\# | Part | Subtotal ($)
---------|------|------
2 | AS5048A 14-bit Rotary Encoder | 39.98
2 | Raspberry Pi 0W + Essential Peripherals | ~50.00
2 | AS5600 12-bit Rotary Encoder | ~20.00
2 | Diametric Magnets | 0.68

We did not have time to fully implement encoders, although much of the functionality for controlling the telescope using encoders exists within the code. The total cost of all parts purchased for this project was ~$370.

### Gearbox
We used stepper motors to actuate the telescope, and this meant that we needed a gearbox with a sufficiently high reduction ratio, low backlash, no backdriving, and low cost. There were no COTS systems that did this, so we designed our own. We chose worm gears as the internal reduction mechanism because they had low backlash, could not be backdriven, and could do better than the required 400:1 reduction ratio with only two gearing stages. A gearbox housing was designed to mount motors and hold shafts, and the gears were mounted in this housing with the assistance of several 3D-printed spacers. The design is demonstrated in the CAD files, and specifically in A001(long), where several unprintable parts were redesigned. A length of the shaft was left free, and custom mounting brackets were created to fit over the free shaft and glued in place. While this made the system difficult to redesign, it also made for a stable, effective telescope mounting system.

### Mounting System
In order to attach the gearbox subassembly to the ground, we decided to use a monopod, which had the advantage of causing no issues between a colliding telescope and a tripod leg. The exposed azimuthal shaft from the gearbox subassembly was placed into a mounting device that had been cutom printed. This technique was successful, but difficult to set up—the monopod was not suitably supported by the soil it was buried in relative to the cantilevered mass of the telescope, and so a system of clamps had to be devised. This system of clamps made retargeting difficult, but not impossible, and achieved satisfactory stability.


### Electronics
To control the telescope, we needed extremely precice yet powerful rotary motors—not necessarily fast motors. We settled on the use of stepper motors, which are ideal for these circumstances: they are not as fast as other types of motors, but the notion of discrete 'steps' means that the motor torque and precision were exactly what we need. To power the NEMA 23 motors we selected, however, required the purchase of two dedicated controllers, which could convert the logic signals from the RPi to 24V and up to 4A signals to the motors themselves. We settled on the DM542 controllers since we did not care about high microstepping fidelity (as microstepping decreases torque) and it met the requirements of our motors. The ALITOVE power supply was simply chosen because it was the cheapest available which could provide 24VDC power at up to 5A for each motor simultaneously. The choice of RPi was unimportant, in fact, we used many different RPis throughout the project. However, since the RPi only supplies 3.3V on its digital GPIO pins, and the controllers needed at least 3.5V to interpret the signals, we had to purchase a level converter, which would amplify the digital signals coming from the RPi so that they could be read by the controllers. We had attempted a solution involving a non-inverting amplifier using an op-amp, but this had issues at high frequencies, so we purchased dedicated logic converters which doubled the maximum rotation speed of the motors.

#### Circuit Diagram
The blue lines indicate wires that carry the PWM signal from the RPi to the controllers. Each pulse in the PWM signal is an instruction to step the motor once, so it was important that the PWM signal work at high frequencies so the motor would rotate fast, considering we were already stepping down the motor speed by a factor of 729 due to the precision gearing. The green lines indicate wires which carry the binary direction signal to the controllers so that we could rotate the motors in either direction. 

<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/Electronics_Schematic.png">

## Code
In order to facilitate the remote work environment of this project, it was necessary to make the software as user-friendly and modular as possible such that the integration of various parts went smoothly. Since this was almost a necessity anyway, one of our goals was to provide a highly modular and extensible yet user-friendly software to control the telescope. We will go into detail about the main elements pieces of our software below, each being largely independent of the others to allow for this modularity, yet all working together to provide telescope functionality.

### Pointing Angle Calculation
When trying to reference the position of a star in the sky, one potential way to do so is to say something like “It’s 20 degrees above the horizon and 30 degrees east of north.” This way of communicating star locations is very convenient since anybody standing around you should be able to easily find the star. Furthermore, it is easy to tell our telescope where to point, as we can easily determine where the telescope is currently pointing in many different ways.

However, this system of coordinates is not useful for much else. Because of the Earth’s rotation, stars appear to move in the sky. So the original description of the star’s location will (probably) not be valid after some time passes. Furthermore, the Earth is curved; if we wish to specify the location of the star to someone in a completely different place on Earth, this method will not work.

This is why the locations of objects are reported using a coordinate system called Right Ascension (RA), and Declination (DEC). Lines of RA and DEC are essentially lines of latitude and longitude, projected into space. This convention is useful because stars have a RA and DEC that are essentially fixed over a human lifespan. This means that if we specify the RA and DEC of an object, anyone, anywhere on Earth will (in principle) know exactly where in the sky the object is.

To convert from RA and DEC to an actual position in the sky, we need a few values. Besides the RA and DEC of the object, we need the position on Earth of the observer, given by their Latitude, and Longitude. We also need the date and the time. GPS functionality was partly introduced in the software to provide all of these values, however, in the interest of time, we instead chose to input the coordinates directly into the code for the final build. Given all of these values, we can compute the position of the object in the sky, at that time. The details of the calculation can be found <a href="http://www.stargazing.net/kepler/altaz.html"> here </a>.


#### Star Catalogue
Star catalogues are collections of objects in the sky, and some information about them.  Notably, they contain their RA and DEC.  So, our issue becomes querying a catalogue, to get the RA and DEC of our object of interest to feed into the calculations mentioned above. Luckily, there is a Python package called astropy that can do this for us.  It works by querying Sesame, which in turn queries three different star catalogues. This functionality is natively included in this system, but the catalogue we used only contains the locations of fixed stars and celestial bodies. However, it would be easy to implement support for satellites, in fact astropy has the capability to do this, but we chose not to in the interest of time.

### Motor Control
We wanted the motor control to be entirely self-contained, which makes it easier to debug code if the motors fail to run and allows for more freedom when it comes to pointing the telescope. The code uses the pigpio library, which is a 3rd party python library for Raspberry Pi which gives us control of key features of the Pi's hardware, such as its internal, hardware PWM clock. It is important that we use this hardware clock as opposed to the more common software PWM since python is notoriously bad at handling precision time measurements, which would result in erratic and unreliable PWM signals. The hardware clock, on the other hand, is extremely precise to within about a 1 microsecond. This means that we could very precisely control the amount of PWM signals outputted and, as each pulse is an instruction to step the motor once, this is crucial for precision control. The hardware clock does, however, come with the limitation that it can only operate at a few discrete frequencies, so we cannot continuously accelerate the motors as we could if using a software clock. The motor control therefore includes the ability to automatically generate the necessary acceleration curve, given the maximum acceleration, maximum speed, and list of available clock frequencies provided by the user. One example of the generated acceleration curve is shown below, the acceleration is linear, then peaks and holds that maximum speed, then it decreases linearly (or as linearly as possible given the available speeds).

<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/Accel_Curve_10_Revs.png" width=400><img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/Accel_Curve_100_Revs.png" width=400>

The maximum speed, maximum acceleration, and the available frequencies for each motor are all mutable by the user, providing them control of the telescope not achievable by many commercial equivalents. One major limitation of the motor software design is that multiple motors cannot be actuated simultaneously. This is a limitation of the pigpio library which could easily be fixed by purchasing an external clock or (painstakingly) fixed in software. Due to time constraints, none of these fixes were implemented here.

### Telescope Control
The telescope control builds upon the motor control though remains largely modular, if the user wants to switch out the motor control algorithms with an alternative design. It contains the core ability to target a location in the sky, either by feeding it the location directly or telling it to actuate by a certain amount. Some user-friendly functionalities include automatically checking any actuation instruction against a list of physical constraints on the motion of the telescope, which can be modified by the user depending on the constraints of their design. This would prevent the telescope from trying to point straight into the ground, for example, which could break certain assemblies. However, these constraints can be overcome if the user so chooses by interfacing directly with the motors. The telescope also contains automatic closed-loop error correction, so if the user implements encoders, the telescope will be able to check its accuracy in performing some rotation and will automatically correct for any errors. Finally, the telescope has support for tracking via a wide range of possible tracking functions and parameters. The user can pass in a function of their own creation which returns a location in the sky to track to given any number of parameters the user chooses. This could include hardware and software that is not even in the scope of this project, such as image recognition software, dynamic body selection, tracking of currently unsupported bodies, etc. There is also documentation provided on how one can go about writing their own tracking function.

#### Tracking
Along with the functionality to create one's own tracking function, a basic tracking function is built into the software, along with a script that can run it. This script simply checks against the database and calls on the angle calculation code to calculate where the telescope needs to point. The telescope code will run this function every few seconds to update its tracking position. This script was intended to be user-friendly, so it simply asks for the name of the body to be tracked and the duration of time to track for, there are no other parameters.

#### Calibration
Also provided is a calibration script, since we did not manage to get encoders working which would theoretically automatically calibrate the telescope. This calibration script allows the user to manually point the telescope at a selected star via a series of inputted instructions. The script then calibrates based on where the telescope thinks it is pointing, and where the user says it is pointing, to calibrate the telescope. This script also doubled for us as a way to precisely actuate the telescope to a given location—there were many occasions where the tracking function simply didn't work, and this function's manually inputted control ultimately allowed us to take many of the images that we did.

## Results
The final result is a functioning system that can position a telescope with high precision and remotely track stars to varying degrees of success. This project shows this can be built in 10 weeks. On top of that, our telescope can take high-quality images of stars. The images below are of Alpheratz and were taken with .1 sec of exposure, iso 1638.

### Raw Images
More images are available <a href="https://github.com/cbrahana/supreme-carnival/blob/main/images">here</a>, but here are some of the best ones, with the fewest visible artifacts.
<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/Raw1.JPG">
<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/Raw2.JPG">

### Z-Scaled Images
Due to the limited resolution of an iPhone camera, most stars observed will appear essentially black. In order to better view the dynamical range of stars captured by the image, an astronomical imaging technique known as z-scaling is used. This produced higher-quality images that better displayed the varying magnitudes of stars, even the dimmer stars.
<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/spacephoto3zscalecolor.jpeg">
<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/spacephoto4zscale.jpeg">
<img src="https://github.com/cbrahana/supreme-carnival/blob/main/images/spacephoto2zscalecolor.jpeg">

## Conclusion
What we proved with this project is that a functioning system that can position a telescope and track stars can be built within 10 weeks. However, the telescope design and functionality can be expanded in multiple ways. With simultaneous motor actuation, the positioning system can be more efficient in its turns and rotations. Also, with more time, we could improve on encoder functionality for this telescope system. With improvements in the design and software, this telescope could be able to more effectively track stars, track planets and satellites, and possibly even detect exoplanets through transits.

## Contributors and Acknowledgements
This project was made for the spring 2021 UCSB physics 15C/13CH lab class by Collin Brahana, Sam Crossley, Montu Ganesh, and Jack Grossman, under the observation of Dr. Andrew Jayich, and TAs Sean Buechele and Mingyu Fan.
