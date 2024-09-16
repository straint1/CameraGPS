# CameraGPS
Capture gps tagged imagery on a raspberry pi from serial gps connection.

Tested on raspberry pi 4 running Ubuntu with a usb ublox8 gps reciever, and standard raspberry pi V2 camera module. 

# Instructions
- clone repo
- install gpsd following this [tutorial](https://raspberrypi.stackexchange.com/questions/113057/how-can-rpi-listen-to-a-gps-module) note changing etc/defualt/gpsd file.
- install requirements.txt with `pip3 install -r requirements.txt`

# Usage
`python3 main.py -o <out_directory>` will create images with corresponding position and image metadata.
