import cv2
import face_recognition
import numpy as np

import time

import cProfile, pstats

from datetime import datetime
from PIL import Image


def proceed(path):
    time.sleep(3)
    with open("Where to save") as fp:
        directoryToSave = fp.readline().strip()

    profiler = cProfile.Profile()
    profiler.enable()

    image = face_recognition.load_image_file(path)
    face_locations = face_recognition.face_locations(image, model="hog")
    encoding = face_recognition.face_encodings(image)[0]
    profiler.disable()
    make_rectangle(image, face_locations, directoryToSave)


def make_rectangle(image, coordinates, path_to_save):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for i in range(len(coordinates)):
        cv2.rectangle(rgb,
                      (coordinates[i][3], coordinates[i][2]),
                      (coordinates[i][1], coordinates[i][0]),
                      (255, 255, 0), 2)

    profiler = cProfile.Profile()
    profiler.enable()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()

    currentTime = datetime.now().strftime("%H:%M:%S")
    cv2.imwrite(f'{path_to_save}{currentTime}_found({len(coordinates)}).jpg', rgb)
    print(f"Saved image to {path_to_save}")


def cutImage(path, coordinates, path_to_save):
    img = Image.open(path)
    for i in range(len(coordinates)):
        top = coordinates[i][0]
        right = coordinates[i][1]
        bottom = coordinates[i][2]
        left = coordinates[i][3]

        box = (left, top, right, bottom)

        currentTime = datetime.now().strftime("%H:%M:%S")
        imgCropped = img.crop(box)
        imgCropped.save(f'{path_to_save}{currentTime}_{i}.jpg')
