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
    MAX_VELOCITY_METERS_PER_SEC = 3.830227695
    SECONDS_PER_MINUTE = 60
    MAX_RPM = 12
    RADIANS_PER_REV = 2
    MAX_VELOCITY_RADS_PER_SEC = MAX_RPM / SECONDS_PER_MINUTE * RADIANS_PER_REV

    def setUp(self):
        self.test_mulebot = MuleBot()

    def tearDown(self):
        pass

    def test_class_variables(self):
        self.assertEqual(MuleBot.WHEEL_RADIUS, 2)
        self.assertEqual(MuleBot.WHEEL_BASE_LENGTH, 20)


    def test_velocity_check_A(self):
        """test_velocity_check_A
        If the velocities are the same, a turn isn't required.
        """
        v_l = 0
        v_r = 0
        v_l_ret, v_r_ret, duration = self.test_mulebot.velocity_check(v_l, v_r)

        duration_check = 0
        self.assertEqual(v_l_ret, v_l)
        self.assertEqual(v_r_ret, v_r)
        self.assertEqual(duration, duration_check)

        v_l = MuleBot.MAX_RPS
        v_r = MuleBot.MAX_RPS
        v_l_ret, v_r_ret, duration = self.test_mulebot.velocity_check(v_l, v_r)

        duration_check = 0
        self.assertEqual(v_l_ret, v_l)
        self.assertEqual(v_r_ret, v_r)
        self.assertEqual(duration, duration_check)

    def test_velocity_check_B(self):
        """test_velocity_check_B
        If the velocities are within +-MAX_RPS, the turn can be completed
        in one second.
        """
        v_l = MuleBot.MAX_RPS
        v_r = -MuleBot.MAX_RPS
        v_l_ret, v_r_ret, duration = self.test_mulebot.velocity_check(v_l, v_r)

        duration_check = 1
        self.assertEqual(v_l_ret, v_l)
        self.assertEqual(v_r_ret, v_r)
        self.assertEqual(duration, duration_check)


    def test_velocity_check_C(self):
        """test_velocity_check_C
        Set the velocities outside of +-MAX_RPS, and make sure the duration
        is over one second.
        """

        multiple = 2.0

        v_l = MuleBot.MAX_RPS * multiple
        v_r = -MuleBot.MAX_RPS * multiple
        v_l_ret, v_r_ret, duration = self.test_mulebot.velocity_check(v_l, v_r)

        duration_check = multiple
        self.assertEqual(v_l_ret, MuleBot.MAX_RPS)
        self.assertEqual(v_r_ret, -MuleBot.MAX_RPS)
        self.assertEqual(duration, duration_check)



    def test_v_1(self):
        # vel and check_vel_m are in meters per second
        self.test_mulebot.dcMotorPWMDurationLeft = 4095
        vel = int(self.test_mulebot.v() * 10000) / 10000

        check_vel_m = MuleBot.CIRCUM_M * MuleBot.MAX_RPM

        # Convert to per second
        check_vel_m = check_vel_m / MuleBot.SECONDS_PER_MINUTE

        check_vel_m = int(check_vel_m * 10000) / 10000
        print("check_vel_m: ", check_vel_m)

        self.assertEqual(vel, check_vel_m)

        self.test_mulebot.dcMotorPWMDurationLeft = 0
        self.assertEqual(self.test_mulebot.v(), 0)

    def test_v_2(self):
        """test_v_2 uses two different instances of MuleBot. During testing 
        it was discovered that this was causing a problem."""

        test_mulebot2 = MuleBot()

        rpm = MuleBot.MAX_RPM
        self.test_mulebot.motorSpeed(rpm, rpm)

        mps = self.test_mulebot.v()
        mps2 = test_mulebot2.v()

        self.assertEqual(mps, mps2)








    def test___init___(self):
        self.assertEqual(self.test_mulebot._running, True)
        self.assertEqual(self.test_mulebot.distanceToWall, 0)
        self.assertEqual(self.test_mulebot.pwmEnablePin, 16)
        self.assertEqual(self.test_mulebot.motor1DirectionPin, 20)
        self.assertEqual(self.test_mulebot.motor2DirectionPin, 21)

        self.assertEqual(self.test_mulebot.motorForward, GPIO.HIGH)
        self.assertEqual(self.test_mulebot.motorReverse, GPIO.LOW)

# TODO: Finish this.



    def test_mps_to_rps(self):

        # Set velocity (meters per second) to the circumference of the wheel
        # in meters.
        v_mps = MuleBot.CIRCUM_M
        v_rps = self.test_mulebot.mps_to_rps(v_mps)

        self.assertEqual(v_rps, MuleBot.RADIANS_IN_CIRCLE)

    def test_rps_to_mps(self):

        # Set velocity (radians per second) to 2 which equals 360 degrees.
        v_rps = 2.0
        v_mps = self.test_mulebot.rps_to_mps(v_rps)

        self.assertEqual(v_mps, MuleBot.CIRCUM_M)

    def test_rps_to_rpm(self):
        """test_rps_to_rpm

        2 radians = 1 rpm by definition."""

        SECONDS_PER_MINUTES = 60
        v_rps = 2.0 / SECONDS_PER_MINUTES
        v_rpm = self.test_mulebot.rps_to_rpm(v_rps)

        v_rpm_check = 1.0
        self.assertEqual(v_rpm, v_rpm_check)










    def test_set_wheel_drive_rates_A(self):
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

    def test_set_wheel_drive_rates_B(self):
        # These numbers are from a test.

        vel_l = 6.0 / TestMuleBot.SECONDS_PER_MINUTE # (radians per second)
        vel_r = 6.0 / TestMuleBot.SECONDS_PER_MINUTE # (radians per second)

        rpm_l, rpm_r = self.test_mulebot.set_wheel_drive_rates(vel_l, vel_r)
        rpm_l = int(rpm_l * 1000) / 1000

        self.assertEqual(rpm_l, 3.0)
        self.assertEqual(rpm_r, 3.0)

    def test__uni_to_diff_A(self):
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

    def test__uni_to_diff_B(self):
        v = 0.9569
        omega = 0.1356

        v_l, v_r = self.test_mulebot._uni_to_diff(v, omega)
        # v_l and v_r in radians per second. v is in meters per second.

        circum_in = 2.0 * math.pi * MuleBot.WHEEL_RADIUS
        circum_m = circum_in / 39.3701

        left_v = v_l * circum_m / 2
        right_v = v_r * circum_m / 2

        self.assertLess(left_v, v)
        self.assertGreater(right_v, v)

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

    def test_motorSpeed_A(self):
        """test_motorSpeed_A sets bot wheels to zero rpm and then checks the pwmDuration.
        """
        rpm = 0

        self.test_mulebot.motorSpeed(rpm, rpm)

        self.assertEqual(self.test_mulebot.dcMotorPWMDurationLeft, 0)

    def test_motorSpeed_B(self):
        """test_motorSpeed_A sets bot wheels to zero rpm and then checks the pwmDuration.
        """
        rpm = self.test_mulebot.motorMaxRPM

        self.test_mulebot.motorSpeed(rpm, rpm)

        self.assertEqual(self.test_mulebot.dcMotorPWMDurationLeft, 4095)


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
