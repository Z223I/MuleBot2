#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import sys
sys.path.append("/home/pi/pythondev/RangeBot/RangeBot")
from RangeBot import RangeBot

import time

import RPi.GPIO as GPIO
import threading
import queue
import re
import os
import math

class MuleBot:

  """ Class MuleBot
  This class accepts driving commands from the keyboard and it also has
  a target mode where it drives to the target."""

  WHEEL_RADIUS = 2
  # Am pretty sure this is to be width.  Not length. The script is using
  # the distrance between the two motor driven wheels.
  WHEEL_BASE_LENGTH = 20

  def __init__(self):
    """__init__"""

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

    self.motorMaxRPM = 12.0

    # Pin Setup:
    GPIO.setwarnings(False)
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
    """terminate"""
    self._running = False

  def v(self):
      """v returns the velocity in m/s."""

      # PWM duration can go from 0 to 4095 with 4095 representing max rpm
      speed_percentage = float(self.dcMotorPWMDurationLeft) / 4095.0

      # Calculate max meters per minute
      wheel_circum_inches = 2.0 * math.pi * MuleBot.WHEEL_RADIUS
      max_inches_per_minute = wheel_circum_inches * self.motorMaxRPM
      inches_per_meter = 39.37
      max_m_per_minute = max_inches_per_minute / inches_per_meter

      m_per_s = speed_percentage * (max_m_per_minute / 60.0)

      return m_per_s

  # I don't think setServoPulse is ever called.
  # Is the pulse parameter ever used?

  #servoMin = 4096 / 12  # Min pulse length out of 4096
  #servoMax = 4095       # Max pulse length out of 4096

  def setServoPulse(channel, pulse):
    """setServoPulse"""

    pulseLength = 1000000                   # 1,000,000 us per second
    pulseLength /= 60                       # 60 Hz
    print ("%d us per period" % pulseLength)
    pulseLength /= 4096                     # 12 bits of resolution
    print ("%d us per bit" % pulseLength)
    pulse *= 1000
    pulse /= pulseLength
    self.pwm.setPWM(channel, 0, pulse)

  def set_wheel_drive_rates(self, v_l, v_r):
      """ set_wheel_drive_rates set the drive rates of the wheels to the 
      specified velocities (m/s).


      @type v_l:  float
      @param v_l: velocity left wheel (m/s)

      @type v_r: float
      @param v_r: velocity right wheel (m/s)

      """

      # Convert velocity from m/s to RPM
      SECONDS_PER_MINUTE = 60
      PI = math.pi
      INCHES_PER_METER = 39.3701

      # rpm = ( meters per minute ) * INCHES_PER_METER / wheel diameter (inches)
      rpm_l = (v_l * SECONDS_PER_MINUTE) * INCHES_PER_METER  / (MuleBot.WHEEL_RADIUS * 2 * PI)
      rpm_r = (v_r * SECONDS_PER_MINUTE) * INCHES_PER_METER  / (MuleBot.WHEEL_RADIUS * 2 * PI)

      self.motorSpeed(rpm_l, rpm_r)

  def _uni_to_diff(self, v, omega):
    """ _uni_to_diff The is a "unicycle model".  It performs a unicycle to 
    "differential drive model" mathematical translation.

    This came from the 'Sobot Rimulator' by Nick McCrea.

    @type v:  float
    @param v: velocity (m/s)

    @type omega: float
    @param omega: angular velocity (rad/s)

    @rtype: float
    @return: v_l velocity left wheel (m/s)

    @rtype: float
    @return: v_r velocity right wheel (m/s)"""

    # v = translation velocity (m/s)
    # omega = angular velocity (rad/s)

    R = MuleBot.WHEEL_RADIUS
    L = MuleBot.WHEEL_BASE_LENGTH

    v_l = ( (2.0 * v) - (omega * L) ) / (2.0 * R)
    v_r = ( (2.0 * v) + (omega * L) ) / (2.0 * R)

    return v_l, v_r

  def motorDirection(self, motorPin, direction):
    """motorDirection"""
    #  print "motorPin: ", motorPin
    #  print "direction: ",  direction
    GPIO.output(motorPin, direction)


  def motorsDirection(self, direction):
    """motorsDirection"""

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
    """dcMotorLeftTurn"""

    print ("From dcMotorLeftTurn: ", self.dcMotorPWMDurationLeft)
    tempPWMDurationLeft = int( self.dcMotorPWMDurationLeft * 70 / 100 )  # 98
    self.pwm.setPWM(self.dcMotorLeftMotor, 0, tempPWMDurationLeft)

    # Duration of the turn  
    time.sleep(duration)

    # Go straight
    self.pwm.setPWM(self.dcMotorLeftMotor, 0, self.dcMotorPWMDurationLeft)


  def dcMotorRightTurn(self, duration):
    """dcMotorRightTurn"""

    tempPWMDurationRight = int( self.dcMotorPWMDurationRight * 70 / 100 )
    self.pwm.setPWM(self.dcMotorRightMotor, 0, tempPWMDurationRight)

    # Duration of the turn  
    time.sleep(duration)

    # Go straight
    self.pwm.setPWM(self.dcMotorRightMotor, 0, self.dcMotorPWMDurationRight)

  def constrainSpeed(self, speedRPM):
      """constrainSpeed ensures 0 <= speedRPM <= max.

      @type speedRPM: float
      @param speedRPM: wheel speedRPM (rpm)

      @rtype: float
      @return: constrained wheel speed (rpm)
      """

      if speedRPM > self.motorMaxRPM:
        speedRPM = self.motorMaxRPM

      if speedRPM < 0.0:
        speedRPM = 0.0

      print ( "motorSpeed RPM adjusted: ", speedRPM )

      return speedRPM


  def motorSpeed(self, speedRPM_l, speedRPM_r):
    """motorSpeed"""

    speedRPM_l = self.constrainSpeed(speedRPM_l)
    speedRPM_r = self.constrainSpeed(speedRPM_r)

