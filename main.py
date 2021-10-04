from threading import Thread

import cProfile

from DirectoryListener import ScanDirectory



def initDirectoryListener():
    scan = ScanDirectory()
    scan.run()


if __name__ == '__main__':
    Thread(target=initDirectoryListener).start()



