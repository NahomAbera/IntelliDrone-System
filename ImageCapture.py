from djitellopy import tello
import cv2

drn = tello.Tello()
drn.connect()
print(drn.get_battery())

drn.streamon()

while True:
    img = drn.get_frame_read().frame
    cv2.imshow("Image", img)
    cv2.waitKey(1)