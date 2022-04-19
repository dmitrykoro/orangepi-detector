from threading import Thread
from directory_listener import ScanDirectory


def init_directory_listener():
    scanner = ScanDirectory()
    scanner.run()


if __name__ == '__main__':
    Thread(target=init_directory_listener).start()
