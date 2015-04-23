roscore
/opt/grx3.0/HRP2LAAS/bin/GrxUI.sh
roslaunch hrp2_bringup openhrp_bridge.launch robot:=hrp2_14 mode:=dg_with_stabilizer simulation:=true
rosrun dynamic_graph_bridge run_command

%lancer commandes de script.py

rosservice call /start_dynamic_graph
