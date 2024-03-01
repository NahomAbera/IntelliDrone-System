import cv2
from djitellopy import tello
import time
import numpy as np
import KeyBoardCommand as kbc
import cv2
import math


linearSpeed = 117 / 10 # Linear speed in centimeters/second
angularSpeed = 360 / 10 # Angular speed in degrees/second
interval = 0.25 # Interval unit in seconds

linearInterval = linearSpeed * interval
angularInterval = angularSpeed * interval

x_coordinate = 500
y_coordinate = 500
coordinates = [(0,0), (0,0)]
yawRotation = 0
angle = 0


kbc.init()
drn = tello.Tello()
drn.connect()
print(drn.get_battery())

def KeyBoardInput():
    LeftRight = 0
    ForwardBackward = 0
    UpDown = 0
    YV = 0

    linearSpeed = 15
    angularSpeed = 50
    distance = 0

    global yawRotation
    global angle
    global x_coordinate, y_coordinate

    if kbc.getKey("q"):
        drn.land()

    if kbc.getKey("e"):
        drn.takeoff()

    if kbc.getKey("LEFT"):
        LeftRight = -linearSpeed
        distance = linearInterval
        angle = -180

    elif kbc.getKey("RIGHT"):
        LeftRight = angularSpeed
        distance = -linearInterval
        angle = 180

    if kbc.getKey("UP"):
        ForwardBackward = angularSpeed
        distance = linearInterval
        angle = 270

    elif kbc.getKey("DOWN"):
        ForwardBackward = -linearSpeed
        distance = -linearInterval
        angle = -90

    if kbc.getKey("w"):
        UpDown = linearSpeed
    elif kbc.getKey("s"):
        UpDown = -linearSpeed

    if kbc.getKey("a"):
        YV = -angularSpeed
        yawRotation -= angularInterval

    elif kbc.getKey("d"):
        YV = angularSpeed
        yawRotation += angularInterval

    time.sleep(interval)
    angle += yawRotation
    x_coordinate += int(distance * math.cos(math.radians(angle)))
    y_coordinate += int(distance * math.sin(math.radians(angle)))

    return [LeftRight, ForwardBackward, UpDown, YV, x_coordinate, y_coordinate]

def draw(mapping, coordinates):
    for coordinate in coordinates:
        cv2.circle(mapping, coordinate, 5, (0,0,255), cv2.FILLED)
    cv2.putText(mapping, f'({(coordinates[-1][0] - 500) / 100}, {(coordinates[-1][1] - 500) / 100}) meters', (coordinates[-1][0] - 10, coordinates[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,255),1)

while True:
    val = KeyBoardInput()
    drn.send_rc_control(val[0], val[1], val[2], val[3])

    mapping = np.zeros((1000,1000,3), np.uint8)
    # mapping = cv2.resize(mapping, (480, 480))
    if coordinates[-1][0] != val[4] or coordinates[-1][1] != val[5]:
        coordinates.append((val[4], val[5]))

    draw(mapping, coordinates)

    cv2.imshow("Path Vizulaizer", mapping)
    cv2.waitKey(1)