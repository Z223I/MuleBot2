import threading
import queue
import time
import os

#from LidarLite3Ext import LidarLite3Ext
from Pro2 import Pro2

#from Con1 import Con1
from MuleBot import MuleBot as Con1
from Accessory import Accessory


#lidarLite3Ext = LidarLite3Ext()
#lidarLite3Ext.init()

# Delete existing log files.
try:
    os.remove("*.log")
except:
    pass

pro2 = Pro2()
#con1 = Con1()
con2 = Con1()
stateLocation = Con1()
lidar_Nav = Con1()
water_pump = Accessory()


qNumbers       = queue.Queue(maxsize=0)
qCommands      = queue.Queue(maxsize=0)
qQuit          = queue.Queue(maxsize=0)
qWallDistance  = queue.Queue(maxsize=0)
q_lidar_nav    = queue.Queue(maxsize=0)
q_water_pump   = queue.Queue(maxsize=0)


#lidarLite3ExtThread  = threading.Thread(target=lidarLite3Ext.run, args=(qNumbers,))
pro2Thread  = threading.Thread(target=pro2.run, args=(qCommands, qQuit, ))
#con1Thread1 = threading.Thread(target=con1.run1, args=(qNumbers, qCommands, qWallDistance, ))
con2Thread2 = threading.Thread(target=con2.run2, args= \
    (qCommands, qWallDistance, q_lidar_nav, q_water_pump))
stateLocationThread = threading.Thread(target=stateLocation.laserNav, args=(qCommands, ))
lidarNavThread = threading.Thread(target=lidar_Nav.lidarNav, args=(qCommands, q_lidar_nav))
w_p_Thread = threading.Thread(target=water_pump.water_pump, args=(q_water_pump,))

#lidarLite3ExtThread.start()
pro2Thread.start()
#con1Thread1.start()
con2Thread2.start()
stateLocationThread.start()
lidarNavThread.start()
w_p_Thread.start()

qQuit.get()
qQuit.task_done()


print ("Recieved quit command:")

#lidarLite3Ext.terminate()
pro2.terminate()
#con1.terminate()
con2.terminate()
stateLocation.terminate()
lidar_Nav.terminate()
water_pump.terminate()
print ("terminated 5 threads")

print ("3")
time.sleep(1)

print ("2")
time.sleep(1)

print ("1")
time.sleep(1)


qCommands.join()
print ("joined 1 queue(s)")
qQuit.join()
print ("joined 2 queue(s)")
qNumbers.join()
print ("joined 3 queue(s)")
qWallDistance.join()
print ("joined 4 queue(s)")
q_lidar_nav.join()
print ("joined 5 queue(s)")
water_pump.join()
print ("joined 6 queue(s)")

print ("Bye!")
