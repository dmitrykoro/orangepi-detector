import json
import subprocess

import logging
import os
import requests


class ImageOperator:
    def __init__(self, path_to_image, server_params):
        self.path_to_image = path_to_image
        self.server_params = server_params
        self.face_locations = []
        self.face_encodings = []

    @classmethod
    def init(cls, path_to_image, server_params):
        return ImageOperator(path_to_image=path_to_image, server_params=server_params)

    @property
    def path_to_image(self):
        return self._path_to_image

    @path_to_image.setter
    def path_to_image(self, value):
        self._path_to_image = value

    @property
    def server_params(self):
        return self._server_params

    @server_params.setter
    def server_params(self, value):
        self._server_params = value

    def encode_faces_binary(self):
        output = subprocess.run(["./dnn_face_recognition_ex", self.path_to_image], stdout=subprocess.PIPE, universal_newlines=True).stdout
        self.face_encodings = output
        return

    def delete_source_image(self):
        if self._path_to_image:
            os.remove(self._path_to_image)
            logging.warning(f'Successfully removed the source image: {self._path_to_image}')

        self._path_to_image = None

    def send_encodings_to_server(self):
        address = self.server_params['address']
        auth_token = self.server_params['auth_token']

        headers = {
            'user-agent': 'orangepi-zero',
            'authorization': auth_token
        }
        #data = {'data': self.face_encodings}
        data = json.dumps(self.face_encodings)

        try:
            requests.post(address, headers=headers, data=data)
        except requests.exceptions.InvalidSchema:
            logging.error('Wrong server address format: use https://<...>')

        logging.warning(f'Sent encodings to the server {address}')

        return

    def process_new_image(self):
        self.encode_faces_binary()
        self.delete_source_image()
        self.send_encodings_to_server()


