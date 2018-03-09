import RPi.GPIO as GPIO
import time

# Set each LED to a GPIO pin
green = 18
red = 23
button = 17

# Pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initial state for LEDs:
GPIO.output(red, GPIO.LOW)
GPIO.output(green, GPIO.LOW)

def button_press():
    print("Let's try this out")
    try:
        while 1:
            if GPIO.input(button):
                GPIO.output(red, GPIO.LOW)
                GPIO.output(green, GPIO.HIGH)
            else:
                GPIO.output(red, GPIO.HIGH)
                GPIO.output(green, GPIO.LOW)
    except KeyboardInterrupt:
        GPIO.cleanup()

button_press()
