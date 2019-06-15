import RPi.GPIO as GPIO
import time

def checkdist():
    GPIO.output(20,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(20,GPIO.LOW)
    while not GPIO.input(21):
        pass
    t1 = time.time()
    while GPIO.input(21):
        pass
    t2 = time.time()
    return (t2-t1)*340/2

GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(21,GPIO.IN)

time.sleep(2)

try:
    while True:
    	print 'Distance: %0.2f m' %checkdist()
    time.sleep(3)

except KeyboardInterrupt:
	GPIO.cleanup()
