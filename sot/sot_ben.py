#!/opt/grx/bin/hrpsyspy
import sys
import socket
import traceback
import math
import time
import java.lang.System
import os
import rtm
import waitInput
import bodyinfo
import sotinfo
import OpenHRP
from OpenHRP.RobotHardwareServicePackage import SwitchStatus

st = None
if "ON" == "ON":
    useStabilizerComp = True
else:
    useStabilizerComp = False

def init(robotHost=None):
    if robotHost != None:
      print 'robot host = '+robotHost
      java.lang.System.setProperty('NS_OPT',
          '-ORBInitRef NameService=corbaloc:iiop:'+robotHost+':2809/NameService')
      rtm.initCORBA()

    print "creating components"
    rtcList = createComps(robotHost)

    print "connecting components"
    connectComps()

    print "activating components"
    activateComps(rtcList)

    print "initialize bodyinfo"
    bodyinfo.init(rtm.rootnc)

    print "initialized successfully"

def activateComps(rtcList):
    rtm.serializeComponents(rtcList)
    for r in rtcList:
        r.start()

def initRTC(module, name):
    ms.load(module)
    return ms.create(module, name)

def goActual():
    sh_svc.goActual()

def setJointAngle(jname, angle, tm, wait=True):
    seq_svc.setJointAngle(jname, angle*pi/180.0, tm)
    if wait:
        seq_svc.waitInterpolation()

def setJointAnglesDeg(pose, tm, wait=True):
    seq_svc.setJointAngles(bodyinfo.makeCommandPose(pose), tm)
    if wait:
        seq_svc.waitInterpolation()

def goInitial(tm=bodyinfo.timeToInitialPose):
    if isServoOn(): 
      putRobotUp()
      waitInputConfirm( \
        '!! Robot Motion Warning !!\n\n' +\
        'Push [OK] to move to the Initial Pose')
    setJointAnglesDeg(bodyinfo.initialPose, tm)

def loadPattern(basename, tm=3.0):
    seq_svc.loadPattern(basename, tm)

def goHalfSitting(tm=bodyinfo.timeToHalfsitPose, wait=True):
    if isServoOn():
      putRobotUp()
      waitInputConfirm( \
        '!! Robot Motion Warning !!\n\n' +\
        'Push [OK] to move to the Half-Sit Pose')
    setJointAnglesDeg(bodyinfo.halfsitPose, tm, False)
    waistpos = [0,0,bodyinfo.halfsitWaistHeight]
    if not seq_svc.setBasePos(waistpos, tm):
        print "setBasePos() failed"
    zmp = [0,0,-bodyinfo.halfsitWaistHeight]
    if not seq_svc.setZmp(zmp, tm):
        print "setZmp() failed"
    if wait==True:
        seq_svc.waitInterpolation()

def stOn():
    st.setProperty("isEnabled", "1")

def stOff():
    st.setProperty("isEnabled", "0")

def sotOn():
    sot.setProperty("is_enabled", "1")

def sotOff():
    sot.setProperty("is_enabled", "0")

def walk05():
    kpg_svc.setTargetPos(0.449, 0.0, 0.0)

def startStep():
    kpg_svc.startStepping()

def stopStep():
    kpg_svc.stopStepping()

def createComps(hostname=socket.gethostname()):
    global ms, adm_svc, rh, rh_svc, seq, seq_svc, sh, sh_svc, servo, kpg, kpg_svc, st, kf, log, simulation_mode, sot
    ms = rtm.findRTCmanager(hostname)
    rh = rtm.findRTC("RobotHardware0")
    if rh != None:
        simulation_mode = 0
        rh_svc = OpenHRP.RobotHardwareServiceHelper.narrow(rh.service("service0"))
        servo = rh
        adm = rtm.findRTC("SystemAdmin0")
        if adm != None:
          adm.start()
          adm_svc = OpenHRP.SystemAdminServiceHelper.narrow(adm.service("service0"))
    else:
        simulation_mode = 1
        rh = rtm.findRTC(bodyinfo.modelName+"Controller(Robot)0")
        servo = rtm.findRTC("PDservo0")
    seq = initRTC("SequencePlayer", "seq")
    seq_svc = OpenHRP.SequencePlayerServiceHelper.narrow(seq.service("service0"))
    sh  = initRTC("StateHolder", "StateHolder0")
    sh_svc = OpenHRP.StateHolderServiceHelper.narrow(sh.service("service0"))

    if useStabilizerComp:
        kf  = initRTC("KalmanFilter", "kf")
    kpg = initRTC("WalkGenerator", "kpg")
    kpg_svc = OpenHRP.WalkGeneratorServiceHelper.narrow(kpg.service("service0"))
    if useStabilizerComp:
        st  = initRTC("Stabilizer", "st")
        st.setConfiguration(bodyinfo.hstConfig)

    log = initRTC("DataLogger", "log")
    
    print "Creating SoT"
    sot = initRTC("RtcStackOfTasks","sot")
    print "Set configuration of SoT"
    sot.setConfiguration(sotinfo.sotConfig)
    if useStabilizerComp:
        return [rh, seq, kf, kpg, sh, st, log, sot]
    else:
        return [rh, seq, kpg, sh, log, sot]
    

