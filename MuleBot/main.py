import threading
import queue
import time

#from LL3Threaded.LidarLiteChild import LidarLiteChild
from LidarLiteChild import LidarLiteChild
from Pro2 import Pro2

#from Con1 import Con1
from mulebot import MuleBot as Con1


lidarLiteChild = LidarLiteChild()
lidarLiteChild.init()

pro2 = Pro2()
#con1 = Con1()
con2 = Con1()
stateLocation = Con1()
lidar_Nav = Con1()

qNumbers      = queue.Queue(maxsize=0)
qCommands     = queue.Queue(maxsize=0)
qQuit         = queue.Queue(maxsize=0)
qWallDistance = queue.Queue(maxsize=0)


lidarLiteChildThread  = threading.Thread(target=lidarLiteChild.run, args=(qNumbers,))
pro2Thread  = threading.Thread(target=pro2.run, args=(qCommands, qQuit, ))
#con1Thread1 = threading.Thread(target=con1.run1, args=(qNumbers, qCommands, qWallDistance, ))
con2Thread2 = threading.Thread(target=con2.run2, args=(qCommands, qWallDistance, ))
stateLocationThread = threading.Thread(target=stateLocation.laserNav, args=(qCommands, ))
lidarNavThread = threading.Thread(target=lidar_Nav.lidarNav, args=(qNumbers, qCommands, ))

lidarLiteChildThread.start()
pro2Thread.start()
#con1Thread1.start()
con2Thread2.start()
stateLocationThread.start()
lidarNavThread.start()

qQuit.get()
qQuit.task_done()


print ("Recieved quit command:")

lidarLiteChild.terminate()
pro2.terminate()
#con1.terminate()
con2.terminate()
stateLocation.terminate()
lidar_Nav.terminate()
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


print ("Bye!")