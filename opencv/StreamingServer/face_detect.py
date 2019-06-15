# -*- coding: utf-8 -*-

import cv2
import sys
import numpy as np

cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

def encode(mat, ext):
	return cv2.imencode(ext, mat)[1]

def decode(binary_image):
	data = np.fromstring(binary_image, dtype=np.uint8)
	return cv2.imdecode(data, 1)

def detect(binary_image, ext):
	#return binary_image, False
	if len(binary_image)==0: return 0
	#print type(binary_image), len(binary_image), ext
	image = decode(binary_image)
	# print 'shit', type(image), len(image)
	#return encode(image, ext), False
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# Detect faces in the image
	faces = faceCascade.detectMultiScale(
	    gray,
	    scaleFactor=1.1,
	    minNeighbors=5,
	    minSize=(30, 30),
	    # flags = cv2.cv.CV_HAAR_SCALE_IMAGE
	)
	for (x, y, w, h) in faces:
	    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
	
	return len(faces)

if __name__ == '__main__':
	# Get user supplied values
	imagePath = sys.argv[1]
	file = open(imagePath, 'rb')
	data = file.read()
	file.close()
	image, find = detect(data, '.png')
	image = decode(image)
	cv2.namedWindow('Image')
	cv2.imshow('Image', image)
	cv2.waitKey(0)