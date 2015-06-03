#!/usr/bin/env python
"""
Launch the HRP2controller, the jython script that initialize OpenRTM, and prepare a shell that parse python command into ros which interact with the sot.
See http://exyr.org/2011/gnome-terminal-tabs/
"""
from time import sleep
import subprocess

terminal = ['gnome-terminal']

# establish the dynamic graph and the its connection to opehrp3.1

# Start roscore in a terminal
terminal.extend(['--tab-with-profile=HoldOnExit', '-e','''
bash -c '
echo "launch roscore"
roscore
'
''' % locals(), '-t', '''roscore'''])

# Start Controller
terminal.extend(['--tab-with-profile=HoldOnExit', '-e','''
bash -c '
echo "Launching Controller"
/opt/grx/HRP2LAAS/bin/HRPController.sh
'
''' % locals(), '-t', '''HRP2 Controller'''])

# Start sot.py terminal
terminal.extend(['--tab-with-profile=HoldOnExit', '-e','''
bash -c '
echo "Initialize the connection between the sot and the OpenRTM"
sleep 5
/opt/grx/HRP2LAAS/script/sot_ben.py

'
''' % locals(), '-t', '''sot.py'''])
#/opt/grx/HRP2LAAS/script/sot_ben.py
#/opt/grx/HRP2LAAS/script/sot.py

# Start dynamic_graph_bridge run_command terminal
terminal.extend(['--tab-with-profile=HoldOnExit', '-e','''
bash -c '
echo "run command :"
rosrun dynamic_graph_bridge run_command
'
''' % locals(), '-t', '''Run Command'''])

# Set the size of the terminal
terminal.extend(['''--geometry=195x50+0+0'''])

subprocess.call(terminal)
