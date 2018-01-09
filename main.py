import threading
import Queue
import time

#from LL3Threaded.LidarLiteChild import LidarLiteChild
from LidarLiteChild import LidarLiteChild
from Pro2 import Pro2

#from Con1 import Con1
from mulebot import MuleBot as Con1


lidarLiteChild = LidarLiteChild()
lidarLiteChild.init()

pro2 = Pro2()
con1 = Con1()
con2 = Con1()

qNumbers  = Queue.Queue(maxsize=0)
qCommands = Queue.Queue(maxsize=0)
qQuit     = Queue.Queue(maxsize=0)

lidarLiteChildThread  = threading.Thread(target=lidarLiteChild.run, args=(qNumbers,))
pro2Thread  = threading.Thread(target=pro2.run, args=(qCommands, qQuit, ))
con1Thread1 = threading.Thread(target=con1.run1, args=(qNumbers,))
con2Thread2 = threading.Thread(target=con2.run2, args=(qCommands, ))

lidarLiteChildThread.start()
pro2Thread.start()
con1Thread1.start()
con2Thread2.start()

qQuit.get()
qQuit.task_done()


print "Recieved quit command:"

lidarLiteChild.terminate()
pro2.terminate()
con1.terminate()
con2.terminate()
print "terminated 4 threads"


qCommands.join()
print "joined 1 queue(s)"
qQuit.join()
print "joined 2 queue(s)"
qNumbers.join()
print "joined 3 queue(s)"


print "Bye!"
