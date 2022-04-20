import json


class BaseServiceParameters:

    def __init__(self):
        service_params = json.load(open('params.json'))

        self.server_address = service_params['server']['address']
        self.auth_token = service_params['server']['auth_token']
        self.path_to_images = service_params['images']['src']
