## Controle de deux moteurs DC par le Raspberry Pi

import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BOARD)   ##je prefere la numerotation BOARD plutot que BCM

Moteur1A = 16      ## premiere sortie du premier moteur, pin 16
Moteur1B = 18      ## deuxieme sortie de premier moteur, pin 18
Moteur1E = 22      ## enable du premier moteur, pin 22

Moteur2A = 19      ## premiere sortie du deuxieme moteur, pin 16
Moteur2B = 21      ## deuxieme sortie de deuxieme moteur, pin 18
Moteur2E = 23      ## enable du deuxieme moteur, pin 22

gpio.setup(Moteur1A,gpio.OUT)  ## ces 6 pins du Raspberry Pi sont des sorties
gpio.setup(Moteur1B,gpio.OUT)
gpio.setup(Moteur1E,gpio.OUT)
gpio.setup(Moteur2A,gpio.OUT) 
gpio.setup(Moteur2B,gpio.OUT)
gpio.setup(Moteur2E,gpio.OUT)

pwm1 = gpio.PWM(Moteur1E,80)   ## pwm de la pin 22 a une frequence de 50 Hz
pwm1.start(76)   ## on commemnce avec un rapport cyclique de 100%

pwm2 = gpio.PWM(Moteur2E,100)   ## pwm de la pin 23 a une frequence de 50 Hz
pwm2.start(100)   ## on commemnce avec un rapport cyclique de 100%

print "Moteur 1 sens direct, rapide.  Moteur 2 sens direct, lent."

gpio.output(Moteur1A,gpio.LOW)
gpio.output(Moteur1B,gpio.HIGH)
gpio.output(Moteur1E,gpio.HIGH)

gpio.output(Moteur2A,gpio.HIGH)
gpio.output(Moteur2B,gpio.LOW)
gpio.output(Moteur2E,gpio.HIGH)

sleep(3)  ## on laisse tourner les moteur 5 secondes avec des parametres

print "Moteur 1 sens direct, lent.  Moteur 2 sens inverse, lent."

#pwm1.ChangeDutyCycle(20)  ## modification du rapport cyclique a 20%

#gpio.output(Moteur2A,gpio.LOW)
#gpio.output(Moteur2B,gpio.HIGH)

#sleep(2)

#print "Moteur 1 sens inverse, lent.  Moteur 2 sens inverse, rapide."

#pwm2.ChangeDutyCycle(100)  ## modification du rapport cyclique a 100%

#gpio.output(Moteur1A,gpio.LOW)
#gpio.output(Moteur1B,gpio.HIGH)


#sleep(5)


print "Arret des moteurs"
gpio.output(Moteur1E,gpio.LOW)
gpio.output(Moteur2E,gpio.LOW)

pwm1.stop()    ## interruption du pwm
pwm2.stop()

gpio.cleanup()

