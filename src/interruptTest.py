import libioplus
import RPi.GPIO as GPIO
import signal
import sys
import time
import threading

BUTTON_GPIO=25
POWER_ON_GPIO=26

SOLENOID_RELAY=5

NUM_SOLENOIDS=1

fan_on = threading.Event()
fan_on.clear()

def signal_handler(sig, frame):
	GPIO.cleanup()
	print("BuhBye")
	sys.exit(0)

def signal_alrm_handler(sig, frame):
	print("Alarm")
	signal.alarm(signal.SIGUSR1)
	signal.pause()

def turn_12v_on():
	fan_on.set()
	print("Turn 12V on: fan_on = " + str(fan_on.is_set()))

	GPIO.setup(POWER_ON_GPIO, GPIO.OUT)
	GPIO.output(POWER_ON_GPIO, GPIO.LOW)

def turn_12v_off():
	fan_on.clear()
	print("Turn 12V off: fan_on = " + str(fan_on.is_set()))
	GPIO.setup(POWER_ON_GPIO, GPIO.IN)

def open_drip_line(sensor):
	print("Open Drip Line " + str(sensor+SOLENOID_RELAY))
	libioplus.setRelayCh(0, sensor+SOLENOID_RELAY, 1)

def close_drip_line(sensor):
	print("Close Drip Line " + str(sensor+SOLENOID_RELAY))
	libioplus.setRelayCh(0, sensor+SOLENOID_RELAY, 0)

def switch_callback(channel):
	time.sleep(0.1) #need to wait a moment for switch to stablize

	if not GPIO.input(BUTTON_GPIO):
		print("Switch on!")
		turn_12v_on()
		time.sleep(1)

		for sensor in range(NUM_SOLENOIDS):
			open_drip_line(sensor)
			time.sleep(0.5)

	else:
		print("Switch off!")

		for sensor in range(NUM_SOLENOIDS):
			close_drip_line(sensor)
			time.sleep(0.5)
	
		time.sleep(1)
		turn_12v_off()

def test():
	print(fan_on)

if __name__ == '__main__':
	test()

	try:
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(BUTTON_GPIO, GPIO.BOTH, 
				callback=switch_callback, bouncetime=200) # debounce larger than sleep in callback
		
		signal.signal(signal.SIGINT, signal_handler)
		signal.signal(signal.SIGALRM, signal_alrm_handler)
		# signal.alarm(signal.SIGUSR1) # this is testing alarms

		signal.pause()
	finally:
		print("Doing cleanup")
		GPIO.cleanup()