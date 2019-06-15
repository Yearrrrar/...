#encoding: utf-8
#!/usr/bin/env python
#This is a demo for security door. For more details, you can consult readme.docx

import os
import wave
import time
import cognitive_face as CF
import sys
from PIL import Image
import threading
import RPi.GPIO as GPIO
import struct
import sys
import pigpio
import requests
import json

#pin: the GPIO pin you choose
#times: times to blink
#delay: duration between blinking
def light(pin, times, delay):
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin,GPIO.OUT)
	onoff = GPIO.LOW
	
	i = 0
	while i < times:
		if onoff == GPIO.LOW:
			onoff = GPIO.HIGH
		else:
			onoff = GPIO.LOW
		GPIO.output(pin, onoff)
		time.sleep(delay)
		i += 1
	GPIO.output(pin, GPIO.LOW)

#if x^2 + y^2 + z^2 > threshold
#somebody knock the door
def knock(threshold):
	global buffer
	if sys.version > '3':
		buffer = memoryview
	BUS = 1
	ADXL345_I2C_ADDR = 0x53
	pi = pigpio.pi() # open local Pi
	h = pi.i2c_open(BUS, ADXL345_I2C_ADDR)
	if h >= 0: # Connected OK?
		# Initialise ADXL345.
		pi.i2c_write_byte_data(h, 0x2d, 0)  # POWER_CTL reset.
		pi.i2c_write_byte_data(h, 0x2d, 8)  # POWER_CTL measure.
		pi.i2c_write_byte_data(h, 0x31, 0)  # DATA_FORMAT reset.
		pi.i2c_write_byte_data(h, 0x31, 11) # DATA_FORMAT full res +/- 16g.
		read = 0
	#get initial pos
	(s, b) = pi.i2c_read_i2c_block_data(h, 0x32, 6)
	if s >= 0:
		(init_x,init_y,init_z) = struct.unpack('<3h', buffer(b))
	#loop until someone move the sensor
	while 1:
		(s, b) = pi.i2c_read_i2c_block_data(h, 0x32, 6)
		if s >= 0:
			(x,y,z) = struct.unpack('<3h', buffer(b))
		if (init_x - x)**2 + (init_y - y) ** 2 + (init_z - z) ** 2 >= threshold:
			break
		time.sleep(0.01)

#control the steering gear
def open_door():
	GPIO.setup(12,GPIO.OUT)
	p = GPIO.PWM(12,50)
	p.start(0)
	global onoff,dc, dir
	onoff = GPIO.LOW
	dc = 0
	dir = 5

	while 1:
		if dc > 125:
			dir = -5
		elif dc < 10:
			dir = 5
		dc = dc + dir
		p.ChangeDutyCycle( dc/10 )


def face_detect(face_image):
    key = 'twbFnRTexW-xeChmM-LkfDnaaOxSXeyI'
    secret = 'UKPzzg_FaKmXzU6QRZ6yA_pW1o_tNakD'
    cloud_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {
        'api_key': key,
        'api_secret': secret,
        'return_landmark': '0',
        'return_attributes': 'gender,age'
    }
    files = {'image_file': open(face_image, 'rb')}
    response = requests.post(cloud_url, data=data, files=files)
    return response

def face_compare(face_image):
    key = 'twbFnRTexW-xeChmM-LkfDnaaOxSXeyI'
    secret = 'UKPzzg_FaKmXzU6QRZ6yA_pW1o_tNakD'
    cloud_url = 'https://api-cn.faceplusplus.com/facepp/v3/compare'
    data = {
        'api_key': key,
        'api_secret': secret,
        'return_landmark': '0',
        'return_attributes': 'gender,age'
    }
    files = {'image_file1': open(face_image, 'rb'),
           'image_file2': open('myself.jpg', 'rb')
    }
    response = requests.post(cloud_url, data=data, files=files)
    return response



# Start from here.......
knock(1000)

print("Welcome to our security door!")
os.system('aplay -D sysdefault:CARD=1 welcome.wav')
print("Please say OPEN THE DOOR")

os.system('arecord --device=plughw:1,0 --format S16_LE --rate 16000 -d 5 -c1 oneOrTwo.wav&')#record one or two
#Countdown
light(11, 5, 1)
audioFile = "oneOrTwo.wav"

#analysis your recording
#r = sr.Recognizer()
#with sr.AudioFile(audioFile) as source:
#	audio = r.record(source) 
#
#speech_key = "34c7815245934e4a8e088956af4e62d7"  
#
#try:
#    speech_result = r.recognize_bing(audio, key=speech_key)
#    print(speech_result.encode("utf-8"))
#except sr.UnknownValueError:
#    print("Microsoft Bing Voice Recognition could not understand audio")
#except sr.RequestError as e:
#	print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

#if "open" in speech_result or "Open" in speech_result:
if 1:
	#Try to take a photo for you
	print("I will take a photo for you, please look at the camera:")
	time.sleep(2)
	os.system('sudo raspistill -o face_recognition.jpg -w 640 -h 480')
	res = face_detect("face_recognition.jpg")
        result = json.loads(res.text)
        print str(res.text)

	if len(result["faces"]) != 1:
		print("There is no face or more than one face in your photo!")

	else:
                res = face_compare("face_recognition.jpg")
                result = json.loads(res.text)
		confidence = result['confidence']
		print("Confidence： " + str(confidence))
		if confidence >= 70:
			print("Accept!")
			open_door()
		else:
			print("Permission Denied!")
