from djitellopy import tello

drn = tello.Tello()

drn.connect()

print(drn.get_battery())