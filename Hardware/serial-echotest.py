#!/usr/bin/python
# -*- coding:utf-8 -*-
import serial
import time

ser = serial.Serial("/dev/ttyS0", 9600)
print ser.portstr
def main():
    while True:
	ser.write("\x55")
	time.sleep(0.1)
        count = ser.inWaiting()
        if count != 0:
		value = ser.read(1)
		print("%#x" %ord(value))
        ser.flushInput()
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()