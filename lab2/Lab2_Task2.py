from __future__ import print_function  # python 3 style print in py2
from __future__ import division

import time
import brickpi3

BP = brickpi3.BrickPi3()  

# Configure sensors
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH)
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_COLOR_COLOR)

motor_on = False
count = 0
color = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

print("Single press = START, Double press = STOP")

try:
    while True:
        # --- check touch sensor ---
        try:
            value = BP.get_sensor(BP.PORT_2)
        except brickpi3.SensorError:
            value = 0

        if value == 1:
            count += 1

            if count % 3 == 1:   #
                motor_on = True
                print("Motors ON")
            elif count % 3 == 0: # 
                motor_on = False
                BP.set_motor_power(BP.PORT_B, 0)
                print("Motors OFF")

            # wait until released to avoid double-count
            while True:
                try:
                    if BP.get_sensor(BP.PORT_2) == 0:
                        break
                except brickpi3.SensorError:
                    pass
                time.sleep(0.05)

        # if ON, read color sensor and control motor 
        if motor_on:
            try:
                value1 = BP.get_sensor(BP.PORT_1)  
                if value1 == 2:        # Blue
                    BP.set_motor_power(BP.PORT_B, 50)
                elif value1 == 3:      # Green
                    BP.set_motor_power(BP.PORT_B, 100)
                elif value1 == 5:      # Red
                    BP.set_motor_power(BP.PORT_B, 0)
                else:
                    BP.set_motor_power(BP.PORT_B, 0)
            except brickpi3.SensorError as error:
                print(error)

        time.sleep(0.05)

except KeyboardInterrupt:
    BP.reset_all()
