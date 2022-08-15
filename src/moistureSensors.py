import math
import random
import time

import RPi.GPIO as GPIO

import libioplus

NUM_ZONES = 2 #max 4

MOISTURE_VCC_GPIO = 21
MOISTURE_FIRST_ADC = 1

SIMULATE = False

#2.23v right after watering
#1.24v well in need of water


def setup(sim):
    global SIMULATE
    SIMULATE = sim

    if not SIMULATE:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MOISTURE_VCC_GPIO, GPIO.IN)

def check_one(sensor):
    sum = 0
    sumsq = 0
    n = 0

    for i in range(10):
        n += 1
        value = libioplus.getAdcV(0, MOISTURE_FIRST_ADC+sensor)

        print("s(" + str(n) + ") " + str(sensor) + ": " + str(value))

        sum += value
        sumsq += (value * value)

        mean = sum / n
        variance = (sumsq/n) - (mean * mean)
        time.sleep(1)

    print("s" + str(sensor) + ": " + str(round(mean,3)) + ", stdDev: " + str(round(math.sqrt(variance), 4)))

    return round(mean,3)

def check_all_moistures():
    totally_dry = 1.3 #V
    ok_moist = 2.1 #V

    results = {}
    results["any"] = False

    try:
        if not SIMULATE:
            GPIO.setup(MOISTURE_VCC_GPIO, GPIO.OUT)
            GPIO.output(MOISTURE_VCC_GPIO, GPIO.HIGH)
            time.sleep(1)

        for sensor in range(NUM_ZONES):
            if not SIMULATE:
                value = check_one(sensor)
            else:
                value = random.randint(13, 32)/10

            results["m"+str(sensor)] = value
            results["w"+str(sensor)] = (value < ok_moist)
            results["any"] |= results["w"+str(sensor)]

    finally:
        if not SIMULATE:
            GPIO.output(MOISTURE_VCC_GPIO, GPIO.LOW)
            GPIO.setup(MOISTURE_VCC_GPIO, GPIO.IN)

    print(results)

    return results

def test():
    import power12v

    try:
        power12v.setup(SIMULATE)
        setup(SIMULATE)

        power12v.turn_12v_on()

        check_all_moistures()
    finally:
        power12v.turn_12v_off()
        if not SIMULATE:
            GPIO.cleanup()


