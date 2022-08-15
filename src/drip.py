import RPi.GPIO as GPIO
import time
import libioplus
import random
import mqtt

ALL_YES=True
SIMULATE=False
PUBLISH_MQTT=False

POWER_ON_GPIO=20
SLEEP_TIME=15

NUM_SENSORS=2

SOLENOID_START_RELAY=5

MOISTURE_VCC_GPIO=21
MOISTURE_ADC=1

PUMP_POWER_RELAY=1

print("Drip")

print("Start")

def setup():
	if not SIMULATE:
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(MOISTURE_VCC_GPIO, GPIO.IN)
		GPIO.setup(POWER_ON_GPIO, GPIO.IN)

def check_water_level():
	if ALL_YES == True:
		return True

	result = input("Is water level good? ")
	if result == "Y":
		return True
	else:
		return False


# NOT USED
def is_dry(sensor):
	totally_dry = 1.3 #V
	ok_moist = 2.1 #V

	if ALL_YES == True:
		return True

	if not SIMULATE:
		GPIO.setup(MOISTURE_VCC_GPIO, GPIO.OUT)
		GPIO.output(MOISTURE_VCC_GPIO, GPIO.HIGH)
		time.sleep(1)
		value = libioplus.getAdcV(0, MOISTURE_ADC)		
		GPIO.output(MOISTURE_VCC_GPIO, GPIO.LOW)
		GPIO.setup(MOISTURE_VCC_GPIO, GPIO.IN)

		print("Drip value: "+str(value))
		return value < ok_moist

	result = input("Is dry? ")
	if result == "Y":
		return True
	else:
		return False

def check_all_moistures():
	totally_dry = 1.3 #V
	ok_moist = 2.1 #V

	results = {}
	results["any"] = False

	if not SIMULATE:
		GPIO.setup(MOISTURE_VCC_GPIO, GPIO.OUT)
		GPIO.output(MOISTURE_VCC_GPIO, GPIO.HIGH)
		time.sleep(1)

	for sensor in range(NUM_SENSORS):
		if not SIMULATE:
			value = libioplus.getAdcV(0, MOISTURE_ADC+sensor)		
		else:
			value = random.randint(13, 32)/10

		value = True

		results["m"+str(sensor)] = value
		results["w"+str(sensor)] = (value < ok_moist)
		results["any"] |= results["w"+str(sensor)]

	if not SIMULATE:
		GPIO.output(MOISTURE_VCC_GPIO, GPIO.LOW)
		GPIO.setup(MOISTURE_VCC_GPIO, GPIO.IN)

	return results

def open_drip_line(sensor):
	print("Open Drip Line " + str(sensor+SOLENOID_START_RELAY))
	if not SIMULATE:
		libioplus.setRelayCh(0, sensor+SOLENOID_START_RELAY, 1)

def close_drip_line(sensor):
	print("Close Drip Line " + str(sensor+SOLENOID_START_RELAY))
	if not SIMULATE:
		libioplus.setRelayCh(0, sensor+SOLENOID_START_RELAY, 0)

def turn_12v_on():
	print("Turn 12V on")
	if not SIMULATE:
		print("REALLY")
		GPIO.setup(POWER_ON_GPIO, GPIO.OUT)
		GPIO.output(POWER_ON_GPIO, GPIO.LOW)

def turn_12v_off():
	print("Turn 12V off")
	if not SIMULATE:
		GPIO.setup(POWER_ON_GPIO, GPIO.IN)

def turn_pump_on():
	print("Turn Pump On")
	if not SIMULATE:
	 	libioplus.setRelayCh(0,PUMP_POWER_RELAY,1)

def turn_pump_off():
	print("Turn Pump Off")
	if not SIMULATE:
	 	libioplus.setRelayCh(0,PUMP_POWER_RELAY,0)

def wait_water_time():
	print("Wait water time: " + str(SLEEP_TIME))
	time.sleep(SLEEP_TIME)

try:
	setup()

	water_level = check_water_level()

	success = False;
	moistures = check_all_moistures()
	moistures["timestamp"] = time.time()

	if water_level == True:
		print(moistures)

		if True: # moistures["any"]:
			# turn_12v_on()
			# time.sleep(1)

			turn_pump_on()
			time.sleep(1)

			for sensor in range(NUM_SENSORS):
				if moistures["w"+str(sensor)]:
					open_drip_line(sensor)
					time.sleep(0.5)

			wait_water_time()

			turn_pump_off()
			time.sleep(1)

			for sensor in range(NUM_SENSORS):
				close_drip_line(sensor)
				time.sleep(0.5)
	
		success = True

	# turn_12v_off()

finally:
	if PUBLISH_MQTT:
		del moistures["any"]
		pub = mqtt.MQTT()
		pub.publish(moistures)

	if not SIMULATE:
		GPIO.cleanup()

print("Done")
