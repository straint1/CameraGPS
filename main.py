import argparse
import datetime
import os
import time

import cv2
import pandas as pd
import serial

from camera import Camera
from location import PositionTracker

IMAGE_DIR = "Images"
METADATA_FILE = "metadata.csv"
DATA_SAVE_RATE = 10


def setup_output_folder(
    output_dir: str,
) -> str:
    """
    creates output folders if not already created

    returns modified output folder (with timestamp)
    """

    # create initial folder
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # and now time stamped folder in there
    now_str = datetime.datetime.now().strftime("%d-%b-%y_%H-%M")
    output_dir = os.path.join(output_dir, now_str)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    image_dir = os.path.join(output_dir, IMAGE_DIR)
    if not os.path.exists(image_dir):
        os.mkdir(image_dir)

    return output_dir


def save_data(data: list, output_dir: str) -> None:
    """
    save data as csv
    """

    pd.DataFrame.from_dict(data).to_csv(
        os.path.join(output_dir, METADATA_FILE), index=False
    )


def main(
    output_dir: str,
) -> None:
    """
    main camera and gps sensor loop

    args:
            output_dir: where to save image
    """

    data = []

    # initialise camera and gps
    cam = Camera()
    pos = PositionTracker()

    # keep looping
    while True:

        # gps reading
        pos.get_reading()

        # take image
        cam.take_image()
        filename = os.path.join(
            output_dir,
            IMAGE_DIR,
            f"image_{cam.reading_num}.jpg",
        )
        # cam.display_image()

        # add reading to data
        data.append(
            {
                "filename": filename,
                "easting": pos.easting,
                "northing": pos.northing,
                "latitude": pos.latitude,
                "longitude": pos.longitude,
                "horizontal_accuracy": pos.horizontal_accuracy,
                "reading_num_cam": cam.reading_num,
                "reading_num_gps": pos.reading_num,
                "gps_time": pos.time,
                "cam_time": cam.time,
            }
        )
        print(data[-1])

        # save image and data every
        cam.save_image(filename)
        if cam.reading_num % DATA_SAVE_RATE == 0:
            save_data(data, output_dir)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cam.shutdown()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="capture gps tagged imagery")
    parser.add_argument(
        "--output_dir", "-o", type=str, help="output folder", default="."
    )

    args = parser.parse_args()
    output_dir = setup_output_folder(args.output_dir)
    main(output_dir)
