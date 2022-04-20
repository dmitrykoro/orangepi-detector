import cv2
import face_recognition

import logging
import os

import time
import cProfile
import pstats

import numpy as np

from datetime import datetime
from PIL import Image


class ImageOperator:
    def __init__(self, path_to_image):
        self.path_to_image = path_to_image
        self.face_locations = []
        self.face_encodings = []

    @classmethod
    def init(cls, path_to_image):
        return ImageOperator(path_to_image=path_to_image)

    @property
    def path_to_image(self):
        return self._path_to_image

    @path_to_image.setter
    def path_to_image(self, value):
        self._path_to_image = value

    def locate_faces(self):
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            cv2_image_instance = cv2.imread(self.path_to_image)
            gray = cv2.cvtColor(cv2_image_instance, cv2.COLOR_BGR2GRAY)
            face_locations_cv2 = face_cascade.detectMultiScale(gray, 1.1, 4)
        except Exception as e:
            logging.error(f'Exception occurred while locating faces in the image {self._path_to_image}. '
                          f'Exception: {e.with_traceback()}')
            return

        number_of_detected_faces = len(face_locations_cv2)
        logging.warning(f'Detected {number_of_detected_faces} faces in the image {self._path_to_image}')

        if number_of_detected_faces:
            for x, y, w, h in face_locations_cv2:
                self.face_locations.append([(y, x + w, y + h, x)])
        return

    def encode_faces(self):
        face_recognition_image_instance = face_recognition.load_image_file(self.path_to_image)

        for current_locations in self.face_locations:
            try:
                self.face_encodings.append(face_recognition.face_encodings(
                    known_face_locations=current_locations,
                    face_image=face_recognition_image_instance
                ))
                logging.warning(f'Successfully encoded face in the image {self._path_to_image}')

            except Exception as e:
                logging.error(f'Exception occurred while making encoding for the image {self._path_to_image}. '
                              f'Exception: {e.with_traceback()}')
        return

    def delete_source_image(self):
        if self._path_to_image:
            os.remove(self._path_to_image)
            logging.warning(f'Successfully removed the source image: {self._path_to_image}')

        self._path_to_image = None

    def process_new_image(self):
        self.locate_faces()
        self.encode_faces()
        self.delete_source_image()


