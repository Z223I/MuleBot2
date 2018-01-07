import time
import threading

class Pro1():
    """
    Producer 1 generates numbers.
    """

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, _q):
        while self._running:
            name = threading.currentThread().getName()
            print "Producer thread:  ", name
            number = 5
            _q.put(number)
            print number
            time.sleep(4)
