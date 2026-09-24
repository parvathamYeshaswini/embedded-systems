#!/usr/bin/python3
from __future__ import print_function, division
import serial
import time
import brickpi3

# --- BrickPi3 in COLOR mode ---
BP = brickpi3.BrickPi3()
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_COLOR_COLOR)
# COLOR IDs: 0=None, 1=Black, 2=Blue, 3=Green, 4=Yellow, 5=Red, 6=White, 7=Brown
color = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

# --- Serial / PRIZM ---
port = "/dev/ttyUSB0"   # change if needed
ser = serial.Serial(port, baudrate=9600, timeout=1)

def cmdSend(ser, cmd):
    ser.write((str(cmd) + "\n").encode("utf-8"))
    line = ser.readline()
    try:
        return line.decode("utf-8", errors="ignore").strip()
    except Exception:
        return ""

def get_color():
    try:
        return BP.get_sensor(BP.PORT_1)
    except brickpi3.SensorError:
        return 0  # None

# ---- handshake ----
print("*** Press the GREEN button to start the robot ***")
time.sleep(1.5)
while True:
    print("--- Sending out handshaking signal ---")
    if cmdSend(ser, 1):
        print("!!! Connected to the robot !!!")
        break
    print("*** Try again ***")
    time.sleep(0.2)

# ---- wait for RED start ----
while True:
    c = get_color()
    if c == 5:  # RED start
        print("!!! Start Point (RED) !!!")
        break
    time.sleep(0.05)

# ---- edge-follow params ----
SAMPLES_REQ = 2     # need 2 consecutive reads to switch action
DT          = 0.02  # 20ms sample
# Start by following the RIGHT edge; set to False to start on LEFT edge
FOLLOW_RIGHT_EDGE = True

last_action  = None
white_streak = 0
black_streak = 0
ok_streak    = 0
YELLOW_REQ   = 10  
yellow_streak = 0 
Red_streak = 0
Red_REQ= 10 
turn=0    

# ---- main loop ----
while True:
    c = get_color()

    # stop if we see RED again
#    if c == 5:
#        cmdSend(ser, 5)  # stop+blink
#        print("Reached RED again. Stopping.")
#        break

    # SIMPLE U-TURN ON YELLOW: spin left for 2 seconds,
    # then flip which edge we follow and continue


    # --- edge following using WHITE vs BLACK-ish (BLACK or NONE) ---
    is_white_like   = (c == 6)
    is_blackish     = (c == 1) or (c == 0)   # treat NONE as black side

    if is_white_like:
        white_streak += 1
        black_streak = 0
        ok_streak    = 0

        # Decide nudge direction based on which edge we're following
        # FOLLOW_RIGHT_EDGE=True  => WHITE -> nudge RIGHT (3)
        # FOLLOW_RIGHT_EDGE=False => WHITE -> nudge LEFT  (2)
        desired = 3 if FOLLOW_RIGHT_EDGE else 2
        if white_streak >= SAMPLES_REQ and last_action != desired:
            cmdSend(ser, desired)
            last_action = desired

    elif is_blackish:
        black_streak += 1
        white_streak = 0
        ok_streak    = 0

        # Opposite mapping for black side:
        # FOLLOW_RIGHT_EDGE=True  => BLACK-ish -> nudge LEFT  (2)
        # FOLLOW_RIGHT_EDGE=False => BLACK-ish -> nudge RIGHT (3)
        desired = 2 if FOLLOW_RIGHT_EDGE else 3
        if black_streak >= SAMPLES_REQ and last_action != desired:
            cmdSend(ser, desired)
            last_action = desired

    else:
        ok_streak += 1
        white_streak = 0
        black_streak = 0
        if ok_streak >= SAMPLES_REQ and last_action != 6:
            cmdSend(ser, 6)  # forward
            last_action = 6

    time.sleep(DT)
    
    
    if c == 4:
        yellow_streak += 1
    else:
        yellow_streak = 0

    if yellow_streak >= YELLOW_REQ:
      if turn ==0:
        print("YELLOW confirmed -> U-turn (cmd 7) & flip edge side")
        cmdSend(ser, 7)      # your U-turn command
        # Keep sleep only if case 7 doesn't manage timing itself:
        cmdSend(ser, 5)
        time.sleep(2.0)
        cmdSend(ser, 6)
        turn=1
        FOLLOW_RIGHT_EDGE = not FOLLOW_RIGHT_EDGE
        white_streak = black_streak = ok_streak = 0
        last_action = 6
        yellow_streak = 0     # reset after handling
        time.sleep(DT)
        continue
        
    if c == 5:
        Red_streak += 1
    else:
        Red_streak = 0

    if Red_streak >= Red_REQ:
      if turn ==1:
        print("RED confirmed. Stop!")
  
        cmdSend(ser, 5)

        break
    
    