def connectComps():
    if useStabilizerComp:
        rtm.connectPorts(rh.port("q"), [sh.port("currentQIn"),
                                        st.port("q")])
    else:
        rtm.connectPorts(rh.port("q"), sh.port("currentQIn"))
    if servo != None:
        if useStabilizerComp:
            rtm.connectPorts(rh.port("rfsensor"), st.port("forceR"))
            rtm.connectPorts(rh.port("lfsensor"), st.port("forceL"))
            rtm.connectPorts(rh.port("gyrometer"), [st.port("rate"),
                                                    kf.port("rate")])
            rtm.connectPorts(rh.port("gsensor"), [kf.port("acc"),
                                                  st.port("acc")])
        rtm.connectPorts(rh.port("rfsensor"), sot.port ("forcesRF"))
        rtm.connectPorts(rh.port("lfsensor"), sot.port ("forcesLF"))
        rtm.connectPorts(rh.port("rhsensor"), sot.port ("forcesRH"))
        rtm.connectPorts(rh.port("lhsensor"), sot.port ("forcesLH"))
    #
    rtm.connectPorts(seq.port("qRef"),    sh.port("qIn"))
    rtm.connectPorts(seq.port("basePos"), sh.port("basePosIn"))
    rtm.connectPorts(seq.port("baseRpy"), sh.port("baseRpyIn"))
    if useStabilizerComp:
        rtm.connectPorts(seq.port("accRef"),  kf.port("accRef"))
        rtm.connectPorts(seq.port("zmpRef"),  st.port("zmpRef"))
        rtm.connectPorts(sot.port("accRef"),  kf.port("accRef"))
        rtm.connectPorts(sot.port("zmpRef"),  st.port("zmpRef"))
        rtm.connectPorts(sh.port("qOut"), st.port("qRefIn"))
        rtm.connectPorts(sh.port("baseRpyOut"), st.port("rpyRef"))

    rtm.connectPorts(sot.port("qRef"),    sh.port("qIn"))
    rtm.connectPorts(sot.port("pRef"),    sh.port("basePosIn"))
    rtm.connectPorts(sot.port("rpyRef"),  sh.port("baseRpyIn"))
    #
    rtm.connectPorts(sh.port("qOut"), [seq.port("qInit"),
                                       sot.port("qInit")])
    rtm.connectPorts(sh.port("basePosOut"), [seq.port("basePosInit"),
                                         sot.port("pInit")])
    rtm.connectPorts(sh.port("baseRpyOut"), [seq.port("baseRpyInit"),
                                             sot.port("rpyInit")])
    #
    if servo: # simulation_mode with dynamics or real robot mode
        if useStabilizerComp:
            rtm.connectPorts(st.port("qRefOut"), servo.port("qRef"))
        else:
            rtm.connectPorts(sh.port("qOut"), servo.port("qRef"))
    else:     # simulation mode without dynamics
        rtm.connectPorts(sh.port("qOut"), rh.port("qIn"))
    #

