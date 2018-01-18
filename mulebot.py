#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
#import datetime
#channel = 6

import RPi.GPIO as GPIO
import threading
import queue
import re
import os


class MuleBot:

  def __init__(self):

    global GPIO

    # running is used to control thread execution.
    self._running = True

    # Keep MuleBot parallel to the wall at this distance.
    self.distanceToWall = 0


    self.pwmEnablePin       = 16 # Broadcom pin 16
    self.motor1DirectionPin = 20 # Broadcom pin 20
    self.motor2DirectionPin = 21 # Broadcom pin 21

    self.motorForward = GPIO.HIGH
    self.motorReverse = GPIO.LOW


    self.dcMotorLeftMotor  = 0
    self.dcMotorRightMotor = 1
    
    self.dcMotorPWMDurationLeft = 0
    self.dcMotorPWMDurationRight = 0

    self.laserDetectLeftPin  = 6
    self.laserDetectRightPin = 5

    self.motorMaxRPM = 12

    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    GPIO.setup(self.pwmEnablePin,       GPIO.OUT)
    GPIO.setup(self.motor1DirectionPin, GPIO.OUT)
    GPIO.setup(self.motor2DirectionPin, GPIO.OUT)

    GPIO.output(self.pwmEnablePin,       GPIO.LOW )

    # This is interupts setups.  They get used with the
    # test() method.
    #GPIO.setup(laserDetectLeftPin,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(laserDetectRightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    #GPIO.add_event_detect(laserDetectLeftPin,  GPIO.FALLING, callback=myInt)
    #GPIO.add_event_detect(laserDetectRightPin, GPIO.FALLING, callback=myInt)


    # Initialise the PWM device using the default address
    self.pwm = PWM(0x40)
    # Note if you'd like more debug output you can instead run:
    #pwm = PWM(0x40, debug=True)


    #count = 1
    self.pwm.setPWMFreq(1000)                        # Set frequency to 1000 Hz


  def terminate(self):
    self._running = False


  # I don't think setServoPulse is ever called.
  # Is the pulse parameter ever used?

  #servoMin = 4096 / 12  # Min pulse length out of 4096
  #servoMax = 4095       # Max pulse length out of 4096

  def setServoPulse(channel, pulse):
    pulseLength = 1000000                   # 1,000,000 us per second
    pulseLength /= 60                       # 60 Hz
    print ("%d us per period" % pulseLength)
    pulseLength /= 4096                     # 12 bits of resolution
    print ("%d us per bit" % pulseLength)
    pulse *= 1000
    pulse /= pulseLength
    self.pwm.setPWM(channel, 0, pulse)


  def motorDirection(self, motorPin, direction):
  #  print "motorPin: ", motorPin
  #  print "direction: ",  direction
    GPIO.output(motorPin, direction)


  def motorsDirection(self, direction):
    print (direction)
    if direction == 'r' or direction == 'R':
      self.motorDirection(self.motor1DirectionPin, self.motorReverse)
      self.motorDirection(self.motor2DirectionPin, self.motorReverse)
      print ("Direction reverse")
    else:
      self.motorDirection(self.motor1DirectionPin, self.motorForward)
      self.motorDirection(self.motor2DirectionPin, self.motorForward)
      print ("Direction forward")

  def dcMotorLeftTurn(self, duration):
    print ("From dcMotorLeftTurn: ", self.dcMotorPWMDurationLeft)
    tempPWMDurationLeft = int( self.dcMotorPWMDurationLeft * 70 / 100 )  # 98
    self.pwm.setPWM(self.dcMotorLeftMotor, 0, tempPWMDurationLeft)

    # Duration of the turn  
    time.sleep(duration)

    # Go straight
    self.pwm.setPWM(self.dcMotorLeftMotor, 0, self.dcMotorPWMDurationLeft)


  def dcMotorRightTurn(self, duration):
    tempPWMDurationRight = int( self.dcMotorPWMDurationRight * 70 / 100 )
    self.pwm.setPWM(self.dcMotorRightMotor, 0, tempPWMDurationRight)

    # Duration of the turn  
    time.sleep(duration)

    # Go straight
    self.pwm.setPWM(self.dcMotorRightMotor, 0, self.dcMotorPWMDurationRight)


  def motorSpeed(self, speedRPM):

    #global dcMotorPWMDurationLeft
    #global dcMotorPWMDurationRight
    intSpeedRPM = int( speedRPM )

    print ( "motorSpeed RPM: ", speedRPM )
    if intSpeedRPM > self.motorMaxRPM:
      speedRPM = 12



      #TODO: What is going on here?  Should there be 
      #      two different variables?


    if intSpeedRPM < 0:
      speedRPM = 0

    print ( "motorSpeed RPM adjusted: ", speedRPM )

