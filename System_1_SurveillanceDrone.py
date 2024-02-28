from djitellopy import tello
import time
import cv2
import KeyBoardCommand as kbc


kbc.init()
drn = tello.Tello()
drn.connect()
print(drn.get_battery())

global strm
drn.streamon()
def KeyBoardInput():
    LeftRight = 0
    ForwardBackward = 0
    UpDown = 0
    YV = 0
    speed = 50

    if kbc.getKey("q"):
        drn.land()
        time.sleep(3)

    if kbc.getKey("e"):
        drn.takeoff()

    if kbc.getKey("LEFT"):
        LeftRight = -speed
    elif kbc.getKey("RIGHT"):
        LeftRight = speed

    if kbc.getKey("UP"):
        ForwardBackward = speed
    elif kbc.getKey("DOWN"):
        ForwardBackward = -speed

    if kbc.getKey("w"):
        UpDown = speed
    elif kbc.getKey("s"):
        UpDown = -speed

    if kbc.getKey("a"):
        YV = speed
    elif kbc.getKey("d"):
        YV = -speed

    if kbc.getKey("r"):
        cv2.imwrite(f'Snapshots/{time.time()}.jpg', strm)
        time.sleep(0.3)

    return [LeftRight, ForwardBackward, UpDown, YV]


while True:
    val = KeyBoardInput()
    drn.send_rc_control(val[0], val[1], val[2], val[3])
    strm = drn.get_frame_read().frame
    strm = cv2.resize(strm, (480, 480))
    cv2.imshow("Image", strm)
    cv2.waitKey(1)