from datetime import datetime
import mqtt
import time

import dripLines
import moistureSensors
import power12v

import RPi.GPIO as GPIO

SIMULATE = False
PUBLISH_MQTT = True

WATER_ON_TIME = 15

POWER_12V_ON_GPIO=20

now = datetime.now()
current_time = now.strftime("%m/%d %H:%M:%S")

print("CronDrip: ", current_time)

def setup():
    if not SIMULATE:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(POWER_12V_ON_GPIO, GPIO.IN)

try:
    setup()
    power12v.setup(SIMULATE)
    power12v.turn_12v_on()

    moistureSensors.setup(SIMULATE)
    moistures = moistureSensors.check_all_moistures()
    print(moistures)
    # dripLines.water(moistures)
finally:
    if PUBLISH_MQTT:
        del moistures["any"]
        moistures["timestamp"] = time.time()
        PUB = mqtt.MQTT()
        PUB.publish(moistures)

    if not SIMULATE:
        power12v.turn_12v_off()
        GPIO.cleanup()


print("Done")
