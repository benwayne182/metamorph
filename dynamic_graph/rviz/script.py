from dynamic_graph.sot.application.velocity.precomputed_tasks import initialize
solver=initialize(robot)
robot.initializeTracer()
#launch service start_dynamic_graph

#walk few steps
from dynamic_graph.sot.pattern_generator.walking import CreateEverythingForPG, walkFewSteps, walkFewStepsCircular
CreateEverythingForPG(robot,solver)
walkFewSteps(robot)

#creation of a task
from dynamic_graph.sot.core.math_small_entities import Derivator_of_Matrix, Inverse_of_matrixHomo, Multiply_of_matrixHomo, Stack_of_vector, PoseRollPitchYawToMatrixHomo, MatrixHomoToPoseRollPitchYaw, Multiply_matrixHomo_vector
from dynamic_graph import plug
print solver #show tasks in solver controling the robot
robot.tasks #show library of precomputed tasks
poserpy=PoseRollPitchYawToMatrixHomo('poserpy') #convert 6d vectors (x,y,z,roll,pitch,yaw) to homogeneous matrix
poserpy.sin.value = (0.08,0.4,0.0,0,0,0)
plug(poserpy.sout, robot.features['left-wrist'].reference)
solver.push(robot.tasks['left-wrist'])
