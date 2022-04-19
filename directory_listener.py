import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from image_operator import ImageOperator


class ScanDirectory:
    def __init__(self):
        self.observer = Observer()
        with open("Directory") as fp:
            self.watch_directory = fp.readline().strip()
            print(f'Watching for the directory: {self.watch_directory}')

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            print("Received new image: " + event.src_path)

            current_image_path = event.src_path
            current_image_operator = ImageOperator(current_image_path)
            current_image_operator.process_new_image()

            print(current_image_operator.face_encodings)