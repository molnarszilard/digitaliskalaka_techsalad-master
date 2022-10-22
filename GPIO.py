import RPi.GPIO as GPIO
import time
# Pin Definitons:
white = 26 
green = 19 
red = 13 
yellow = 6 
blue = 5


# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(white, GPIO.OUT) # LED pin set as output
GPIO.setup(green, GPIO.OUT) # LED pin set as output
GPIO.setup(red, GPIO.OUT) # LED pin set as output
GPIO.setup(yellow, GPIO.OUT) # LED pin set as output
GPIO.setup(blue, GPIO.OUT) # LED pin set as output


# Initial state for LEDs:
GPIO.output(white, GPIO.HIGH)
GPIO.output(green, GPIO.HIGH)
GPIO.output(red, GPIO.HIGH)
GPIO.output(yellow, GPIO.HIGH)
GPIO.output(blue, GPIO.HIGH)

while(True):
    GPIO.output(white, GPIO.LOW)
    GPIO.output(green, GPIO.LOW)
    GPIO.output(red, GPIO.LOW)
    GPIO.output(yellow, GPIO.LOW)
    GPIO.output(blue, GPIO.LOW)
    time.sleep(1)
    GPIO.output(white, GPIO.HIGH)
    GPIO.output(green, GPIO.HIGH)
    GPIO.output(red, GPIO.HIGH)
    GPIO.output(yellow, GPIO.HIGH)
    GPIO.output(blue, GPIO.HIGH)
    time.sleep(1)



