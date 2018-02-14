try:
    from builtins import object
except ImportError:
    pass

import unittest
from unittest.mock import patch

import time

import sys
sys.path.append('/home/pi/pythondev/MuleBot2/MuleBot')
from Accessory import Accessory

class TestAccessory(unittest.TestCase):

    def setUp(self):
        self.testAccessory = Accessory()

    def tearDown(self):
        pass

    def test___init__(self):
        self.assertEqual(self.testAccessory.time_on, 2)
        self.assertEqual(self.testAccessory.time_off, 4)

    def test_water_pump(self):
        pass
        
    def test__w_p_init(self):
        pass
        
    def test__w_p_loop(self):
        pass
        
        
#    def test_set_clip_distance(self):
#        val = 6
#        self.testRangeBot.set_clip_distance(val)
#        self.assertEqual(self.testRangeBot.clip_distance, val)

#    @patch('RangeBot.time.sleep')
#    @patch('RangeBot.LidarLite3Ext.read')
#    def test_scan2_A(self, mock_read, mock_sleep):
#        mock_read.return_value = 80



if __name__ == "__main__":

    unittest.main()









