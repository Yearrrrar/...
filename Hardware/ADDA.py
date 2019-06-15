#!/usr/bin/python
# -*- coding:utf-8 -*-
import smbus
import time

address = 0x49
VCC = 5.0
A0 = 0x41
A1 = 0x42
A2 = 0x43
A3 = 0x40

bus = smbus.SMBus(1)
while True:
    bus.write_byte(address,A0)
    v0 = bus.read_byte(address)
    print("AOUT:%1.3f  " %(v0*VCC/255)),

    bus.write_byte(address,A1)
    v1 = bus.read_byte(address)
    print("RES:%1.3f  " %(v1*VCC/255)),

    bus.write_byte(address,A2)
    v2 = bus.read_byte(address)
    print("TEMP:%1.3f  " %(v2*VCC/255)),

    bus.write_byte(address,A3)
    v3 = bus.read_byte(address)
    print("LUX:%1.3f  " %(v3*VCC/255)),

    bus.write_byte_data(address, 0x40, v1)
    print("LED:%1.3f  " %(v1*VCC/255))

    time.sleep(0.2)