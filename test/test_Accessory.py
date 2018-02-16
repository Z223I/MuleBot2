try:
    from builtins import object
except ImportError:
    pass

import unittest
from unittest.mock import patch

import queue
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
        self.assertFalse(self.testAccessory.auto_water)

    def test_terminate(self):
        self.testAccessory.terminate()
        self.assertFalse(self.testAccessory._running)
        
    def test_is_running(self):
        running = self.testAccessory.is_running()
        self.assertTrue(running)

    def test__w_p_queue_check_A(self):
        """test__w_p_queue_check_A checks the water on command, a.k.a. 'won'
        to verify it is working."""
        
        # Establish water pump queue.
        q_w_p = queue.Queue(maxsize=0)
        
        # Place command in the queue
        q_w_p.put('won')
        
        # Call _w_p_queue_check
        self.testAccessory._w_p_queue_check(q_w_p)
        
        # assert on
        self.assertTrue(self.testAccessory.auto_water)

    def test__w_p_queue_check_B(self):
        """test__w_p_queue_check_B checks the water off command, a.k.a. 'woff'
        to verify it is working."""
        
        # Establish water pump queue.
        q_w_p = queue.Queue(maxsize=0)
        
        # Place command in the queue
        q_w_p.put('woff')
        
        # Call _w_p_queue_check
        self.testAccessory._w_p_queue_check(q_w_p)
        
        # assert off
        self.assertFalse(self.testAccessory.auto_water)


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

    @patch('Accessory.Accessory._water_pump')
    @patch('Accessory.time.sleep')
    def test__w_p_loop_A(self, mock_time, mock__wp):
        """test__w_p_loop_A tests the water pump loop when auto_water is true."""
        
        mock__wp.side_effect = [True, False]
        
        self.testAccessory.auto_water = True
        self.testAccessory._w_p_loop()

        self.assertTrue(mock__wp.called)
        self.assertEqual(mock__wp.call_count, 2)

    @patch('Accessory.Accessory._water_pump')
    @patch('Accessory.time.sleep')
    def test__w_p_loop_B(self, mock_time, mock__wp):
        """test__w_p_loop_B tests the water pump loop when auto_water is false."""
        
        mock__wp.side_effect = [True, False]
        
        self.testAccessory.auto_water = False
        self.testAccessory._w_p_loop()

        self.assertFalse(mock__wp.called)
        self.assertEqual(mock_time.call_count, 1)
        
        
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









