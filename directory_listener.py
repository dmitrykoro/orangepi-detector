import time
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from image_operator import ImageOperator
from service_parameters_parser import BaseServiceParameters


class ScanDirectory(BaseServiceParameters):
    def __init__(self):
        super().__init__()

        self.observer = Observer()
        self.watch_directory = self.path_to_images

        logging.warning(f'Listening the directory {self.watch_directory}')

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            logging.warning("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            logging.warning("Received new image: " + event.src_path)

            current_image_path = event.src_path
            current_image_operator = ImageOperator(current_image_path)
            current_image_operator.process_new_image()


