#importing modules

import cv2   
import numpy as np
import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)

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




def capteur():

        # Define GPIO to use on Pi
        gpio_TRIGGER = 3
        gpio_ECHO = 5

        # Set pins as output and input
        gpio.setup(gpio_TRIGGER,gpio.OUT)  # Trigger
        gpio.setup(gpio_ECHO,gpio.IN)      # Echo

        # Set trigger to False (Low)
        gpio.output(gpio_TRIGGER, False)


        # Allow module to settle
        time.sleep(0.5)

        # Send 10us pulse to trigger
        gpio.output(gpio_TRIGGER, True)
        time.sleep(0.00001)
        gpio.output(gpio_TRIGGER, False)
        start = time.time()
        while gpio.input(gpio_ECHO)==0:
          start = time.time()

        while gpio.input(gpio_ECHO)==1:
          stop = time.time()

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 00

        # That was the distance there and back so halve the value
        distance = distance / 2

        return distance


def couleur():
        
        while(1):
                 _, img = cap.read()
                                        
                #converting frame(img i.e BGR) to HSV (hue-saturation-value)

                hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

                #definig the range of red color
                red_lower=np.array([136,87,111],np.uint8)
                red_upper=np.array([180,255,255],np.uint8)


                #finding the range of red
                red=cv2.inRange(hsv, red_lower, red_upper)
                                
                #Morphological transformation, Dilation  	
                kernal = np.ones((5 ,5), "uint8")

                red=cv2.dilate(red, kernal)
                res=cv2.bitwise_and(img, img, mask = red)

                #Tracking the Red Color
                (_,contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                                
                for pic, contour in enumerate(contours):
                        area = cv2.contourArea(contour)
                                        
                               
                        if(area>500):
                                x,y,w,h = cv2.boundingRect(contour)	
                                img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                                cv2.putText(img,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
                                print "Couleur rouge dtecteeee"
                                cv2.imshow("Color Tracking",img)
                                print "Arret des moteurs 2"
                                gpio.output(Moteur1E,gpio.LOW)
                                gpio.output(Moteur2E,gpio.LOW)
                                                
                                pwm1 = gpio.PWM(Moteur1E,30)   ## pwm de la pin 22 a une frequence de 30 Hz
                                pwm2 = gpio.PWM(Moteur2E,30)   ## pwm de la pin 22 a une frequence de 30 Hz
                         
                                pwm1.stop()    ## interruption du pwm
                                pwm2.stop()    ## interruption du pwm
                                time.sleep(2)
                                break
                        else :
                                print "Arret des moteurs 3"
                                gpio.output(Moteur1E,gpio.LOW)
                                gpio.output(Moteur2E,gpio.LOW)
                                                
                                pwm1 = gpio.PWM(Moteur1E,30)   ## pwm de la pin 22 a une frequence de 30 Hz
                                pwm2 = gpio.PWM(Moteur2E,30)   ## pwm de la pin 22 a une frequence de 30 Hz
                         
                                pwm1.stop()    ## interruption du pwm
                                pwm2.stop()    ## interruption du pwm
                                time.sleep(1)
                                                                
                                                                        




def mon_main():
        #capturing video through webcam
        cap=cv2.VideoCapture(0)
        cap.set(3,320)
        cap.set(4,240)
                
        while True:
                
                d = capteur()
                
                if d < 15 :
                        print "Arret des moteurs 1"
                        gpio.output(Moteur1E,gpio.LOW)
                        gpio.output(Moteur2E,gpio.LOW)
                        
                        pwm1 = gpio.PWM(Moteur1E,30)   ## pwm de la pin 22 a une frequence de 30 Hz
                        pwm2 = gpio.PWM(Moteur2E,30)   ## pwm de la pin 22 a une frequence de 30 Hz
 
                        pwm1.stop()    ## interruption du pwm
                        pwm2.stop()    ## interruption du pwm
                        time.sleep(1)
                        
                        
                else :
                        print "moteurs tournent"
                        pwm1 = gpio.PWM(Moteur1E,30)   ## pwm de la pin 22 a une frequence de 30 Hz
                        pwm1.start(30) 

                        pwm2 = gpio.PWM(Moteur2E,30)   ## pwm de la pin 22 a une frequence de 30 Hz
                        pwm2.start(30)
                                                 
                        gpio.output(Moteur1A,gpio.LOW)
                        gpio.output(Moteur1B,gpio.HIGH)
                        gpio.output(Moteur1E,30)

                        gpio.output(Moteur2A,gpio.LOW)
                        gpio.output(Moteur2B,gpio.HIGH)
                        gpio.output(Moteur2E,30)

                        time.sleep(1)

               
        # Reset gpio settings
        gpio.cleanup() 
                        


mon_main()