#   Left motor
    pwmDuration = 4095.0 * speedRPM_l / self.motorMaxRPM
    print("Duration float: ", pwmDuration)
    pwmDuration = int( pwmDuration )
    print("Duration int: ", pwmDuration)
    startOfPulse = 0
    self.pwm.setPWM(self.dcMotorLeftMotor, startOfPulse, pwmDuration)
    self.dcMotorPWMDurationLeft = pwmDuration

#   Right motor
    #Adjust for right motor being faster
    pwmDuration = 4095.0 * speedRPM_r / self.motorMaxRPM
    pwmDuration = pwmDuration * 9852 / 10000  # 98.519113 percent
    pwmDuration = int( pwmDuration )
    startOfPulse = 0
    self.pwm.setPWM(self.dcMotorRightMotor, startOfPulse, pwmDuration)
    self.dcMotorPWMDurationRight = pwmDuration


  def init(self):
    """init"""

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

      """run1 is used to navigate the MuleBot to
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
          print ("Current distance: ", currentDistance)

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


  def lidarNav(self, _q2, q_lidar_nav):

      """lidarNav is used to navigate the MuleBot to
      an object.

      This method is a thread.

      _q2 is used to send steering directions to the run2 thread.
      q_lidar_nav receives target range and width information."""

      # Create the RangeBot instance.
      servo_channel = 3
      range_bot = RangeBot(servo_channel)

      target_range = 0
      target_width = 0
      navigating = False

      while self._running:
          if navigating:
              name = threading.currentThread().getName()
              print("Consumer thread x:  ", name)

          if not q_lidar_nav.empty():
             command = q_lidar_nav.get()
             first_char = 0
             if command[first_char] == 'r':
               target_range = float( command[1:] )
             if command[first_char] == 'w':
               target_width = float( command[1:] )



          # Are we navigating?
          navigating = target_range > 0 and target_width > 0
          if navigating:
              print("distance: ", target_range)
              print("width: ", target_width)
              time.sleep(2)

              angle, tgt_range, hits = range_bot.execute_hunt(target_range, target_width)

              # Stop if we are too close to the target
              if tgt_range < 24:
                  v_l = 0
                  v_r = 0
                  self.set_wheel_drive_rates(v_l, v_r)

                  # setting the range to zero will stop any navigating.
                  target_range = 0

              else:
                  # Use the updated range for the next run.
                  target_range = tgt_range

                  # Turn based on the angle to target.
                  # Positive angles are left.
                  # Negative angles are right.

                  # Convert from degrees to radians.
                  angle_rad = math.radians(angle)

                  # Navigate per the angle.
                  # What is our current velocity (m/s)
                  v = self.v()
                  omega = angle_rad
                  v_l, v_r = self._uni_to_diff(v, omega)
                  self.set_wheel_drive_rates(v_l, v_r)
                  # Sleep during the turn
                  time.sleep(1)
                  # Drive straight
                  omega = 0 # zero is no turn
                  v_l, v_r = self._uni_to_diff(v, omega)
                  self.set_wheel_drive_rates(v_l, v_r)
              # end else tgt_range < minimum allowed
          # end if navigating
          time.sleep(5)


  def intFromStr( self, _string, _index ):
      """intFromStr extract an integer from a string."""

      list = re.findall( r'\d+', _string )
      return int( list[_index] )

  def run2(self, _q2, _qWallDistance, q_lidar_nav):
        """ run2 is a thread
        It is processing commands from the keyboard
        _q2 is a command queue
        _qWallDistance is the ideal distance from the wall
        q_lidar_nav is target range and width pairs"""

        while self._running:
#                name = threading.currentThread().getName()
#                print ("Consumer thread 2:  ", name)
                qCommand = _q2.get();
#                print ("Here is the command... ", qCommand)
#                print


                qSize = _q2.qsize()
                if qSize > 1:
                  print ( "***** Command Queue Size: ", qSize, " *****" )

                # Change the command to lowercase
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
                # n is for navigating using Lidar.
                elif command == 'n':
                    if len(cmd) >= 3:
                        if cmd[1] == 'r':
                            # get range to target
                            target_range = cmd[2:]
                            target_range = int(target_range)
                            print("Target range: ", target_range)
                            q_lidar_nav.put( 'r' + str(target_range) )
                        if cmd[1] == 'w':
                            # get width of target
                            target_width = cmd[2:]
                            target_width = int(target_width)
                            print("Target width: ", target_width)
                            q_lidar_nav.put( 'w' + str(target_width) )
                        
                    # end if



                elif command == 'z':
                  self.setMotorsDirection('f')

                  # Get speeds (m/m)
                  speeds = cmd[1:]
                  comma_index = speeds.find(',')

                  vmm_l = speeds[0: comma_index]
                  vmm_r = speeds[comma_index + 1:]

                  print("vmm_l: ", vmm_l)
                  print("vmm_r: ", vmm_r)

                  # Convert from meters per minute to meters per second
                  v_l = float(vmm_l) / 60.0
                  v_r = float(vmm_r) / 60.0

                  print("v_l: ", v_l)
                  print("v_r: ", v_r)


                  self.set_wheel_drive_rates(v_l, v_r)

                elif command == 'f' or command == 'r':
                  direction = command
                  print (direction)
                  self.setMotorsDirection(direction)

                  index = 0
                  speed = float(cmd[1:])
                  print("Speed: ", speed)

                  self.motorSpeed(speed, speed)
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


                

  def laserNav( self, _qCommands ):

      """ Name:  laserNav
          Date:  January 2018

          Arguments:  self

          Purpose:  laserNav 

      """

      lastCommandChangeTime = None
      lastCommand = None

      while self._running:

          if not (lastCommandChangeTime == None):
              if not (lastCommand == None):
                  # There is a time and command.
              
                  # Check if at least 30 seconds have passed since 
                  # last state change.
                  TIME_TO_WAIT = 30   # Seconds
                  currentTime = time.time() # Seconds
                  sufficientWaitTime = ( (currentTime - lastCommandChangeTime) > TIME_TO_WAIT )
                  if sufficientWaitTime:
                      _qCommands.put(lastCommand)
                      lastCommandChangeTime = currentTime



          files = os.listdir("/home/pi/pythondev/MuleBot2/")
          
          for file in files:
              # Looking for files ending in ".loc"
              if file.endswith(".loc"):
                  print ( file )
                  command = "rm " + file
                  os.system( command )

                  # Determine which of the six states that the
                  # Laser Detector is in and steer accordingly.
                  if file == "LO_FL.loc":
                      _qCommands.put("S6")
                      lastCommand = "S6"
                  elif file == "LO_L.loc":
                      _qCommands.put("S3")
                      lastCommand = "S3"
                  elif file == "LO_C.loc":
                      _qCommands.put("S1")
                      lastCommand = "S1"
                  elif file == "RO_C.loc":
                      _qCommands.put("P1")
                      lastCommand = "P1"
                  elif file == "RO_R.loc":
                      _qCommands.put("P3")
                      lastCommand = "P3"
                  elif file == "RO_FR.loc":
                      _qCommands.put("P6")
                      lastCommand = "P6"
                  else:
                      # This should never happen.
                      print( file, " is an invalid state name" )

                  # Ignoring the check for an invalid state, their
                  # there should have been a command issued.
                  lastCommandChangeTime = time.time()

          time.sleep(0.5)



  def setMotorsDirection(self, _direction):
    """setMotorsDirection sets both motors to the same direction. """

    if _direction == 'f' or _direction == 'F':
      self.motorDirection(self.motor1DirectionPin, self.motorForward)
      self.motorDirection(self.motor2DirectionPin, self.motorForward)
    elif _direction == 'r' or _direction == 'R':
      self.motorDirection(self.motor1DirectionPin, self.motorReverse)
      self.motorDirection(self.motor2DirectionPin, self.motorReverse)
    else:
      print ("ERROR: setMotorsDirection bad parameter: " + direction)

  def shutdown(self):
    """shutdown """
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
