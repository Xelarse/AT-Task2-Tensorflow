import os
import cv2
import numpy as np
import requests
import random
from pathlib import Path
import time

# Latitude range = -90 to 90
# Longitude range = -180 to 180

# Wales and england long = -4.6 to 1.2, lat = 50.6 to 54.6
# New york long = -74.5 to -73.6, lat 40.58 to 41
# Dubai long 54.9 to 55.8, lat 24.87 to 25.52

LONG = [-4.6, 1.2]
LAT = [50.6, 54.6]
MAP_SIZE = 1000      # width and height
MAP_TYPE = "sat"  # Map = map, Satellite = sat, Hybrid = hyb
IMG_TYPE = "png"    # jpg or png
ZOOM_LEVEL = 17     # 1 - 18
IMG_AMOUNT = 20


def fetch_random_image_from_mapquest():
    lat = random.uniform(LAT[0], LAT[1])
    lon = random.uniform(LONG[0], LONG[1])
    url = f"https://www.mapquestapi.com/staticmap/v4/getmap?key=E02fmBElqJp2hrREVk635hTidJ8dtIS1&size={MAP_SIZE},{MAP_SIZE + 60}&type={MAP_TYPE}&imagetype={IMG_TYPE}&zoom={ZOOM_LEVEL}&scalebar=false&traffic=false&center={lat},{lon}"
    resp = requests.get(url, stream=True).raw
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    return cv2.imdecode(image, cv2.IMREAD_COLOR)


def save_random_image():
    new_image = fetch_random_image_from_mapquest()
    cropped_img = new_image[0:MAP_SIZE, 0:MAP_SIZE]
    path = str(Path(__file__).parents[2]) + "\\Dataset\\Satellite\\RawImages\\"
    file_name = f"{int(time.time())}.{IMG_TYPE}"
    cv2.imwrite(path + file_name, cropped_img)


for x in range(IMG_AMOUNT):
    save_random_image()


# Test code
# new_image = fetch_random_image_from_mapquest()
# cv2.imshow("Map image", new_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


