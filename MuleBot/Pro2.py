#!/usr/bin/python

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
            command = input("Enter command: ")
            name = threading.currentThread().getName()
#            print ("Producer thread:  ", name)

            emptyString = ( len(command) == 0 )
            if ( emptyString ):
                pass
            else:
                _q.put(command)
#                print (command)
                if command[0] == 'h' or command[0] == 'H':
                    _qQuit.put(command)
                    break
