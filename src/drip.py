import RPi.GPIO as GPIO
import time
import libioplus

ALL_YES=True
SIMULATE=True

POWER_ON_GPIO=26
SLEEP_TIME=10

NUM_SENSORS=4
SENSOR_START_RELAY=1

PUMP_RELAY=5

MOISTURE_VCC_GPIO=21
MOISTURE_ADC=8

print("Drip")

print("Start")

def setup():
	if not SIMULATE:
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(MOISTURE_VCC_GPIO, GPIO.IN)

def check_water_level():
	if ALL_YES == True:
		return True

	result = input("Is water level good? ")
	if result == "Y":
		return True
	else:
		return False


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

def open_drip_line(sensor):
	print("Open Drip Line " + str(sensor+SENSOR_START_RELAY))
	if not SIMULATE:
		libioplus.setRelayCh(0, sensor+SENSOR_START_RELAY, 1)

def close_drip_line(sensor):
	print("Close Drip Line " + str(sensor+SENSOR_START_RELAY))
	if not SIMULATE:
		libioplus.setRelayCh(0, sensor+SENSOR_START_RELAY, 0)

def turn_12v_on():
	print("Turn 12V on")
	if not SIMULATE:
		GPIO.setup(POWER_ON_GPIO, GPIO.OUT)
		GPIO.output(POWER_ON_GPIO, GPIO.LOW)

def turn_12v_off():
	print("Turn 12V off")
	if not SIMULATE:
		GPIO.setup(POWER_ON_GPIO, GPIO.IN)

def turn_pump_on():
	print("Turn Pump On")
	if not SIMULATE:
	 	libioplus.setRelayCh(0,PUMP_RELAY,1)

def turn_pump_off():
	print("Turn Pump Off")
	if not SIMULATE:
	 	libioplus.setRelayCh(0,PUMP_RELAY,0)

def wait_water_time():
	print("Wait water time: " + str(SLEEP_TIME))
	time.sleep(SLEEP_TIME)

try:
	setup()

	water_level = check_water_level()

	if water_level == True:
		for sensor in range(NUM_SENSORS):
			needs_water = is_dry(sensor)

			print("Needs water: " +str(needs_water))
			if needs_water == True:
				turn_12v_on()
				open_drip_line(sensor)
				turn_pump_on()
				wait_water_time()
				close_drip_line(sensor)

	turn_pump_off()
	turn_12v_off()

finally:
	GPIO.cleanup()

print("Done")
