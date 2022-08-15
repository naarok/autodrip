import time

import libioplus
import RPi.GPIO as GPIO

PUMP_POWER_RELAY=1
SOLENOID_START_RELAY=5

def setup(sim):
    global SIMULATE
    SIMULATE = sim

    if not SIMULATE:
        GPIO.setmode(GPIO.BCM)

def open_drip_line(sensor):
    print("Open Drip Line " + str(sensor+SOLENOID_START_RELAY))
    if not SIMULATE:
        libioplus.setRelayCh(0, sensor+SOLENOID_START_RELAY, 1)
        time.sleep(1)

def close_drip_line(sensor):
    print("Close Drip Line " + str(sensor+SOLENOID_START_RELAY))
    if not SIMULATE:
        libioplus.setRelayCh(0, sensor+SOLENOID_START_RELAY, 0)
        time.sleep(1)

def turn_pump_on():
    print("Turn Pump On")
    if not SIMULATE:
        libioplus.setRelayCh(0,PUMP_POWER_RELAY,1)
        time.sleep(3)

def turn_pump_off():
    print("Turn Pump Off")
    if not SIMULATE:
        libioplus.setRelayCh(0,PUMP_POWER_RELAY,0)
        time.sleep(1)

def water(moistures):
    open_drip_lines=[]
    for key,value in moistures.items():
        print(key, '->', value)

        if(key.startswith("w")):
            sensor = key[1]
            if(moistures["w"+sensor]):
                open_drip_line(int(sensor))
                open_drip_lines.append(int(sensor))

    turn_pump_on()
    time.sleep(15)

    for sensor in open_drip_lines:
        close_drip_line(sensor)

def test():
    import power12v

    try:
        power12v.setup(False)
        setup(False)

        power12v.turn_12v_on()

#        turn_pump_on()

        water({'any': True, 'm0': 2.6, 'w0': False, 'm1': 1.4, 'w1': True})

        turn_pump_off()
        time.sleep(2)
    finally:
        power12v.turn_12v_off()
        if not SIMULATE:
            GPIO.cleanup()
