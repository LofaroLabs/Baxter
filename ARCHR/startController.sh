#!/bin/sh
# Project ARCHR: Mannan Javid (mannanj90@gmail.com) 
# 		  		 Patrick Early
#          		 Eric Eide
#         	     Martyna Bula
echo "======Enabling robot and telling him to shush.======"
rosrun baxter_tools enable_robot.py -e
rostopic pub -1 /robot/sonar/head_sonar/set_sonars_enabled std_msgs/UInt16 0
rosrun baxter_examples xdisplay_image.py --file=`rospack find baxter_examples`/home/archr/projects/Baxter/ARCHR/archr_team.jpg
echo "======Starting terminal for the hubo-ach, network, & dynamixels. Please check everything started.======"
cd /home/archr/projects/Baxter/ARCHR/scripts && gnome-terminal --tab --command "sudo ufw disable" --tab -e "sudo avahi-autoipd eth0" --tab -e "hubo-ach start" --tab -e "sudo python sendACHData.py"
sleep 5 #this could be changed so that the below only runs if the dynamixels have been scanned
echo "======Next opening terminal with the environment for baxter loaded.======"
echo "======Please run bash serverArms.sh, controllerL.sh and bash controllerR.sh here.======"
echo "======For the gripper run bash gripperL.sh or bash gripperR.sh here.======"
cd /home/archr/ros_ws && gnome-terminal --tab --command "bash baxter.sh" --tab -e "bash baxter.sh"  --tab -e "bash baxter.sh"  --tab -e "bash baxter.sh" 