#   Left motor
    pwmDuration = 4096 * intSpeedRPM / self.motorMaxRPM - 1
    pwmDuration = int( pwmDuration )
    self.pwm.setPWM(self.dcMotorLeftMotor, 0, pwmDuration)
    self.dcMotorPWMDurationLeft = pwmDuration

#   Right motor
    #Adjust for right motor being faster
    pwmDuration = pwmDuration * 9851 / 10000  # x97.019779 percent 98.519113
    pwmDuration = int( pwmDuration )
    self.pwm.setPWM(self.dcMotorRightMotor, 0, pwmDuration)
    self.dcMotorPWMDurationRight = pwmDuration


  def init(self):

    junk = 0
    # This is all interupt stuff for calibrating the speed
    # of the wheels.
    #self.interruptLeftCount  = -2
    #self.interruptRightCount = -2
    #self.startTimeLeft  = 0
    #self.startTimeRight = 0
    #self.lastTimeLeft   = 0
    #self.lastTimeRight  = 0



  def run1(self, _q1, _q2,_qWallDistance):

      """This method, run1, is used to navigate the MuleBot to
       a desired distance from the wall.

       This method is a thread.

       _q1 is the current distance to the wall.
       _qWallDistance is used occasionally to establish
       the desire distance.

       _q2 is used to send steering directions to the run2 thread."""


      timeInRightTurn = 0
      timeInLeftTurn = 0

      while self._running:
          #name = threading.currentThread().getName()
          #print "Consumer thread 1:  ", name

          # This method is the only consumer of _qWallDistance.
          # Therefore checking if the queue is empty works.
          # In a multi-consumer environment, check empty()
          # can cause a race condition.
          if _qWallDistance.empty():
              pass
          else:
              self.distanceToWall = _qWallDistance.get()
              _qWallDistance.task_done()






          currentDistance = _q1.get();
