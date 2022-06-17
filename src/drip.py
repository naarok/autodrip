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

print("Drip")

print("Start")

def setup():
	if not SIMULATE:
		GPIO.setmode(GPIO.BCM)

def check_water_level():
	if ALL_YES == True:
		return True

	result = input("Is water level good? ")
	if result == "Y":
		return True
	else:
		return False


def check_moisture(sensor):
	if ALL_YES == True:
		return True

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

setup()

water_level = check_water_level()

if water_level == True:
	# more_sensors = has_more_sensors()

	# if more_sensors == True:
	for sensor in range(NUM_SENSORS):
		# next_sensor = get_next_sensor()

		is_dry = check_moisture(sensor)

		if is_dry == True:
			turn_12v_on()
			open_drip_line(sensor)
			turn_pump_on()
			wait_water_time()
			close_drip_line(sensor)


turn_pump_off()
turn_12v_off()

print("Done")
