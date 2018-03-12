#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import re
import requests
import signal
import RPi.GPIO as GPIO
from picamera import PiCamera

# Set LED Pinouts
green = 18
red = 23
button = 17

# Set some GPIO stuff
GPIO.setmode(GPIO.BCM)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initial states for LEDs
GPIO.output(green, GPIO.HIGH)
GPIO.output(red, GPIO.LOW)

# Slack constants
token = os.environ.get('SLACK_API_TOKEN')

def shutter(button):
    print("Button pressed\n")
    camera = PiCamera()
    camera.resolution = (1920, 1080)
    GPIO.output(red, GPIO.HIGH)
    GPIO.output(green, GPIO.LOW)
    time.sleep(2)
    print("Taking picture\n")
    camera.capture('/home/april/gohan-time/images/oishii.jpg')
    camera.close()
    GPIO.output(red, GPIO.LOW)
    GPIO.output(green, GPIO.HIGH)
    post_image()
    return

def callback(button):
    print("CallbacK!")

def post_image():
    tasty_treat = {
            'file' : ('/home/april/gohan-time/images/oishii.jpg', open('/home/april/gohan-time/images/oishii.jpg', 'rb'), 'jpg')
            }
    payload={
            "filename":"oishii.jpg",
            "token":token,
            "channels":['#griz_test_chan'],
            }
    r = requests.post("https://slack.com/api/files.upload", params=payload, files=tasty_treat)
    print("Uploaded")
    print(r.status_code)
    return None

def handleSIG():
    GPIO.cleanup()
signal.signal(signal.SIGINT, handleSIG)

def cleanup():
    GPIO.cleanup()
    print("Cleaning up GPIO...sayonara.")

GPIO.add_event_detect(button, GPIO.RISING, callback=shutter, bouncetime=200)

while True:
    keypressed = raw_input('Press q to quit: ')
    if keypressed == 'q':
        cleanup()
        break
    else:
        print("idk")