#          print ("Current distance: ", currentDistance)

          qSize = _q1.qsize()
          if qSize > 1:
            print ( "***** Distance Queue Size: ", qSize, " *****" )

          # Are we navigating?
          navigating = (self.distanceToWall > 0)
          if navigating:
              print ("Desired distance: ", self.distanceToWall)

              accuracy = 0.5
              # Navigate
              if currentDistance < self.distanceToWall - accuracy:
                  print ("Turn right >>>")
                  timeInRightTurn += 1
                  _q2.put('s1')
              elif currentDistance > self.distanceToWall + accuracy:
                  print ("Turn left <<<")
                  timeInLeftTurn += 1
                  _q2.put('p1')
              else:
                  if ( timeInRightTurn > 0 ):
                      for i in range( timeInRightTurn ):
                          _q2.put('p1')
                      # Reset the time
                      timeInRightTurn = 0
                  if ( timeInLeftTurn > 0 ):
                      for i in range( timeInLeftTurn ):
                          _q2.put('s1')
                      # Reset the time
                      timeInLeftTurn = 0
                  print ("On path.")
          # end if 

          _q1.task_done()


 
  def intFromStr( self, _string, _index ):
      list = re.findall( r'\d+', _string )
      return int( list[_index] )

  """ run2 is a thread """

  def run2(self, _q2, _qWallDistance):
        while self._running:
                name = threading.currentThread().getName()
                print ("Consumer thread 2:  ", name)
                qCommand = _q2.get();
                print ("Here is the command... ", qCommand)
                print


                qSize = _q2.qsize()
                if qSize > 1:
                  print ( "***** Command Queue Size: ", qSize, " *****" )



                # Change speed of motors
                qCommand = qCommand.lower()
                cmd = qCommand
                command = cmd[0]

                if command == 'h':
                  pass
                elif command == 'p':
                  index = 0
                  count = self.intFromStr( cmd, index )
                  print ("Left Turn, ", count, " seconds")
                  self.dcMotorLeftTurn (  count  )
                elif command == 's':
                  index = 0
                  count = self.intFromStr( cmd, index )
                  print ("Right Turn, ", count, " seconds")
                  self.dcMotorRightTurn( count  )
                elif command == 't':
                  self.test()
                elif command == 'f' or command == 'r':
                  direction = command
                  print (direction)
                  self.setMotorsDirection(direction)

                  index = 0
                  speed = self.intFromStr( cmd, index )

                  self.motorSpeed(speed)
                elif command == 'd':
                  index = 0
                  inches = self.intFromStr( cmd, index )
                  _qWallDistance.put( inches )
                else:
                  print ("Invalid input: ", command)
                  print ("Please try again.")


                #time.sleep(4)
                _q2.task_done()
        # End while


        time.sleep(2)
        self.shutdown()


  """ Name:  laserNav
      Date:  January 2018

      Arguments:  self

      Purpose:  laserNav monitors the Laser Detector' state.
                The Laser Detector's computer executes a shell 
                script on the MuleBot's computer to establish a
                file whos name indicates the current state.

                Each file has the name format of '*.loc'.

                The state of the Laser Detector changes so slowly,
                that using files is probably fast enough.
  """
                

  def laserNav( self, _qCommands ):
      try:
          # At start of the thread, delete all loc[ation] files.
          os.system( "rm *.loc" )
      except:
          pass


      while self._running:
          files = os.listdir("/home/pi/pythondev/MuleBot2/")
          
          for file in files:
              # Looking for files ending in ".loc"
              if file.endswith(".loc"):
                  print ( file )
                  command = "rm " + file
                  os.system( command )

                  # Determine which of the six states that the
                  # Laser Detector is in.
                  if file == "LO_FL.loc":
                      _qCommands.put("S6")
                  elif file == "LO_L.loc":
                      _qCommands.put("S3")
                      pass
                  elif file == "LO_C.loc":
                      pass
                  elif file == "RO_C.loc":
                      pass
                  elif file == "RO_R.loc":
                      _qCommands.put("P3")
                  elif file == "RO_FR.loc":
                      _qCommands.put("P6")
                  else:
                      print( file, " is an invalid state name" )

          time.sleep(0.5)



  def setMotorsDirection(self, _direction):
    if _direction == 'f' or _direction == 'F':
      self.motorDirection(self.motor1DirectionPin, self.motorForward)
      self.motorDirection(self.motor2DirectionPin, self.motorForward)
    elif _direction == 'r' or _direction == 'R':
      self.motorDirection(self.motor1DirectionPin, self.motorReverse)
      self.motorDirection(self.motor2DirectionPin, self.motorReverse)
    else:
      print ("ERROR: setMotorsDirection bad parameter: " + direction)

  def shutdown(self):
    count = 0
    self.pwm.setPWM(0, 0, count)
    self.pwm.setPWM(1, 0, count)

    ### How to use the Enable Pin???
    #TODO:  Put this back in.
    #GPIO.output(pwmEnablePin, GPIO.HIGH)
    GPIO.cleanup()
    print
    print ("Good Bye!")










def myInt(channel):
  global interruptLeftCount
  global interruptRightCount
  global startTimeLeft
  global startTimeRight


  now = time.time()

  if channel == laserDetectLeftPin:
    interruptLeftCount += 1
    elapsedTime = 0.0
#    print channel, interruptLeftCount

    if interruptLeftCount == 1:
      startTimeLeft = now

    if interruptLeftCount > 0:
      elapsedTime = now - startTimeLeft
    print ("Left ", channel, now, interruptLeftCount, elapsedTime)


  if channel == laserDetectRightPin:
    interruptRightCount += 1
    elapsedTime = 0.0
#    print channel, interruptRightCount

    if interruptRightCount == 1:
      startTimeRight = now

    if interruptRightCount > 0:
      elapsedTime = now - startTimeRight
    print ("Right ", channel, now, interruptRightCount, elapsedTime)






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
          print (deltaTime)
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
  print (singleDeltaTime, " * ", maxEvents, " = ", totalDeltaTime)

