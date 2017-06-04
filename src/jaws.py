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


open_port = BP.PORT_1
close_port = BP.PORT_2

#motors = BP.PORT_A + BP.PORT_D
motors = BP.PORT_B 
BP.set_motor_power(motors, 0)

open_speed = 20
close_speed = -50

BP.set_sensor_type(open_port, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(close_port, BP.SENSOR_TYPE.TOUCH)

try:
    print("Press a touch sensor to start jaws")
    open_value = 0
    close_value = 0
    while not (open_value + close_value):
        try:
            open_value = BP.get_sensor(open_port)
            close_value = BP.get_sensor(close_port)
        except brickpi3.SensorError:
            pass
    
    speed = 0
    while True:
        # BP.get_sensor retrieves a sensor value.
        # BP.PORT_1 specifies that we are looking for the value of sensor port 1.
        # BP.get_sensor returns the sensor value.
        try:
            open_value = BP.get_sensor(open_port)
            close_value = BP.get_sensor(close_port)
        except brickpi3.SensorError as error:
            print(error)
            value = 0
        
        if open_value:     
            speed = open_speed 
        elif close_value:
            speed = close_speed
        else:
            speed = 0
        
        BP.set_motor_power(motors, speed)
        
        try:
            # Each of the following BP.get_motor_encoder functions returns the encoder value (what we want to display).
            print("Encoder A: %6d  D: %6d" % (BP.get_motor_encoder(BP.PORT_A), BP.get_motor_encoder(BP.PORT_D)))
        except IOError as error:
            print(error)
        
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
