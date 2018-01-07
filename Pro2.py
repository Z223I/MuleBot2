import time
import threading

class Pro2():
    """
    Producer 2 generates commands.
    """

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, _q, _qQuit):
        while self._running:
            command = raw_input("Enter command: ")
            name = threading.currentThread().getName()
            print "Producer thread:  ", name
            _q.put(command)
            print command
            if command[0] == 'q' or command[0] == 'Q':
                _qQuit.put(command)
                break
