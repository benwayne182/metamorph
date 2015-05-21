import numpy as np
from pinocchio.utils import *
import pinocchio as se3
from pinocchio.romeo_wrapper import RomeoWrapper
robot = RomeoWrapper('/home/bsinivas/devel/pinocchio/pinocchio/models/romeo.urdf')

#for name,function in robot.model.__class__.__dict__.items():
#  print " **** ", name, ": ", function.__doc__
#def index(self,name):
#   return [ idx for idx,name in enumerate(robot.model.names) if name=="RWristPitch" ][0]
# Get the placement of joint number idx
#placement = robot.data.oMi[0]

#q=zero(robot.nq)
#v=rand(robot.nv)
#robot.com(q)            # Compute the robot center of mass.
#robot.position(q,23)    # Compute the placement of joint 23

#lancer gepetto-viewer-server
#--------------creating and displaying the robot---------------
from gepetto.corbaserver import Client
client = Client ()
wid = client.gui.createWindow ("w")# open a new window
client.gui.createSceneWithFloor("world")
client.gui.addSceneToWindow("world",wid)
client.gui.addURDF("world/romeo","/home/bsinivas/devel/pinocchio/pinocchio/models/romeo.urdf","/home/bsinivas/devel/pinocchio/pinocchio/models/")
client.gui.getNodeList()
#-----------give a specific position to a joint-----------------
#q1 = [1,1,1,1,0,0,0]
#client.gui.applyConfiguration('world/romeo/HeadRollLink',q1)
#client.gui.applyConfiguration('world/romeo/LElbowYawLink',q1)
#client.gui.applyConfiguration('world/romeo/LHipPitchLink',q1)
#client.gui.applyConfiguration('world/romeo/LKneePitchLink',q1)
#client.gui.applyConfiguration('world/romeo/LShoulderYawLink',q1)
#client.gui.applyConfiguration('world/romeo/LWristRollLink',q1)
#client.gui.applyConfiguration('world/romeo/LWristYawLink',q1)
#client.gui.applyConfiguration('world/romeo/NeckPitchLink',q1)
#client.gui.applyConfiguration('world/romeo/RElbowYawLink',q1)
#client.gui.applyConfiguration('world/romeo/RHipPitchLink',q1)
#client.gui.applyConfiguration('world/romeo/RKneePitchLink',q1)
#client.gui.applyConfiguration('world/romeo/RShoulderYawLink',q1)
#client.gui.applyConfiguration('world/romeo/RWristRollLink',q1)
#client.gui.applyConfiguration('world/romeo/RWristYawLink',q1)
#client.gui.applyConfiguration('world/romeo/body',q1)
#client.gui.applyConfiguration('world/romeo/l_ankle',q1)
#client.gui.applyConfiguration('world/romeo/l_wrist',q1)
#client.gui.applyConfiguration('world/romeo/r_ankle',q1)
#client.gui.applyConfiguration('world/romeo/r_wrist',q1)
#client.gui.applyConfiguration('world/romeo/torso',q1)
#client.gui.refresh() # Refresh the window.

#head_joint_id=robot.index('HeadRoll')
#M=robot.position(robot.q0,head_joint_id)

robot.initDisplay("world/romeo") #init the displaying of the robot
robot.display(robot.q0) # display the robot at the initial position
q=robot.q0
v = rand(robot.nv)
