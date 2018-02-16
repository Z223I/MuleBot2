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

    @patch('Accessory.Accessory._init_relay')
    def test___init__(self, mock__init_relay):
        self.assertTrue(self.testAccessory._running)
        self.assertEqual(self.testAccessory.time_on, 2)
        self.assertEqual(self.testAccessory.time_off, 4)
        self.assertFalse(self.testAccessory.auto_water)
        self.assertTrue(mock__init_relay.called)

    @patch('Accessory.RelayPiPy.init')
    def test_init_relay(self, mock_relay_init):
        self.testAccessory._init_relay()
        self.assertTrue(mock_relay_init.called)
        
    def test_terminate(self):
        self.testAccessory.terminate()
        self.assertFalse(self.testAccessory._running)
        
    def test_is_running(self):
        running = self.testAccessory.is_running()
        self.assertTrue(running)

    @patch('Accessory.RelayPiPy.on')
    def test__water_pump_A(self, mock_on):
        on = True
        is_on = self.testAccessory._water_pump(on)
        self.assertTrue(is_on)
        self.assertTrue(mock_on.called)

    @patch('Accessory.RelayPiPy.off')
    def test__water_pump_B(self, mock_off):
        on = False
        is_on = self.testAccessory._water_pump(on)
        self.assertFalse(is_on)
        self.assertTrue(mock_off.called)
    
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
        
        # The q isn't being used during the test.
        q = None
        self.testAccessory.water_pump(q)
        self.assertTrue(mock__w_p_init.called)
        self.assertTrue(mock__w_p_loop.called)
        self.assertTrue(mock_is_running.called)
        
    def test__w_p_init(self):
        pass

    @patch('Accessory.Accessory._w_p_queue_check')
    @patch('Accessory.Accessory._water_pump')
    @patch('Accessory.time.sleep')
    def test__w_p_loop_A(self, mock_time, mock__wp, mock_queue_check):
        """test__w_p_loop_A tests the water pump loop when auto_water is true."""
        
        mock__wp.side_effect = [True, False]
        
        self.testAccessory.auto_water = True
        
        # The q isn't being used in the test.  It's use is mocked.
        q = None
        self.testAccessory._w_p_loop(q)

        self.assertTrue(mock__wp.called)
        self.assertEqual(mock__wp.call_count, 2)

    @patch('Accessory.Accessory._w_p_queue_check')
    @patch('Accessory.Accessory._water_pump')
    @patch('Accessory.time.sleep')
    def test__w_p_loop_B(self, mock_time, mock__wp, mock_queue_check):
        """test__w_p_loop_B tests the water pump loop when auto_water is false."""
        
        mock__wp.side_effect = [True, False]
        
        self.testAccessory.auto_water = False

        # The q isn't being used in the test.  It's use is mocked.
        q = None
        self.testAccessory._w_p_loop(q)

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









