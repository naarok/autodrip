import RPi.GPIO as GPIO
import time
import libioplus

POWER_ON_GPIO=26
ALL_YES=True
NUMBER_SENSORS=1
SLEEP_TIME=10

current_sensor=1

print("Drip")

print("Start")

def setup():
	GPIO.setmode(GPIO.BCM)

def check_water_level():
	if ALL_YES == True:
		return True

	result = input("Is water level good? ")
	if result == "Y":
		return True
	else:
		return False


def has_more_sensors():
	if ALL_YES:
		if current_sensor <= NUMBER_SENSORS:
			return True

	result = input("Has more sensors? ")
	if result == "Y":
		return True
	else:
		return False

def get_next_sensor():
	pass

def check_moisture(sensor):
	if ALL_YES == True:
		return True

	result = input("Is dry? ")
	if result == "Y":
		return True
	else:
		return False

def open_drip_line():
	print("Open Drip Line")
	libioplus.setRelayCh(0, current_sensor+4, 1)

def close_drip_line():
	print("CLose Drip Line")
	libioplus.setRelayCh(0, current_sensor+4, 0)

def turn_12v_on():
	print("Turn 12V on")
	GPIO.setup(POWER_ON_GPIO, GPIO.OUT)
	GPIO.output(POWER_ON_GPIO, GPIO.LOW)

def turn_12v_off():
	print("Turn 12V off")
	GPIO.setup(POWER_ON_GPIO, GPIO.IN)

def turn_pump_on():
	print("Turn Pump On")

def turn_pump_off():
	print("Turn Pump Off")

def wait_water_time():
	print("Wait water time")
	time.sleep(SLEEP_TIME)

setup()

water_level = check_water_level()

if water_level == True:
	more_sensors = has_more_sensors()

	if more_sensors == True:
		next_sensor = get_next_sensor()

		is_dry = check_moisture(next_sensor)

		if is_dry == True:
			turn_12v_on()
			open_drip_line()
			wait_water_time()
			close_drip_line()


#turn_pump_off()
turn_12v_off()

print("Done")
