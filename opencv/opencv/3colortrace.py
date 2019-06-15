from collections import deque
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

red1 = np.array([170, 100, 100])  
red2 = np.array([179, 255, 255]) 

mybuffer = 64  
pts = deque(maxlen=mybuffer)
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32

rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(1)

for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = image.array
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, red1, red2)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  
    center = None  

    if len(cnts) > 0:
        c = max(cnts, key = cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        if radius > 10:  
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2) 
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)

    for i in xrange(1, len(pts)):  
        if pts[i - 1] is None or pts[i] is None:  
            continue
        thickness = int(np.sqrt(mybuffer / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break