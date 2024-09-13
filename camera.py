import time

import cv2
import datetime


class Camera:
    """
    camera class
    """

    def __init__(self):
        # define a video capture object
        self.cam = cv2.VideoCapture(0)
        self.reading_num = 0

    def take_image(self):
        # Capture the video frame
        self.ret, self.frame = self.cam.read()
        # get time
        self.time = datetime.datetime.now()
        self.reading_num += 1

    def display_image(self):
        # Display the resulting frame
        cv2.imshow("frame", self.frame)

    def save_image(self, filename):
        # save image to filename
        cv2.imwrite(filename, self.frame)

    def shutdown(self):
        # After the loop release the cap object
        self.cam.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
