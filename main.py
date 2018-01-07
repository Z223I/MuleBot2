import threading
import Queue
import time

from Pro1 import Pro1
from Pro2 import Pro2
from Con1 import Con1

global isDone

isDone = False



pro1 = Pro1()
pro2 = Pro2()
con1 = Con1()
con2 = Con1()

qNumbers  = Queue.Queue(maxsize=0)
qCommands = Queue.Queue(maxsize=0)
qQuit     = Queue.Queue(maxsize=0)

pro1Thread  = threading.Thread(target=pro1.run, args=(qNumbers,))
pro2Thread  = threading.Thread(target=pro2.run, args=(qCommands, qQuit, ))
con1Thread1 = threading.Thread(target=con1.run1, args=(qNumbers,))
con2Thread2 = threading.Thread(target=con2.run2, args=(qCommands, ))

pro1Thread.start()
pro2Thread.start()
con1Thread1.start()
con2Thread2.start()

qQuit.get()
qQuit.task_done()


print "Recieved quit command:"

pro1.terminate()
pro2.terminate()
con1.terminate()
con2.terminate()
print "terminated 4 threads"

qNumbers.join()
qCommands.join()
qQuit.join()
print "joined 3 queues"


print "Bye!"
