#!/bin/bash

print_help(){
  echo ""
  echo " --my_roscore ip [ip2 ..]"
}



if [ -z "$1" ]
then
  print_help
  exit
fi


# IP of the computer
ROSCORE_IP=10.0.160.147


cd /home/mmoreaux/rosbag
source /home/mmoreaux/.bashrc
source /home/mmoreaux/.bashindigo
source /home/mmoreaux/catkin_ws_ork/devel/setup.bash



for M_PORT in {12345..12347}
do 

  Set_NAO_IP_from_port $M_PORT
  export ROS_MASTER_URI=http://10.0.160.147:$M_PORT/
  export ROS_NAMESPACE=$M_PORT


  echo ""
  echo "################################"
  echo "    launching roscore at :   "
  echo "  $ROS_MASTER_URI       "
  echo "################################"

  roscore -p $M_PORT &
  sleep 5  

  echo ""
  echo "--launch rosbridge on robot"
  echo " -> $NAO_IP"
  echo " -> $ROS_MASTER_URI"
  if [ "$WITH_RVIZ" = "1" ]
  then
    rosrun rviz rviz &
  fi
  source ~/work/catkin_ws_naoqi_driver/devel/setup.bash
  roslaunch naoqi_driver naoqi_driver.launch >/dev/null &


  ssh -f nao@$NAO_IP "qicli call ALMotion.setAngles HeadYaw 0 0.5"
  sleep 1
  ssh -f nao@$NAO_IP "qicli call ALMotion.setAngles HeadPitch .4 0.5"


done





# echo ""
# echo "--Waiting 30sec for all to be ready   "
# sleep 30

# for WHATEVER in {1..12}
# do
#   echo ""
#   echo "################################"
#   echo "    Recording rosbags   "
#   echo "################################"
#   for M_PORT in {12345..12347}
#   do
#     if test $WHATEVER -gt 1
#     then 
#       echo ""
#       echo " --- moving $M_PORT rosbags"
#       for BAG in $M_PORT*
#       do
#         sleep 5 &&
#         scp $BAG 10.0.161.123:/media/raid/mmoreaux_raid &&
#         rm $BAG &
#       done
#     fi

#     export ROS_MASTER_URI=http://10.0.160.147:$M_PORT/
#     rosbag record --duration=150 -o $M_PORT \
#     /$M_PORT/audio \
#     /$M_PORT/camera/depth/camera_info \
#     /$M_PORT/camera/depth/image_raw \
#     /$M_PORT/camera/front/camera_info \
#     /$M_PORT/camera/front/image_raw \
#     /$M_PORT/face_detected \
#     /$M_PORT/pose \
#     /diagnostics_agg \
#     /joint_states \
#     /tf &
#     # /$M_PORT/camera/bottom/camera_info \
#     # /$M_PORT/camera/bottom/image_raw \



#   done

#   sleep 150 # record 2'30
# done


# sleep 10
# pkill roscore
# pkill naoqi_driver
# pkill rviz
# pkill rosbag
# pgrep -f nodelet | xargs kill
# pgrep -f object_recognition_core | xargs kill

