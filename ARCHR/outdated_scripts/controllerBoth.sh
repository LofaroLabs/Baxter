#!/bin/sh
echo "======This should start the left arm controller======"
cd /home/archr/projects/archr_Code/Simulation/Baxter_ARCHR
rosrun baxter_tools enable_robot.py -e
rostopic pub -1 /robot/sonar/head_sonar/set_sonars_enabled std_msgs/UInt16 0
python controllerBoth.py 

#add if Ctrl+C pressed, then rosrun baxter_tools enable_robot.py -d