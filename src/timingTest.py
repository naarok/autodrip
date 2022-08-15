from croniter import croniter
from datetime import datetime

base = datetime.now()
iter = croniter('*/5 * * * *', base)  # every 5 minutes
next_time = iter.get_next(datetime)

delta = next_time-base

print("next minute in(s) " + str(delta.seconds))

def initialize_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#if __name__ == '__main__':
#    initialize_GPIO()

#    GPIO.add_event_detect(BUTTON_GPIO, GPIO.BOTH, 
#            callback=switch_callback, bouncetime=200) # debounce larger than sleep in callback
    
#    signal.signal(signal.SIGINT, signal_handler)
#    signal.signal(signal.SIGALRM, signal_alrm_handler)
#    signal.alarm(10)

#    signal.pause()