try:
    from builtins import object
except ImportError:
    pass

#import warnings
#import sys

import unittest
#import time

import sys
sys.path.append('/home/pi/pythondev/MuleBot2/MuleBot')
print(sys.path)
from mulebot import MuleBot

class TestMuleBot(unittest.TestCase):

    def setUp(self):
        self.test_mulebot = MuleBot()

    def tearDown(self):
        pass

    def test___init___(self):
        self.assertEqual(self.testservo.channel, TestServo.CHANNEL)

        self.assertEqual(130, self.testservo.SERVO_MIN)
        self.assertEqual(630, self.testservo.SERVO_MAX)




if __name__ == "__main__":

    unittest.main()
