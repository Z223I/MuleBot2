import sys
sys.path.append("/home/pi/pythondev/RangeBot/RangeBot")

import time
import math

from RangeBot import RangeBot
from mulebot import MuleBot

range_bot = RangeBot(3)

bot = MuleBot()

bot.setMotorsDirection('f')

bot.motorSpeed(3.0, 3.0)
time.sleep(1.5)

#print("Duration: ", bot.dcMotorPWMDurationLeft)

if True:
                  angle_rad = math.radians(2)

                  bot.lidarNav_turn(angle_rad)

                  time.sleep(5)
                  bot.motorSpeed(0, 0)
