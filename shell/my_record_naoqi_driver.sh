#!/bin/bash


WITH_RVIZ="0"

if [ -z "$1" ] # if no arg
then
  WITH_RVIZ="$1"
fi


# IP of the computer
ROSCORE_IP=10.0.160.147



cd /home/mmoreaux/rosbag
source /home/mmoreaux/.bashrc
source /home/mmoreaux/.bashindigo
source /home/mmoreaux/catkin_ws_ork/devel/setup.bash




for WHATEVER in {1..12}
do
  echo ""
  echo "################################"
  echo "    Recording rosbags   "
  echo "################################"
  for M_PORT in {12345..12347}
  do

    export ROS_MASTER_URI=http://$ROSCORE_IP:$M_PORT/
    rosbag record --duration=150 -o $M_PORT \
    /$M_PORT/audio \
    /$M_PORT/camera/depth/camera_info \
    /$M_PORT/camera/depth/image_raw \
    /$M_PORT/camera/front/camera_info \
    /$M_PORT/camera/front/image_raw \
    /$M_PORT/camera/ir/camera_info \
    /$M_PORT/camera/ir/image_raw \
    /$M_PORT/face_detected \
    /$M_PORT/pose \
    /diagnostics_agg \
    /joint_states \
    /tf &
    # /$M_PORT/camera/bottom/camera_info \
    # /$M_PORT/camera/bottom/image_raw \



  done
  sleep 150 # record 2'30

  echo ""
  echo " --- moving $M_PORT rosbags"
  for BAG in $M_PORT*.bag
  do
    scp $BAG 10.0.161.123:/media/raid/mmoreaux_raid &&
    rm $BAG &
  done

done

sleep 5
echo ""
echo " --- moving $M_PORT rosbags"
for BAG in $M_PORT*.bag
do
  scp $BAG 10.0.161.123:/media/raid/mmoreaux_raid &&
  rm $BAG &
done


sleep 10
pkill roscore
pkill naoqi_driver
pkill rviz
pkill rosbag
pgrep -f nodelet | xargs kill
pgrep -f object_recognition_core | xargs kill

