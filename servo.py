#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Contrôle d'un servomoteur avec un Raspberry Pi
Le programme demande à l'utilisateur d'entrer le rapport cyclique
(duty cycle) désiré, et le servomoteur se met à la position correspondante.
electroniqueamateur.blogspot.com
'''

import RPi.GPIO as GPIO

servo_pin = 21  # équivalent de GPIO 18
     
GPIO.setmode(GPIO.BOARD)  # notation board plutôt que BCM

GPIO.setup(servo_pin, GPIO.OUT)  # pin configurée en sortie

pwm = GPIO.PWM(servo_pin, 50)  # pwm à une fréquence de 50 Hz

rapport = 2       # rapport cyclique initial de 7%

pwm.start(rapport)  

while True:
    print "Rapport cyclique actuel: " , rapport
    rapport = raw_input ("Rapport cyclique désiré:  ")
    pwm.ChangeDutyCycle(float(rapport))
