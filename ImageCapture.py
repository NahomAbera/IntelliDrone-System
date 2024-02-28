from djitellopy import tello
import cv2

drn = tello.Tello()
drn.connect()
print(drn.get_battery())

drn.streamon()

while True:
    strm = drn.get_frame_read().frame
    cv2.imshow("Snapshots", strm)
    cv2.waitKey(1)