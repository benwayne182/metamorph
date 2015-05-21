from dynamic_graph.sot.hrp2_14.robot import *
from dynamic_graph.sot.core.robot_simu import RobotSimu
robot=Robot('HRP2LAAS', device=RobotSimu('HRP2LAAS'))
from dynamic_graph.sot.application.velocity.precomputed_tasks import initialize
solver=initialize(robot)
robot.initializeTracer()

from dynamic_graph.sot.pattern_generator.walking import CreateEverythingForPG, walkFewSteps, walkFewStepsCircular
CreateEverythingForPG(robot,solver)
walkFewSteps(robot)
