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
        self.assertTrue(self.testAccessory._running)
        self.assertEqual(self.testAccessory.time_on, 2)
        self.assertEqual(self.testAccessory.time_off, 4)

    def test_terminate(self):
        self.testAccessory.terminate()
        self.assertFalse(self.testAccessory._running)
        
    def test_is_running(self):
        running = self.testAccessory.is_running()
        self.assertTrue(running)

    @patch('Accessory.Accessory.is_running')
    @patch('Accessory.Accessory._w_p_loop')
    @patch('Accessory.Accessory._w_p_init')
    def test_water_pump(self, mock__w_p_init, mock__w_p_loop, mock_is_running):
        mock_is_running.side_effect = [True, False]
        
        self.testAccessory.water_pump()
        self.assertTrue(mock__w_p_init.called)
        self.assertTrue(mock__w_p_loop.called)
        self.assertTrue(mock_is_running.called)
        
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