def setupLogger():
    global log_svc
    log_svc = OpenHRP.DataLoggerServiceHelper.narrow(log.service("service0"))
    log_svc.add("TimedDoubleSeq", "q")
    log_svc.add("TimedDoubleSeq", "qRefst")
    log_svc.add("TimedDoubleSeq", "qOutsh")
    log_svc.add("TimedDoubleSeq", "qRefsot")
    log_svc.add("TimedDoubleSeq", "zmpRefSeq")
    log_svc.add("TimedDoubleSeq", "zmpRefKpg")
    log_svc.add("TimedDoubleSeq", "basePos")
    log_svc.add("TimedDoubleSeq", "rpy")
    log_svc.add("TimedDoubleSeq","forceL")
    log_svc.add("TimedDoubleSeq","forceR")

    rtm.connectPorts(rh.port("q"), log.port("q"))
    rtm.connectPorts(rh.port("rfsensor"), log.port("forceR"))
    rtm.connectPorts(rh.port("lfsensor"), log.port("forceL"))    
    rtm.connectPorts(sh.port("qOut"), log.port("qOutsh"))
    rtm.connectPorts(sot.port("qRef"), log.port("qRefsot"))
    if useStabilizerComp:
        rtm.connectPorts(st.port("qRefOut"), log.port("qRefst"))
        rtm.connectPorts(kf.port("rpy"), log.port("rpy"))
    rtm.connectPorts(seq.port("zmpRef"), log.port("zmpRefSeq"))
    rtm.connectPorts(sot.port("zmpRef"), log.port("zmpRefKpg"))
    rtm.connectPorts(sh.port("basePosOut"), log.port("basePos"))

def saveLog(fname='sot'):
    if log_svc == None:
      waitInputConfirm("Setup DataLogger RTC first.")
      return
    log_svc.save(fname)
    print 'saved'

##
## for real robot
##
import thread
def getActualState():
  stateH = OpenHRP.RobotHardwareServicePackage.RobotStateHolder()
  rh_svc.getStatus(stateH)
  return stateH.value

def isServoOn(jname = "any"):
  if simulation_mode:
    return True
  ss = getActualState().servoState
  if jname == 'any':
    for s in ss:
      if (s&2) > 0:
        return True
    return False

  if jname == 'all':
    for s in ss:
      if (s&2) == 0:
        return False
    return True

  return False

def isCalibDone():
  if simulation_mode:
    return True
  ss = getActualState().servoState
  for s in ss:
    if (s&1) == 0:
      return False
  return True

def countDownLoop(t):
  while (t >= 0):
      print t
      t = t - 1
      time.sleep(0.98)

def countDown(t):
  thread.start_new_thread(countDownLoop, (t, ) )

def putRobotDown(msg=""):
  if simulation_mode:
    print 'omit putRobotDown'
    return
  f = getActualState().force
  while f[0][2] < 50.0 and f[1][2] < 50.0:
    waitInputConfirm(msg + "Put the robot down.")
    f = getActualState().force

def putRobotUp(msg=""):
  if simulation_mode:
    return True
  f = getActualState().force
  while 30.0 < f[0][2] or 30.0 < f[1][2]:
    waitInputConfirm(msg + "Make sure the Robot in the Air.")
    f = getActualState().force

def servoOn(jname = 'all', destroy = 1):
    if not isCalibDone():
      waitInputConfirm('!! Do CheckEncoders First !!\n\n')
      return -1
 
    if isServoOn():
      return 1
    if jname == '':
        jname = 'all'
    putRobotUp()
    rh_svc.power('all', SwitchStatus.SWITCH_ON)

    try:
      waitInputConfirm(\
          '!! Robot Motion Warning (SERVO ON) !!\n\n' +\
          'Confirm turn RELAY ON.\n' +\
          'Push [OK] to servo ON ('+jname+').')
    except:
      rh_svc.power('all', SwitchStatus.SWITCH_OFF)
      raise
    #if destroy:
    #  self.destroyRTCs(0, [self.Robot])
    #  self.initRTSystem()
    try: 
      stOff()
      goActual()
      time.sleep(0.1)
      rh_svc.servo(jname, SwitchStatus.SWITCH_ON)
      time.sleep(5)
      if not isServoOn(jname):
        print 'servo on failed.'
        raise
    except:
      print "exception occured"

    return 1

def servoOff(jname = 'all'):
    if simulation_mode:
      print "omit servo off"
      return
    if not isServoOn():
      if jname == 'all':
        rh_svc.power('all', SwitchStatus.SWITCH_OFF)   
      return 1
    if jname == '':
      jname = 'all'

    putRobotUp()

    waitInputConfirm(\
      '!! Robot Motion Warning (Servo OFF)!!\n\n' + 
      'Push [OK] to servo OFF ('+jname+').')#:

    try:
      rh_svc.servo('all', SwitchStatus.SWITCH_OFF)   
      if jname == 'all':
        rh_svc.power('all', SwitchStatus.SWITCH_OFF)   
      return 1
    except:
      print 'servo off : communication error'
      return -1

