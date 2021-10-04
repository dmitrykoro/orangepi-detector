import time
from ImageOperator import proceed


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



class ScanDirectory:
    with open("Directory") as fp:
        watchDirectory = fp.readline().strip()
        print(f'Watching for the directory: {watchDirectory}')

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
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
            currentImagePath = event.src_path

            proceed(path=currentImagePath)


