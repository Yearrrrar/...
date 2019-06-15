import RPi.GPIO as GPIO
import time

def checkdist1():
    GPIO.output(16,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(16,GPIO.LOW)
    while not GPIO.input(18):
        pass
    t1 = time.time()
    while GPIO.input(18):
        pass
    t2 = time.time()
    return (t2-t1)*340/2

def checkdist2():
    GPIO.output(31,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(31,GPIO.LOW)
    while not GPIO.input(33):
        pass
    t1 = time.time()
    while GPIO.input(33):
        pass
    t2 = time.time()
    return (t2-t1)*340/2

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(18,GPIO.IN)
GPIO.setup(31,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(33,GPIO.IN)

time.sleep(2)

try:
    while True:
    	print 'Distance: %0.2f m' %checkdist1()
    	print 'Distance          : %0.2f m' %checkdist2()
    	time.sleep(0.5)

except KeyboardInterrupt:
	GPIO.cleanup()
