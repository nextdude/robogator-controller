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

left_touch = BP.PORT_1
right_touch = BP.PORT_2

left_leg = BP.PORT_A
right_leg = BP.PORT_D
BP.set_motor_power(left_leg + right_leg, 0)

normal_speed = -50
faster_speed = -normal_speed

BP.set_sensor_type(left_touch, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(right_touch, BP.SENSOR_TYPE.TOUCH)

try:
    print("Press touch sensors to start")
    left_click = 0
    right_click = 0
    while not left_click + right_click:
        try:
            left_click = BP.get_sensor(left_touch)
            right_click = BP.get_sensor(right_touch)
        except brickpi3.SensorError:
            pass
    
    speed = 0
    while True:
        try:
            left_click = BP.get_sensor(left_touch)
            right_click = BP.get_sensor(right_touch)
        except brickpi3.SensorError as error:
            print(error)
            left_click = 0
            right_click = 0
        
        if left_click and right_click:
            left_speed = normal_speed
            right_speed = normal_speed
        elif left_click and not right_click:
            left_speed = faster_speed
            right_speed = normal_speed
        elif right_click and not left_click:
            left_speed = normal_speed
            right_speed = faster_speed
        else:
            left_speed = 0
            right_speed = 0
        
        BP.set_motor_power(left_leg, left_speed)
        BP.set_motor_power(right_leg, right_speed)
        
        try:
            # Each of the following BP.get_motor_encoder functions returns the encoder value (what we want to display).
            print("Encoder A: %6d  D: %6d" % (BP.get_motor_encoder(BP.PORT_A), BP.get_motor_encoder(BP.PORT_D)))
        except IOError as error:
            print(error)
        
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
