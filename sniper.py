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
        distance = elapsed * 34000

        # That was the distance there and back so halve the value
        distance = distance / 2
        print "Distance : %.1f" % distance

        return distance

pwm1 = gpio.PWM(Moteur1E,100)   ## pwm de la pin 22 a une frequence de 100 Hz
pwm2 = gpio.PWM(Moteur2E,100)   ## pwm de la pin 22 a une frequence de 100 Hz
#capturing video through webcam
cap=cv2.VideoCapture(0)
cap.set(3,240)
cap.set(4,240)

         
while True :


                #time.sleep(1)
                print "moteurs tournent"
                
                pwm1.start(100)
                pwm2.start(100)
                
                gpio.output(Moteur1A,gpio.HIGH)
                gpio.output(Moteur1B,gpio.LOW)
                gpio.output(Moteur1E,100)

                gpio.output(Moteur2A,gpio.HIGH)
                gpio.output(Moteur2B,gpio.LOW)
                gpio.output(Moteur2E,100)
                d = capteur()
                r=0
                while d < 40 and r==0:
                        print "Arret des moteurs 1"
                        gpio.output(Moteur1E,gpio.LOW)
                        gpio.output(Moteur2E,gpio.LOW)
                        

                        
                        pwm1 = gpio.PWM(Moteur1E,100)   ## pwm de la pin 22 a une frequence de 100 Hz
                        pwm2 = gpio.PWM(Moteur2E,100)   ## pwm de la pin 22 a une frequence de 100 Hz
 
                        pwm1.stop()    ## interruption du pwm
                        pwm2.stop()    ## interruption du pwm

                        #time.sleep(0.5)        
                        _, img = cap.read()
                                
                        #converting frame(img i.e BGR) to HSV (hue-saturation-value)

                        hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

                        #definig the range of red color
                        red_lower=np.array([136,87,111],np.uint8)
                        red_upper=np.array([180,255,255],np.uint8)

                        #finding the range of red,blue and yellow color in the image
                        red=cv2.inRange(hsv, red_lower, red_upper)
                     
                        #Morphological transformation, Dilation  	
                        kernal = np.ones((5 ,5), "uint8")

                        red=cv2.dilate(red, kernal)
                        res=cv2.bitwise_and(img, img, mask = red)


                        #Tracking the Red Color
                        (_,contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                       
                        nbr=0
                        for pic, contour in enumerate(contours) :
                                area = cv2.contourArea(contour)
                                
                                nbr+=1
                                
                                if (nbr>100):
                                        print "nbr = %.1f" %nbr
                                        nbr=0
                                        
                                        break 
                                
                                if(area>500):
                                        r+=1
                                        
                                        print "r : %.1f" % r
                                        
                                        x,y,w,h = cv2.boundingRect(contour)	
                                        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                                        cv2.putText(img,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
                                        print "000000000000000"
                                        break
                                else :
                                        print"00"
                        if (r>=1) :
                                print "nbr = %.1f" %nbr 
                                cap.release()
                                cv2.destroyAllWindows()
                                gpio.cleanup()
                                break
                        else :
                                pwm1.start(100)
                                pwm2.start(100)
                
                                
                                gpio.output(Moteur1A,gpio.LOW)
                                gpio.output(Moteur1B,gpio.HIGH)
                                gpio.output(Moteur1E,100)
                                
                                gpio.output(Moteur2A,gpio.HIGH)
                                gpio.output(Moteur2B,gpio.LOW)
                                gpio.output(Moteur2E,100)
                                                
                                time.sleep(0.6)
                                break
                        

                        
                                


                                                         
                        
                                        
                                 
                                   
                        #cv2.imshow("Redcolour",red)
                        cv2.imshow("Color Tracking",img)
                        #cv2.imshow("red",res) 	
                        if cv2.waitKey(10) & 0xFF == ord('q'):
                                 cap.release()
                                 cv2.destroyAllWindows()
                                 break





                        
                        
                        
               
    
               
# Reset gpio settings
gpio.cleanup()
                               
    
