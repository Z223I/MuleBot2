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

    GPIO.add_event_detect(laserDetectFarLeftPin,  GPIO.FALLING, callback=myInt)
    GPIO.add_event_detect(laserDetectLeftPin,     GPIO.FALLING, callback=myInt)
    GPIO.add_event_detect(laserDetectCenterPin,   GPIO.FALLING, callback=myInt)
    GPIO.add_event_detect(laserDetectRightPin,    GPIO.FALLING, callback=myInt)
    GPIO.add_event_detect(laserDetectFarRightPin, GPIO.FALLING, callback=myInt)


  def shutdown(self):
    GPIO.cleanup()
    print
    print "Bye!"  




def write(_string):
    with open("log.txt", "a") as log:
        log.write( "{0}\n".format( _string ) )
    log.close()

def record( message ):
    print( message )
#    write( message )
    shellCommand = "ssh pi@rpi-one \'/home/pi/pythondev/MuleBot2/"
    shellCommand += message
    shellCommand += ".sh\'"
    os.system( shellCommand )

def myInt(channel):

  global laserDetectFarLeftPin
  global laserDetectLeftPin
  global laserDetectCenterPin
  global laserDetectRightPin
  global laserDetectFarRightPin

  if channel == laserDetectFarLeftPin:
    record( "FarLeft" )

  if channel == laserDetectLeftPin:
    record( "Left" )

  if channel == laserDetectCenterPin:
    record( "Center" )

  if channel == laserDetectRightPin:
    record( "Right" )

  if channel == laserDetectFarRightPin:
    record( "FarRight" )







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






mb = LaserDetector()

#myInt(6)
#myInt(19)
#myInt(21)
#myInt(13)
#myInt(26)

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



mb.shutdown()
# exception keyboard
# cleanup pwm
#pwm.cleanup()



