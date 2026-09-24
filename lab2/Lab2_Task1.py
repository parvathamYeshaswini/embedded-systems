#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is an example for running all motors while a touch sensor connected to PORT_2 of the BrickPi3 is being pressed.
# 
# Hardware: Connect EV3 or NXT motor(s) to any of the BrickPi3 motor ports. Make sure that the BrickPi3 is running on a 9v power supply.
#
# Results:  When you run this program, the motor(s) speed will ramp up and down while the touch sensor is pressed. The position for each motor will be printed.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH)

motor_on = False  # state variable

print("Press touch sensor to toggle motors ON/OFF")

try:
    while True:
        try:
            value = BP.get_sensor(BP.PORT_2)
        except brickpi3.SensorError:
            value = 0

        if value == 1:
            motor_on = not motor_on  # toggle state

            if motor_on:
                print("Motors ON")
                print("Encoder  B: %6d  C: %6d " % (BP.get_motor_encoder(BP.PORT_B), BP.get_motor_encoder(BP.PORT_C)))
                BP.set_motor_power(BP.PORT_B + BP.PORT_C, 100)
            else:
                print("Motors OFF")
                print("Encoder  B: %6d  C: %6d " % (BP.get_motor_encoder(BP.PORT_B), BP.get_motor_encoder(BP.PORT_C)))
                BP.set_motor_power(BP.PORT_B + BP.PORT_C, 0)

            # wait until button is released to avoid double toggling
            while True:
                try:
                    if BP.get_sensor(BP.PORT_2) == 0:
                        break
                except brickpi3.SensorError:
                    pass
                time.sleep(0.05)

        time.sleep(0.05)

except KeyboardInterrupt:
    BP.reset_all()



'''
try:
    print("Press touch sensor on port 1 to run motors")
    value = 0
    while not value:
        try:
            value = BP.get_sensor(BP.PORT_2)
        except brickpi3.SensorError:
            pass
    
    speed = 0
    adder = 1
    while True:
        # BP.get_sensor retrieves a sensor value.
        # BP.PORT_2 specifies that we are looking for the value of sensor port 2.
        # BP.get_sensor returns the sensor value.
        try:
            
            value = BP.get_sensor(BP.PORT_2)
        except brickpi3.SensorError as error:
            print(error)
            value = 0
            speed=100
            
        speed = 0
        BP.set_motor_power(BP.PORT_B + BP.PORT_C, speed)
        time.sleep(2)
        
        if value == 1: 
            #time.sleep(2)
            if speed == 0:
              speed = 100
              while( True):
               BP.set_motor_power(BP.PORT_B + BP.PORT_C, speed)
               if (value==1):
                 break
                
             
            elif speed !=0:
              speed=0
              while( True):
               BP.set_motor_power(BP.PORT_B + BP.PORT_C, speed)
               if (value==1):
                 break 
                  
                

                                        # if the touch sensor is pressed
        #else:                                 # else the touch sensor is not pressed or not configured, so set the speed to 0
         #   speed = 0
          #  adder = 1
        
        # Set the motor speed for all four motors
        BP.set_motor_power(BP.PORT_B + BP.PORT_C, speed)
        
        try:
            # Each of the following BP.get_motor_encoder functions returns the encoder value (what we want to display).
            print("Encoder  B: %6d  C: %6d " % (BP.get_motor_encoder(BP.PORT_B), BP.get_motor_encoder(BP.PORT_C)))
        except IOError as error:
            print(error)
        
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.'''
