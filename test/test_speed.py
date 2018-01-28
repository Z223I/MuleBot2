try:
    from builtins import object
except ImportError:
    pass

#import warnings
#import sys

import unittest
#import time
import queue
import math
import time

import sys
sys.path.append('/home/pi/pythondev/MuleBot2/MuleBot')
#print(sys.path)
from mulebot import MuleBot
import RPi.GPIO as GPIO





class TestMuleBot(unittest.TestCase):
    """ These tests are to be ran with the robot and visually verified."""

    MAX_VELOCITY_METERS_PER_SEC = 3.830227695
    SECONDS_PER_MINUTE = 60
    MAX_RPM = 12
    RADIANS_PER_REV = 2
    MAX_VELOCITY_RADS_PER_SEC = MAX_RPM / SECONDS_PER_MINUTE * RADIANS_PER_REV

    def setUp(self):
        self.test_mulebot = MuleBot()

    def tearDown(self):
        pass

    def test_motorSpeed_A(self):
        """test_motorSpeed_A sets bot wheels to zero rpm and then checks the pwmDuration.
        """
        rpm = 0

        self.test_mulebot.motorSpeed(rpm, rpm)

        self.assertEqual(self.test_mulebot.dcMotorPWMDurationLeft, 0)

    def test_motorSpeed_B(self):
        """test_motorSpeed_A sets bot wheels to 3 rpm and then checks the pwmDuration.
        """
        rpm = 3
        self.test_mulebot.motorSpeed(rpm, rpm)
        time.sleep(2)

        rpm = 0
        self.test_mulebot.motorSpeed(rpm, rpm)
        time.sleep(1)

        self.assertEqual(self.test_mulebot.dcMotorPWMDurationLeft, 1023)

    def test_motorSpeed_C(self):
        """test_motorSpeed_C sets bot wheels to three rpm and then checks the pwmDuration.
        The left wheel goes backwards and the right wheel goes forward.
        """
        rpm = 3
        self.test_mulebot.motorSpeed(-rpm, rpm)
        time.sleep(2)

        rpm = 0
        self.test_mulebot.motorSpeed(rpm, rpm)
        time.sleep(1)

        self.assertEqual(self.test_mulebot.dcMotorPWMDurationLeft, 1023)

    def test_motorSpeed_D(self):
        """test_motorSpeed_D sets bot wheels to three rpm and then checks the pwmDuration.
        The left wheel goes forward and the right wheel goes backward.
        """
        rpm = 3
        self.test_mulebot.motorSpeed(rpm, -rpm)
        time.sleep(2)

        rpm = 0
        self.test_mulebot.motorSpeed(rpm, rpm)
        time.sleep(1)

        self.assertEqual(self.test_mulebot.dcMotorPWMDurationLeft, 1023)





if __name__ == "__main__":

    unittest.main()
