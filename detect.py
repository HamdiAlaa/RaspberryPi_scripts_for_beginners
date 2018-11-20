
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)   ##je prefere la numerotation BOARD plutot que BCM

Moteur1A = 16      ## premiere sortie du premier moteur, pin 16
Moteur1B = 18      ## deuxieme sortie de premier moteur, pin 18
Moteur1E = 22      ## enable du premier moteur, pin 22

Moteur2A = 19      ## premiere sortie du deuxieme moteur, pin 16
Moteur2B = 21      ## deuxieme sortie de deuxieme moteur, pin 18
Moteur2E = 23      ## enable du deuxieme moteur, pin 22

GPIO.setup(Moteur1A,GPIO.OUT)  ## ces 6 pins du Raspberry Pi sont des sorties
GPIO.setup(Moteur1B,GPIO.OUT)
GPIO.setup(Moteur1E,GPIO.OUT)
GPIO.setup(Moteur2A,GPIO.OUT) 
GPIO.setup(Moteur2B,GPIO.OUT)
GPIO.setup(Moteur2E,GPIO.OUT)

pwm1 = GPIO.PWM(Moteur1E,50)   ## pwm de la pin 22 a une frequence de 50 Hz
pwm1.start(100)   ## on commemnce avec un rapport cyclique de 100%

#pwm2 = GPIO.PWM(Moteur2E,50)   ## pwm de la pin 23 a une frequence de 50 Hz
#pwm2.start(20)   ## on commemnce avec un rapport cyclique de 100%

while True:
        GPIO.output(Moteur1A,GPIO.HIGH)
        GPIO.output(Moteur1B,GPIO.LOW)
        GPIO.output(Moteur1E,GPIO.HIGH)
        
        
print "Arret des moteurs"
GPIO.output(Moteur1E,GPIO.LOW)
GPIO.output(Moteur2E,GPIO.LOW)

pwm1.stop()    ## interruption du pwm
pwm2.stop()

GPIO.cleanup()


