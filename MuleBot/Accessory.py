#/usr/bin/python

import sys
sys.path.append('/home/pi/pythondev/RelayPiPy/RelayPiPy')
from RelayPiPy import RelayPiPy

#import threading

import time


class Accessory:
    """Accessory """

    def __init__(self):
        """__init__ initializes class variables."""
        self._running = True
        self.time_on = 2
        self.time_off = 4

    def terminate(self):
        """terminate triggers the thread to stop."""
        
        self._running = False

    def _init_relay(self):
        """_init_relay initializes the relay."""

        self.relay4 = RelayPiPy()

        # init list with pin numbers
        pinList = [6, 13, 19, 26]
        self.relay4.init(pinList)
            
    def is_running(self):
        """is_running returns true if the thread is running, otherwise false"""
        
        return self._running
    
    def _water_pump(self, on):
        """_water_pump turns the water pump on/off as specified by the input
        parameter.
        
        @type: boolean
        @param on
        
        @rtype: boolean
        @rparam: on """
        
        # Set water pump to on/off.
        relay_no = 1
        
        if on:
            self.relay4.on(relay_no)
        else:
            self.relay4.off(relay_no)

        return on

    def _w_p_init(self):
        pass
        
    def _w_p_loop(self):
        """_w_p_loop cycles the water pump on and off.  It is used in the
        water_pump method."""

        on = True
        self._water_pump(on)
        time.sleep(self.time_on)
        
        on = False
        self._water_pump(on)
        time.sleep(self.time_off)
    
    def water_pump(self):
        """water_pump is the thread which controls the water pump."""
        self._w_p_init()
        
        while self.is_running():
            self._w_p_loop()
