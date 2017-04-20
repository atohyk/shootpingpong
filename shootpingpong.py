import cv2
import serial
import numpy as np
import time



#system macros
millis = lambda: int(round(time.time() * 1000))

#system variables
pitchAngle = 0
yawAngle = 0
lastPrintTime = 0
lastShootTime = millis()

#serial init
ser = serial.Serial()
ser.baudrate = 115200
ser.port= 'COM12'
ser.open()

if not ser.is_open:
    print('Unable to open Serial Port')

#functions
def shoot():
    shootString = 'S'+'\n'
    ser.write(shootString.encode('utf-8'))

def up():
    pitchAngle += 10
    if pitchAngle > 180:
        pitchAngle= 180
    pitchAngleString = 'P'+str(pitchAngle)+'\n'
    ser.write(pitchAngleString.encode('utf-8'))

def down():
    pitchAngle -= 10
    if pitchAngle < 0:
        pitchAngle = 0
    pitchAngleString = 'P'+str(pitchAngle)+'\n'
    ser.write(pitchAngleString.encode('utf-8'))    

def left():
    yawAngle -= 10
    if yawAngle < 0:
        yawAngle = 0
    yawAngleString = 'P'+str(yawAngle)+'\n'
    ser.write(yawAngleString.encode('utf-8'))

def right():
    yawAngle += 10
    if yawAngle > 180:
        yawAngle = 180
    yawAngleString = 'P'+str(yawAngle)+'\n'
    ser.write(yawAngleString.encode('utf-8'))    

    
#capture the webcam video feed and init subtractor
cap = cv2.VideoCapture(1)
fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = np.ones((5,5),np.uint8)

#initialize windows
while(True):
    ret,frame = cap.read()
    fgmask = fgbg.apply(frame)

    #delete noise outside of object
    opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    #fill holes in object
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    m = cv2.moments(closing)
    if m["m00"] > 1:
        cX = int(m["m10"] / m["m00"])
        cY = int(m["m01"] / m["m00"])
        cv2.circle(closing, (cX, cY), 50, (255,255,255), 10)
        cv2.circle(frame, (cX, cY), 50, (255,0,0), 10)
        cv2.imshow('closing',closing)
    else:
        cX = -1
        cY = -1
        
    cv2.imshow('frame', frame)
    #CONVERT cX and cY into pitchAngle and yawAngle
    '''
    
    #write angles to string
    if(millis() - lastPrintTime > 50) : #update rate of 20hz
        if ser.is_open:
            lastPrintTime = millis()
            pitchAngleString = 'P'+str(pitchAngle)+'\n'
            yawAngleString = 'Y'+str(yawAngle)+'\n'
            shootString = 'S'+'\n'

            #send string through serial
            ser.write(pitchAngleString.encode('utf-8'))
            ser.write(yawAngleString.encode('utf-8'))
            ser.write(shootString.encode('utf-8'))
    '''
       
    #quit if user presses q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord(' '):
        if lastShootTime - millis() > 500:
            shootString = 'S'+'\n'
            ser.write(shootString.encode('utf-8'))
            lastShootTime = millis()

#deinit
cap.release()
cv2.destroyAllWindows()
ser.close()

