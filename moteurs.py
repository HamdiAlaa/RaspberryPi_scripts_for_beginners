import RPi.GPIO as gpio
import time

gpio.setwarnings(False)

gpio.setmode(gpio.BOARD)
gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)

gpio.output(7, True)
gpio.output(11, True)

while True:
        
        gpio.output(15, False)
        gpio.output(13, True)

            
