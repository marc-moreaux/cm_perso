#!/bin/bash

# launch roscore
sourceindigo
roscore & 
sleep 2

# launch R200
source ~/catkin_ws_realsense/devel/setup.bash
roslaunch realsense realsense_r200_launch.launch

# launch rviz
sourceork
rosrun rviz rviz &
sleep 2

