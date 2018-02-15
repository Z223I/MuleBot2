#/usr/bin/python

#import threading

import time

class Accessory:
    """Accessory """

    def __init__(self):
        self._running = True
        self.time_on = 2
        self.time_off = 4

    def terminate(self):
        self._running = False
        
    def is_running(self):
        return self._running

    def _w_p_init(self):
        pass
        
    def _w_p_loop(self):
        time.sleep(self.time_on)
        time.sleep(self.time_off)
    
    def water_pump(self):
        self._w_p_init()
        
        while self.is_running():
            self._w_p_loop()