def reboot():
    waitInputConfirm("Reboot the robot host ?")
    adm_svc.reboot("")

def shutdown():
    waitInputConfirm("Shutdown the robot host ?")
    adm_svc.shutdown("")

def overwriteEncoders(jname='all', option='-overwrite'):
    checkEncoders(jname, option)

def checkEncoders(jname='all', option=''):
    if isServoOn():
      waitInput('Servo Off first.')
      return

    #self.destroyRTCs(0, [self.Robot])
    #self.systemInit()

    rh_svc.power('all', SwitchStatus.SWITCH_ON)
    msg = '!! Robot Motion Warning !!\n' +\
          'Turn Relay ON.\n' +\
          'Then Push [OK] to '
    if option == '-overwrite':
      msg = msg + 'calibrate(OVERWRITE MODE) '
    else:
      msg = msg + 'check '

    if jname == 'all':
      msg = msg + 'the Encoders of all.'
    else:
      msg = msg + 'the Encoder of the Joint "'+jname+'".'

    try:
      waitInputConfirm(msg)
    except:
      rh_svc.power('all', SwitchStatus.SWITCH_OFF)
      return 0
    print 'calib-joint ' + jname + ' ' + option
    rh_svc.initializeJointAngle(jname, option)
    print 'done'
    rh_svc.power('all', SwitchStatus.SWITCH_OFF)

def calibSensors():
    servoOn() # destroy user plugins
    goInitial()
    try:
      waitInputConfirm( \
        'Make sure the robot in the Air\n\n' +\
        'Then push [OK] to calibrate FORCE SENSORs.')
      rh_svc.removeForceSensorOffset()
       
      putRobotDown()
      if waitInputSelect('Push [Yes] to calibrate ATTITUDE SENSORs.'):
        countDown(10)
        rh_svc.calibrateInertiaSensor()
    except:
      exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
      traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback,limit=2, file=sys.stdout)
    servoOff()

def startSot():
    servoOn()
    goHalfSitting()
    if useStabilizerComp:
        stOn()
    sotOn()
    putRobotDown()
    time.sleep(8) # TODO use sleep funtion which can count simulation time
    saveLog("/tmp/%s_sot_%s"%(bodyinfo.modelName.lower(), time.strftime('%Y%m%d%H%M')))

def execTestPattern():
    servoOn()
    goHalfSitting()
    if useStabilizerComp:
        stOn()
    putRobotDown()
    try:
      waitInputConfirm(
        '!! Robot Motion Warning !! \n'+\
        'Check ST then, Push [OK] to start stepping(about 8 sec).')
    except: 
      stOff()
      servoOff()
      return 0

    startStep()
    time.sleep(8) # TODO use sleep funtion which can count simulation time
    stopStep()

    stOff()
    saveLog("/tmp/%s_steptest_%s"%(bodyinfo.modelName.lower(), time.strftime('%Y%m%d%H%M')))
    servoOff()

def execTestPattern2():
    servoOn()
    goHalfSitting()
    if useStabilizerComp:
        stOn()
    putRobotDown()
    try:
      waitInputConfirm(
        '!! Robot Motion Warning !! \n'+\
        'Check ST then, Push [OK] to start walking(1.0m).')
    except: 
      stOff()
      servoOff()
      return 0

    kpg_svc.setTargetPos(1.0, 0.0, 0.0)

    stOff()
    saveLog("/tmp/%s_walktest_%s"%(bodyinfo.modelName.lower(), time.strftime('%Y%m%d%H%M')))
    servoOff()

def userTest():
    goHalfSitting()
    if useStabilizerComp:
        stOn()
    putRobotDown()

    try:
      waitInputConfirm(
        '!! Robot Motion Warning !! \n'+\
        'Check ST then, Push [OK] to start sot.')
    except: 
      stOff()
      servoOff()
      return 0

    print "sot On"
    sotOn()

    while True:
      try:
        waitInputConfirm(
          '!! Robot Motion Warning !! \n'+\
          'Push [OK] to stop sot.')
        print "Dynamic graph stopped"
        stOff()
        servoOff()
        return 0
      except: 
        sleep(2)

if __name__ == '__main__' or __name__ == 'main':
    if len(sys.argv) > 1:
        robotHost = sys.argv[1]
    else:
        robotHost = None
    init(robotHost)
    setupLogger()
    userTest()
