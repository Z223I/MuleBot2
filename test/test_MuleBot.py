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

import sys
sys.path.append('/home/pi/pythondev/MuleBot2/MuleBot')
#print(sys.path)
from mulebot import MuleBot
import RPi.GPIO as GPIO


class TestMuleBot(unittest.TestCase):
    MAX_VELOCITY_RADS_PER_SEC = 1.256637061436
    MAX_VELOCITY_METERS_PER_SEC = 3.830227695
    SECONDS_PER_MINUTE = 60

    def setUp(self):
        self.test_mulebot = MuleBot()

    def tearDown(self):
        pass

    def test_class_variables(self):
        self.assertEqual(MuleBot.WHEEL_RADIUS, 2)
        self.assertEqual(MuleBot.WHEEL_BASE_LENGTH, 20)

    def test_v(self):
        # vel and check_vel_m are in meters per second
        self.test_mulebot.dcMotorPWMDurationLeft = 4095
        vel = int(self.test_mulebot.v() * 10000) / 10000

        circum_in = 2 * math.pi * MuleBot.WHEEL_RADIUS

        check_vel_in = self.test_mulebot.motorMaxRPM * circum_in

        INCHES_PER_METER = 39.3701
        check_vel_m = check_vel_in / INCHES_PER_METER


        check_vel_m = int(check_vel_m * 10000) / 10000
        print("check_vel_m: ", check_vel_m)

        self.assertEqual(vel, check_vel_m)

        self.test_mulebot.dcMotorPWMDurationLeft = 0
        self.assertEqual(self.test_mulebot.v(), 0)

    def test___init___(self):
        self.assertEqual(self.test_mulebot._running, True)
        self.assertEqual(self.test_mulebot.distanceToWall, 0)
        self.assertEqual(self.test_mulebot.pwmEnablePin, 16)
        self.assertEqual(self.test_mulebot.motor1DirectionPin, 20)
        self.assertEqual(self.test_mulebot.motor2DirectionPin, 21)

        self.assertEqual(self.test_mulebot.motorForward, GPIO.HIGH)
        self.assertEqual(self.test_mulebot.motorReverse, GPIO.LOW)

