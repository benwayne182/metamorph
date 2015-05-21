from dynamic_graph.sot.application.velocity.precomputed_tasks import initialize
solver=initialize(robot)
robot.initializeTracer()
#launch service start_dynamic_graph

from dynamic_graph.sot.pattern_generator.walking import CreateEverythingForPG, walkFewSteps, walkFewStepsCircular
CreateEverythingForPG(robot,solver)
walkFewSteps(robot)
