#!/usr/bin/python

import RPi.GPIO as GPIO



class MuleBot:
  def __init__(self):

    global GPIO




    self.laserDetectLeftPin  = 6
    self.laserDetectRightPin = 5





    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

    # This is interupts setups.  They get used with the
    # myInt() method.
    GPIO.setup(self.laserDetectLeftPin,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(self.laserDetectRightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(self.laserDetectLeftPin,  GPIO.FALLING, callback=myInt)
    GPIO.add_event_detect(self.laserDetectRightPin, GPIO.FALLING, callback=myInt)












  def shutdown(self):
    GPIO.cleanup()
    print
    print "Bye!"  














def myInt(channel):

  laserDetectLeftPin  = 6
  laserDetectRightPin = 5

  if channel == laserDetectLeftPin:
    print "Detected LEFT laser."


  if channel == laserDetectRightPin:
    print "Detected RIGHT laser."







def test():
  laserOn = 0
  lastLaserOn = -1

  startTime = time.time()  # This will get overwritten
  finishTime = time.time()
  lastTime = time.time()

  count = 0
  maxEvents = 20
  while count < maxEvents:
    laserOn = GPIO.input(laserDetectLeftPin)
    #print laserOn

    if lastLaserOn == 0:
      if laserOn ==1:
        now = time.time()
        deltaTime = now - lastTime
        if deltaTime > 3.8:
          print deltaTime
          lastTime = now
          if deltaTime > 4.3:
            startTime = now
          else:
            count += 1
            finishTime = now

    lastLaserOn = laserOn

    time.sleep(.01)

  totalDeltaTime = finishTime - startTime
  singleDeltaTime = totalDeltaTime / maxEvents
  print singleDeltaTime, " * ", maxEvents, " = ", totalDeltaTime






mb = MuleBot()


doContinue = True

try:
  while (doContinue):

    cmd = raw_input(":;<  Command, f/r 0..9, E.g. f5: ")
    command = cmd[0]

    if command == 'h':
      doContinue = False
    elif command == 't':
      test()
    else:
      print "Invalid input: ", command
      print "Please try again."


except KeyboardInterrupt:
  pass



mb.shutdown()
# exception keyboard
# cleanup pwm
#pwm.cleanup()
