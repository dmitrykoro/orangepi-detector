import json
import logging
import sys


class BaseServiceParameters:

    def __init__(self):
        try:
            service_params = json.load(open('params.json'))

            self.server_params = service_params['server']
            self.path_to_images = service_params['images']['src']
        except FileNotFoundError:
            logging.error('The configuration file params.json not found')
            sys.exit(-1)
        except KeyError:
            logging.error('Wrong key in the params.json file')
            sys.exit(-1)

        logging.warning('Init successful')
