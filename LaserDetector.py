#!/usr/bin/python

import RPi.GPIO as GPIO
import os


laserDetectFarLeftPin  =  6
laserDetectLeftPin     = 19
laserDetectCenterPin   = 21
laserDetectRightPin    = 13
laserDetectFarRightPin = 26


class LaserDetector:

  global laserDetectFarLeftPin
  global laserDetectLeftPin
  global laserDetectCenterPin
  global laserDetectRightPin
  global laserDetectFarRightPin

  def __init__(self):

    global GPIO

    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

    # This is interupts setups.  They get used with the
    # myInt() method.
    GPIO.setup(laserDetectFarLeftPin,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(laserDetectLeftPin,     GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(laserDetectCenterPin,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(laserDetectRightPin,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(laserDetectFarRightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(laserDetectFarLeftPin,  GPIO.FALLING, callback=self.myInt)
    GPIO.add_event_detect(laserDetectLeftPin,     GPIO.FALLING, callback=self.myInt)
    GPIO.add_event_detect(laserDetectCenterPin,   GPIO.FALLING, callback=self.myInt)
    GPIO.add_event_detect(laserDetectRightPin,    GPIO.FALLING, callback=self.myInt)
    GPIO.add_event_detect(laserDetectFarRightPin, GPIO.FALLING, callback=self.myInt)


  def shutdown(self):
    GPIO.cleanup()
    print
    print "Bye!"  




  def write(self, _string):
      with open("log.txt", "a") as log:
          log.write( "{0}\n".format( _string ) )
      log.close()

  def record( self, message ):
      print( message )
  #    write( message )
      shellCommand = "ssh pi@rpi-one \'/home/pi/pythondev/MuleBot2/"
      shellCommand += message
      shellCommand += ".sh\'"
      os.system( shellCommand )

  def myInt(self, channel):

#    global laserDetectFarLeftPin
#    global laserDetectLeftPin
#    global laserDetectCenterPin
#    global laserDetectRightPin
#    global laserDetectFarRightPin

    if channel == laserDetectFarLeftPin:
      self.record( "FarLeft" )

    if channel == laserDetectLeftPin:
      self.record( "Left" )

    if channel == laserDetectCenterPin:
      self.record( "Center" )

    if channel == laserDetectRightPin:
      self.record( "Right" )

    if channel == laserDetectFarRightPin:
      self.record( "FarRight" )







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






ld = LaserDetector()

#ld.myInt(6)
#ld.myInt(19)
#ld.myInt(21)
#ld.myInt(13)
#ld.myInt(26)

doContinue = True

try:
  while (doContinue):

    cmd = raw_input("Command, [h, t]: ")
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



ld.shutdown()
# exception keyboard
# cleanup pwm
#pwm.cleanup()



