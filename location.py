import time

from convertbng.util import convert_bng
from gps import *


class PositionTracker:
    """
    position data using gps sensor
    """

    def __init__(self):

        self.gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        self.latitude = None
        self.longitude = None
        self.horizontal_accuracy = None
        self.gps_timestamp = None
        self.easting = None
        self.northing = None
        self.reading_num = 0
        self.time = None

    def get_reading(self):
        # get sensor readings
        reading = False
        while not reading:
            nx = self.gpsd.next()
            if nx["class"] == "TPV" and hasattr(nx, "eph") and self.time != nx["time"]:
                # get coordinates
                self.latitude = getattr(nx, "lat", None)
                self.longitude = getattr(nx, "lon", None)
                self.convert_coords()
                # get time and acc meta
                self.horizontal_accuracy = getattr(nx, "eph", None)
                self.time = getattr(nx, "time", None)
                self.reading_num += 1
                # stop loop
                reading = True

    def convert_coords(self):
        # convert lat long to Easting Northing
        res_list = convert_bng(self.longitude, self.latitude)
        self.easting = res_list[0][0]
        self.northing = res_list[1][0]


if __name__ == "__main__":
    pos = PositionTracker()

    while True:
        pos.get_reading()
        print(
            pos.latitude,
            pos.longitude,
            pos.easting,
            pos.northing,
            pos.time,
            pos.horizontal_accuracy,
        )
