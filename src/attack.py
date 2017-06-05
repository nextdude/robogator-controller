# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is an example for running all motors while a touch sensor connected to PORT_1 of the BrickPi3 is being pressed.
# 
# Hardware: Connect EV3 or NXT motor(s) to any of the BrickPi3 motor ports. Make sure that the BrickPi3 is running on a 9v power supply.
#
# Results:  When you run this program, the motor(s) speed will ramp up and down while the touch sensor is pressed. The position for each motor will be printed.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.


sonic_port = BP.PORT_4
BP.set_sensor_type(sonic_port, BP.SENSOR_TYPE.NXT_ULTRASONIC)

legs = BP.PORT_A + BP.PORT_D
jaws = BP.PORT_B 
BP.set_motor_power(legs + jaws, 0)

walk_speed = -50 
close_speed = -50
open_speed = 20
jaw_time = 0
jaw_speed = 0
leg_speed = 0

try:
    while True:
        try:
            sonic_value = BP.get_sensor(sonic_port)
        except brickpi3.SensorError as error:
            print(error)
            sonic_value = 255

        if sonic_value > 62:     
            leg_speed = 0
            jaw_speed = 0
        elif sonic_value > 31:     
            leg_speed = walk_speed
            jaw_speed = 0
        else:
            leg_speed = 0
            now = time.time()
            if (now - jaw_time) > 1.0:
              jaw_speed = open_speed if jaw_speed < 0 else close_speed
              jaw_time = now

        BP.set_motor_power(legs, leg_speed)       
        BP.set_motor_power(jaws, jaw_speed)       
        print("dist={} (legs={}, jaws={})".format(sonic_value, leg_speed, jaw_speed))
        
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
