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
    
    def _water_pump(self, on):
        """_water_pump turns the water pump on/off as specified by the input
        parameter.
        
        @type: boolean
        @param on
        
        @rtype: boolean
        @rparam: on """
        
        # Set water pump to on.
        # TODO: Control the relay.
        return on

    def _w_p_init(self):
        pass
        
    def _w_p_loop(self):
        """_w_p_loop cycles the water pump on and off."""

        on = True
        self._water_pump(on)
        time.sleep(self.time_on)
        
        on = False
        self._water_pump(on)
        time.sleep(self.time_off)
    
    def water_pump(self):
        self._w_p_init()
        
        while self.is_running():
            self._w_p_loop()
