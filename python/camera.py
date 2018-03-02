#!/usr/bin/python

from picamera import PiCamera
from time import sleep

camera = PiCamera()


camera.start_preview()
sleep(3)
camera.capture('/home/april/gohan-time/images/image.jpg')
camera.stop_preview()
