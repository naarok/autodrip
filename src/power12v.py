import time

import RPi.GPIO as GPIO

POWER_12V_ON_GPIO=20

def setup(sim):
    global SIMULATE
    SIMULATE = sim

    if not SIMULATE:
        GPIO.setmode(GPIO.BCM)

def turn_12v_on():
    print("Turn 12V on")
    if not SIMULATE:
        print("REALLY")
        GPIO.setup(POWER_12V_ON_GPIO, GPIO.OUT, initial = GPIO.LOW)
        time.sleep(5)

def turn_12v_off():
    print("Turn 12V off")
    if not SIMULATE:
        GPIO.setup(POWER_12V_ON_GPIO, GPIO.IN)

def test():
    try:
        setup(False)

        turn_12v_on()

        time.sleep(30)
    finally:
        turn_12v_off()
        if not SIMULATE:
            GPIO.cleanup()
