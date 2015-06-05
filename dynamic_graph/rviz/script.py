from dynamic_graph.sot.application.velocity.precomputed_tasks import initialize #deprecated
solver=initialize(robot) #deprecated

from dynamic_graph.sot.application.velocity.precomputed_tasks import Application
appli =Application(robot)
robot.initializeTracer()
#launch service start_dynamic_graph

#walk few steps
from dynamic_graph.sot.pattern_generator.walking import CreateEverythingForPG, walkFewSteps, walkFewStepsCircular
CreateEverythingForPG(robot,solver)
walkFewSteps(robot)

#-----------creation of a task---------------
from dynamic_graph.sot.core.meta_tasks import generic6dReference, Task, GainAdaptive
from dynamic_graph.sot.core.matrix_util import matrixToTuple
from dynamic_graph import plug
from numpy import pi


#show tasks in solver controling the robot
print solver #deprecated
print appli.solver

#show library of precomputed tasks
robot.tasks 

#
appli.gains['right-wrist'].setByPoint(4,0.2,0.01,0.8)

trunktask = Task ("trunk-task")
trunktask.add (appli.features['chest'].name)
trunktask.add (appli.features['waist'].name)
trunktask.add (appli.features['gaze'].name)


trunkgain = GainAdaptive('trunkgaingain')
trunkgain.setConstant(1)
plug(trunkgain.gain, trunktask.controlGain)
plug(trunktask.error, trunkgain.error) 

appli.features['chest'].frame('desired')
appli.features['waist'].frame('desired')
appli.features['gaze'].frame('desired')


appli.features['chest'].selec.value = '010000'
appli.features['waist'].selec.value = '010000'
appli.features['gaze'].selec.value = '111000'

appli.solver.push(trunktask)
appli.solver.push(appli.tasks["right-wrist"])
appli.solver.push(appli.tasks["left-wrist"])

#tasks definition
appli.features['right-wrist'].reference.value = matrixToTuple(generic6dReference((0.10,-0.25,0.85,0,-pi/2,0)))
#appli.features['right-wrist'].reference.value = matrixToTuple(generic6dReference((0.35,-0.25,0.85,0,-pi/2,0)))
appli.features['left-wrist'].reference.value = matrixToTuple(generic6dReference((0.10,0.25,0.85,0,-pi/2,0)))
#appli.features['left-wrist'].reference.value = matrixToTuple(generic6dReference((0.35,0.25,0.85,0,-pi/2,0)))
appli.features['left-wrist'].reference.value = matrixToTuple(generic6dReference((0.10,0.25,0.85,pi/2,0,-pi/2)))

appli.features['left-ankle'].reference.value = matrixToTuple(generic6dReference((0.015,0.25,0.2,0,0,0)))
appli.features['right-ankle'].reference.value = matrixToTuple(generic6dReference((0.015,-0.25,0.2,0,0,0)))



#retirer tache du solver
appli.solver.sot.remove('trunk-task')


