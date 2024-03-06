import time

import cv2
import numpy as np
from djitellopy import tello

drn = tello.Tello()
drn.connect()
print(drn.get_battery())

drn.streamon()
drn.takeoff()
drn.send_rc_control(0,0,15,0)
time.sleep(1.5)

width = 360
height = 240
forwardBackwardRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0
def findFace(strm):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    strmGray = cv2.cvtColor(strm, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(strmGray, 1.2, 8)

    faceArray = []
    faceAreaArray = []

    for x,y,width,height in faces:
        cv2.rectangle(strm, (x,y), (x + width, y + height), (0,0,255), 2)

        centerX = x + (width // 2)
        centerY = y + (height // 2)

        area = width * height
        cv2.circle(strm, (centerX, centerY), 5, (0,255,0), cv2.FILLED)

        faceArray.append([centerX, centerY])
        faceAreaArray.append(area)

    if len(faceAreaArray) != 0:
        i = faceAreaArray.index(max(faceAreaArray))
        return strm, [faceArray[i], faceAreaArray[i]]
    else:
        return strm, [[0,0],0]

def trackFace(info, width, pid, pError):
    area = info[1]
    x, y = info[0]
    forwardBackward = 0

    error = x - (width // 2)
    speed = (pid[0] * error) + (pid[1] * (error - pError))
    speed = int(np.clip(speed, -100,100))

    if area > forwardBackwardRange[0] and area < forwardBackwardRange[1]:
        forwardBackward = 0
    elif area < forwardBackwardRange[0] and area != 0:
        forwardBackward = 20
    elif area > forwardBackwardRange[1]:
        forwardBackward = -20
    if x == 0:
        speed = 0
        error = 0

    #print(speed, forwardBackward)

    drn.send_rc_control(0, forwardBackward, 0, speed)
    return error

cap = cv2.VideoCapture(0)

while True:
    #_, strm = cap.read()
    strm = drn.get_frame_read().frame
    strm = cv2.resize(strm, (width, height))
    strm, info = findFace(strm)
    pError = trackFace(info, width, pid, pError)
    #print("Center: ", info[0], "Area: ", info[1])
    cv2.imshow("Stream", strm)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        drn.land()
        break