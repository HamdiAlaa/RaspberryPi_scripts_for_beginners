import numpy as np
import cv2
import RPi.GPIO as GPIO
 
video_capture = cv2.VideoCapture(-1)
video_capture.set(3, 160)
video_capture.set(4, 120)

GPIO.setmode(GPIO.BOARD)
m11 = 3
m12 = 5
m1pwm = 7
m21 = 11
m22 = 13
m2pwm = 15

# Setup Output Pins
 
# moteur 1
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m1pwm, GPIO.OUT)
# moteur 2
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.setup(m2pwm, GPIO.OUT)

pwm1 = GPIO.PWM(m1pwm,50)   ## pwm de la pin 22 a une frequence de 50 Hz
pwm2 = GPIO.PWM(m2pwm,50)   ## pwm de la pin 22 a une frequence de 50 Hz

 
while(True):
 
    # Capture the frames
    ret, frame = video_capture.read()
 
    # Crop the image
    crop_img = frame[60:120, 0:160]
 
    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
 
    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
 
    # Color thresholding
    ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
 
    # Erode and dilate to remove accidental line detections
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
 
    # Find the contours of the frame
    _, contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
 
    # Find the biggest contour (if detected)
    if len(contours) > 0 :
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
 
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
 
        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
 
        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
 
        # print cx
        # print cy
 
        if cx >= 120:
            print "Turn Left!"
            pwm1.start(30)
            GPIO.output(m11, GPIO.LOW)
            GPIO.output(m12, GPIO.LOW)
            GPIO.output(m21, GPIO.HIGH)
            GPIO.output(m22, GPIO.LOW)
            m=0
 
        if cx < 120 and cx > 50:
            print "On Track!"
            pwm1.start(30)
            pwm2.start(25)
            GPIO.output(m11, GPIO.HIGH)
            GPIO.output(m12, GPIO.LOW)
            GPIO.output(m21, GPIO.HIGH)
            GPIO.output(m22, GPIO.LOW)
            
        if cx <= 50:
            print "Turn Right!"
            pwm2.start(25)
            GPIO.output(m11, GPIO.HIGH)
            GPIO.output(m12, GPIO.LOW)
            GPIO.output(m21, GPIO.LOW)
            GPIO.output(m22, GPIO.LOW)
            m=2
 
    else:
        if m==0:
            print "Turn Left!"
            pwm1.start(30)
            pwm2.start(25)
            GPIO.output(m11, GPIO.LOW)
            GPIO.output(m12, GPIO.HIGH)
            GPIO.output(m21, GPIO.HIGH)
            GPIO.output(m22, GPIO.LOW)
            m=0        
        if m==2:
            print "Turn Right!"
            pwm1.start(30)
            pwm2.start(25)
            GPIO.output(m11, GPIO.HIGH)
            GPIO.output(m12, GPIO.LOW)
            GPIO.output(m21, GPIO.LOW)
            GPIO.output(m22, GPIO.HIGH)
            m=2
 
 
    #Display the resulting frame
    cv2.imshow('frame',crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
GPIO.cleanup()

