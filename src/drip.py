import RPi.GPIO as GPIO

POWER_ON_GPIO=23

print("Drip")

print("Start")

def setup():
	GPIO.setmode(GPIO.BCM)

def check_water_level():
	result = input("Is water level good? ")
	if result == "Y":
		return True
	else:
		return False


def has_more_sensors():
	result = input("Has more sensors? ")
	if result == "Y":
		return True
	else:
		return False

def get_next_sensor():
	pass

def check_moisture(sensor):
	result = input("Is dry? ")
	if result == "Y":
		return True
	else:
		return False

def open_drip_line():
	print("Open Drip Line")

def close_drip_line():
	print("CLose Drip Line")

def turn_12v_on():
	print("Turn 12V on")
	GPIO.setup(POWER_ON_GPIO, GPIO.OUT)
	GPIO.output(POWER_ON_GPIO, GPIO.LOW)

def turn_12v_off():
	print("Turn 12V off")
	GPIO.setup(POWER_ON_GPIO, GPIO.OUT)

def turn_pump_on():
	print("Turn Pump On")

def turn_pump_off():
	print("Turn Pump Off")

def wait_water_time():
	print("Wait water time")

setup()

water_level = check_water_level()

if water_level == True:
	more_sensors = has_more_sensors()

	if more_sensors == True:
		next_sensor = get_next_sensor()

		is_dry = check_moisture(next_sensor)

		if is_dry == True:
			open_drip_line()
			turn_12v_on()
			wait_water_time()
			close_drip_line()


turn_pump_off()
turn_12v_off()

print("Done")
