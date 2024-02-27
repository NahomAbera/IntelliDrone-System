from djitellopy import tello
from time import sleep

drn = tello.Tello()
drn.connect()
print(drn.get_battery())
drn.takeoff()
drn.send_rc_control(0,10,0,0)
drn.flip_forward()
sleep(3)
drn.flip_back()
drn.send_rc_control(0,00,0,0)
drn.land()