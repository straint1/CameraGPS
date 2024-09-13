from gps import *


gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)

while True:
    nx = gpsd.next()
    print(nx)