# TODO: Finish this.


    def test_set_wheel_drive_rates(self):
        vel_l = TestMuleBot.MAX_VELOCITY_RADS_PER_SEC
        vel_r = 0.0

        rpm_l, rpm_r = self.test_mulebot.set_wheel_drive_rates(vel_l, vel_r)
        rpm_l = int(rpm_l * 1000) / 1000

        self.assertEqual(rpm_l, 12)
        self.assertEqual(rpm_r, 0)

        vel_r = TestMuleBot.MAX_VELOCITY_RADS_PER_SEC
        vel_l = 0.0
        rpm_l, rpm_r = self.test_mulebot.set_wheel_drive_rates(vel_l, vel_r)
        rpm_r = int(rpm_r * 1000) / 1000
        self.assertEqual(rpm_l, 0)
        self.assertEqual(rpm_r, 12)

    def test__uni_to_diff(self):
        v = TestMuleBot.MAX_VELOCITY_METERS_PER_SEC
        omega = 0.0

        v_l, v_r = self.test_mulebot._uni_to_diff(v, omega)
        # v_l and v_r in radians per second. v is in meters per second.

        circum_in = 2.0 * math.pi * MuleBot.WHEEL_RADIUS
        circum_m = circum_in / 39.3701

        left_v = v_l * circum_m / 2
        right_v = v_r * circum_m / 2

        self.assertEqual(left_v, v)
        self.assertEqual(right_v, v)

    def test_motorDirection(self):
        pass

    def test_motorsDirection(self):
        pass

    def test_dcMotorLeftTurn(self):
        pass

    def test_dcMotorRightTurn(self):
        pass

    def test_constrainSpeed(self):
        # TODO
        pass

    def test_motorSpeed(self):
        # TODO
        pass

    def test_run1(self):
        pass

    def test_run2(self):
        pass

    def test_lidarNav_queue_check_A(self):
        """test_lidarNav_queue_check_A uses an empty queue.  There should be
        no change to the variables."""
        q_lidar_nav = queue.Queue(maxsize=0)
        target_range = 3
        target_width = 4

        ret_target_range, ret_target_width = \
            self.test_mulebot.lidarNav_queue_check( \
            q_lidar_nav, target_range, target_width)

        self.assertEqual(ret_target_range, target_range)
        self.assertEqual(ret_target_width, target_width)

    def test_lidarNav_queue_check_B(self):
        """test_lidarNav_queue_check_B uses a queue with a range command.  
        only the range variable should change."""
        q_lidar_nav = queue.Queue(maxsize=0)

        queue_range = 43
        q_lidar_nav.put("R" + str(queue_range))

        target_range = 3
        target_width = 4

        ret_target_range, ret_target_width = \
            self.test_mulebot.lidarNav_queue_check( \
            q_lidar_nav, target_range, target_width)

        self.assertEqual(ret_target_range, queue_range)
        self.assertEqual(ret_target_width, target_width)

    def test_lidarNav_queue_check_C(self):
        """test_lidarNav_queue_check_C uses a queue with a width command.  
        only the width variable should change."""
        q_lidar_nav = queue.Queue(maxsize=0)

        queue_width = 444
        q_lidar_nav.put("w" + str(queue_width))

        target_range = 3
        target_width = 4

        ret_target_range, ret_target_width = \
            self.test_mulebot.lidarNav_queue_check( \
            q_lidar_nav, target_range, target_width)

        self.assertEqual(ret_target_range, target_range)
        self.assertEqual(ret_target_width, queue_width)

    def test_lidarNav_should_i_stay_or_should_i_go_A(self):
        """test_lidarNav_should_i_stay_or_should_i_go_A sets the target
        range small enough to stop MuleBot"""

        tgt_range = self.test_mulebot.tgt_min_range - 1
        angle = 45

        target_range, angle_rad = \
            self.test_mulebot.lidarNav_should_i_stay_or_should_i_go(tgt_range, angle)

        # target_range should be zero because we are too close to the target.
        self.assertEqual(target_range, 0)

        # We don't care about the angle if the range is zero.

    def test_lidarNav_should_i_stay_or_should_i_go_B(self):
        """test_lidarNav_should_i_stay_or_should_i_go_A sets the target
         range large enough to MuleBot rolling"""

        tgt_range = self.test_mulebot.tgt_min_range + 1
        angle = 45

        target_range, angle_rad = \
            self.test_mulebot.lidarNav_should_i_stay_or_should_i_go(tgt_range, angle)

        # target_range should be the same.
        self.assertEqual(target_range, tgt_range)

        # The angle should be converted to radians
        self.assertEqual(angle_rad, math.radians(angle))

    def test_lidarNav_turn_A(self):
        """test_lidarNav_turn_A does a check to make sure there isn't a turn
        when omega is 0."""

        v = TestMuleBot.MAX_VELOCITY_RADS_PER_SEC
        angle_rads = 0
        v_l, v_r = self.test_mulebot.lidarNav_turn(v, angle_rads)

        self.assertEqual(v_l, v)
        self.assertEqual(v_r, v)


    def test_lidarNav(self):
        pass

    def test_laserNav(self):
        # No.  This method needs deleted.
        pass

    def test_setMotorsDirection(self):
        pass

    def test_shutDown(self):
        pass




    def test_motorSpeed_A(self):
        rpm_left = 0
        rpm_right = 0
        self.test_mulebot.motorSpeed(rpm_left, rpm_right)
        self.assertEqual(self.test_mulebot.dcMotorPWMDurationLeft, 0)
        self.assertEqual(self.test_mulebot.dcMotorPWMDurationRight, 0)

    def test_motorSpeed_B(self):
        rpm_left = 12
        rpm_right = 12
        self.test_mulebot.motorSpeed(rpm_left, rpm_right)
        self.assertEqual(self.test_mulebot.dcMotorPWMDurationLeft, 4095)
        # Can't actually test non-zero rpm for the right wheel, because
        # it has been adjusted due to it was too fast.

        # TODO: Store the const adjustment as a class variable.
        # retrieve that value, adjust and then test.
        #self.assertEqual(self.test_mulebot.dcMotorPWMDurationRight, 4095)

    def test_motorSpeed_C(self):
        rpm_left = 6
        rpm_right = 6
        self.test_mulebot.motorSpeed(rpm_left, rpm_right)
        self.assertEqual(self.test_mulebot.dcMotorPWMDurationLeft, 2047)
        # Can't actually test non-zero rpm for the right wheel, because
        # it has been adjusted due to it was too fast.

        # TODO: Store the const adjustment as a class variable.
        # retrieve that value, adjust and then test.
        #self.assertEqual(self.test_mulebot.dcMotorPWMDurationRight, 2047)


if __name__ == "__main__":

    unittest.main()
