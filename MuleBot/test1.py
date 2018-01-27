import sys
sys.path.append("/home/pi/pythondev/RangeBot/RangeBot")
from RangeBot import RangeBot

from mulebot import MuleBot

range_bot = RangeBot(3)

bot = MuleBot()

bot.setMotorsDirection('f')

bot.motorSpeed(3.0, 3.0)

print("Duration: ", bot.dcMotorPWMDurationLeft)

if True:
              target_range = 30
              target_width = 22

              v = bot.v()
              print
              print("aMuleBot.lidarNav: v (m/s): ", v)
              print("bMuleBot.lidarNav: target_range: ", target_range)
              print("cMuleBot.lidarNav: target_width: ", target_width)

              angle, tgt_range, hits = \
                  range_bot.execute_hunt(target_range, target_width)
              v = bot.v()
              print
              print("dMuleBot.lidarNav: v (m/s): ", v)
              print("eMuleBot.lidarNav: angle (deg): ", angle)
              print("fMuleBot.lidarNav: tgt_range (inches): ", tgt_range)

              target_range, angle_rad  = \
                  bot.lidarNav_should_i_stay_or_should_i_go(tgt_range, angle)
              v = bot.v()
              print
              print("gMuleBot.lidarNav: v (m/s): ", v)
              print("hMuleBot.lidarNav: target_range: ", target_range)
              print("iMuleBot.lidarNav: angle_rad: ", angle_rad)
              input("Press [Enter] to continue.")

              # Is a turn required?
              if target_range > 0 and not (angle_rad == 0):
                  # A turn is required.

                  # What is our current velocity (m/s)
                  v = bot.v()
                  print("jMuleBot.lidarNav: v (m/s): ", v)
                  input("Press [Enter] to continue.")






                  print("kMuleBot.lidarNav: v (m/s): ", v)
                  print("lMuleBot.lidarNav: angle_rad): ", angle_rad)
                  bot.lidarNav_turn(v, angle_rad)
                  time.sleep(0.25)

