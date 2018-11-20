#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Contr�le d'un servomoteur avec un Raspberry Pi
Le programme demande � l'utilisateur d'entrer le rapport cyclique
(duty cycle) d�sir�, et le servomoteur se met � la position correspondante.
electroniqueamateur.blogspot.com
'''

import RPi.GPIO as GPIO

servo_pin = 21  # �quivalent de GPIO 18
     
GPIO.setmode(GPIO.BOARD)  # notation board plut�t que BCM

GPIO.setup(servo_pin, GPIO.OUT)  # pin configur�e en sortie

pwm = GPIO.PWM(servo_pin, 50)  # pwm � une fr�quence de 50 Hz

rapport = 2       # rapport cyclique initial de 7%

pwm.start(rapport)  

while True:
    print "Rapport cyclique actuel: " , rapport
    rapport = raw_input ("Rapport cyclique d�sir�:  ")
    pwm.ChangeDutyCycle(float(rapport))
