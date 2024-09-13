import argparse
import datetime
import os
import time

import cv2
import pandas as pd
import serial

from camera import Camera
from location import PositionTracker
from multiprocessing import Process

IMAGE_DIR = "Images"
IMAGE_METADATA_FILE = "image_metadata.csv"
POSITION_METADATA_FILE = "position_metadata.csv"


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


def save_data(data: list, save_path: str) -> None:
    """
    save data as csv

    params:
        data: jsonL data to save
        save_path: full save location of file
    """

    pd.DataFrame.from_dict(data).to_csv(os.path.join(save_path), index=False)


def camera(output_dir: str, sample_rate: int = 5, save_rate: int = 50) -> None:
    """
    take images with camera and save

    params:
        output_dir: save path of imagery and metadata
        sample_rate: number of images every second
        save_rate: save metadata file after this many rows
    """
    
    cam = Camera()
    data = []

    while True:

        cam.take_image()
        filename = os.path.join(
            output_dir,
            IMAGE_DIR,
            f"image_{cam.reading_num}.jpg",
        )
        cam.save_image(filename)

        # add reading to data
        data.append(
            {
                "filename": filename,
                "reading_num_cam": cam.reading_num,
                "cam_time": cam.time,
            }
        )
        # wait sample rate
        time.sleep(1 / sample_rate)

        # save if rate is reached
        if cam.reading_num % save_rate == 0:
            print("saving image metadata")
            save_data(data, os.path.join(output_dir, IMAGE_METADATA_FILE))


def location(output_dir: str, save_rate: int = 10) -> None:
    """
    sample gps and save

    params:
        output_dir: save path of metadata
        save_rate: save metadata file after this many rows
    """
    pos = PositionTracker()
    data = []

    while True:

        pos.get_reading()

        data.append(
            {
                "easting": pos.easting,
                "northing": pos.northing,
                "latitude": pos.latitude,
                "longitude": pos.longitude,
                "horizontal_accuracy": pos.horizontal_accuracy,
                "reading_num_gps": pos.reading_num,
                "gps_time": pos.parsed_time,
            }
        )
        if pos.reading_num % save_rate == 0:
            print("saving position meta_data")
            save_data(data, os.path.join(output_dir, POSITION_METADATA_FILE))


def main(output_dir: str) -> None:
    """
    main function
    
    params:
        output_dir: save path of imagery and metadata
    """

    # set up multiprocesses
    p_cam = Process(target=camera, args=(output_dir,))
    p_cam.start()

    p_loc = Process(target=location, args=(output_dir,))
    p_loc.start()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="capture gps tagged imagery")
    parser.add_argument(
        "--output_dir", "-o", type=str, help="output folder", default="."
    )

    args = parser.parse_args()
    output_dir = setup_output_folder(args.output_dir)
    main(output_dir)
