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

#serial init
ser = serial.Serial()
ser.baudrate = 115200
ser.port= 'COM12'
ser.open()

if not ser.is_open:
    print('Unable to open Serial Port')

#capture the webcam video feed and init subtractor
cap = cv2.VideoCapture(0)
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
        cv2.imshow('frame',closing)
    else:
        cX = -1
        cY = -1

    #CONVERT cX and cY into pitchAngle and yawAngle

    #write angles to string
    if(millis() - lastTime > 50) #update rate of 20hz
    {
        lastTime = millis()
        pitchAngleString = 'P'+str(pitchAngle)+'\n'
        yawAngleString = 'Y'+str(yawAngle)+'\n'
        shootString = 'S'+'\n'

        #send string through serial
        ser.write(pitchAngleString.encode('utf-8'))
        ser.write(yawAngleString.encode('utf-8'))
        ser.write(shootString.encode('utf-8'))
    }
    
    #quit if user presses q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(fgmask)
        break

#deinit
cap.release()
cv2.destroyAllWindows()
