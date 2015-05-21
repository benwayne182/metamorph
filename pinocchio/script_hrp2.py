import numpy as np
from pinocchio.utils import *
import pinocchio as se3
from dynamic_graph.sot.hrp2.hrp2 import Hrp2
#robot = Hrp2('/home/bsinivas/devel/ros_unstable/stacks/hrp2/hrp2_14_description/build/urdf/hrp2_14.urdf')
robot = Hrp2("hrp2_14",/home/bsinivas/devel/ros_unstable/install/share/hrp2-14,/home/bsinivas/devel/ros_unstable/install/share/hrp2-14,device=RobotSimu('hrp2_14'),dynamicType=,tracer = None)
#lancer gepetto-viewer-server
#--------------creating and displaying the robot---------------
from gepetto.corbaserver import Client
client = Client ()
wid = client.gui.createWindow ("w")# open a new window
client.gui.createSceneWithFloor("world")
client.gui.addSceneToWindow("world",wid)
client.gui.addURDF("world/hrp2_14","/home/bsinivas/devel/ros_unstable/stacks/hrp2/hrp2_14_description/build/urdf/hrp2_14.urdf","/home/bsinivas/devel/ros_unstable/stacks/hrp2/")
client.gui.getNodeList()
#-----------give a specific position to a joint-----------------
#q1 = [1,1,1,1,0,0,0]
#client.gui.applyConfiguration('world/romeo/HeadRollLink',q1)

#client.gui.refresh() # Refresh the window.

#head_joint_id=robot.index('HeadRoll')
#M=robot.position(robot.q0,head_joint_id)

robot.initDisplay("world/hrp2_14") #init the displaying of the robot
robot.display(robot.q0) # display the robot at the initial position
q=robot.q0
v = rand(robot.nv)
