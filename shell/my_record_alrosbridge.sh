
#######################################
#       Setup on the machine
# with 10.00.00.00 the ip of the robot
#######################################
# git clone git@gitlab.aldebaran.lan:ros/alrosbridge_package.git
# cd alrosbridge_package/
# ./update_pkg.sh atom 10.00.00.00



# IP of the computer
ROSCORE_IP=10.0.160.147


shopt -s expand_aliases
cd /home/mmoreaux/rosbag
pwd
source /home/mmoreaux/.bashrc
source /home/mmoreaux/.bashindigo
source /home/mmoreaux//catkin_ws_ork/devel/setup.bash



for M_PORT in {12345..12347}
do 

	export ROS_MASTER_URI=http://10.0.160.147:$M_PORT/
	echo ""
	echo "################################"
	echo "    launching roscore at :   "
	echo "  $ROS_MASTER_URI       "
	echo "################################"


	roscore -p $M_PORT &
	sleep 5


	# Connect the robots to this roscore
	if [ "$M_PORT" = "12345" ]
	then
		M_NAO_IP=jarc.local
	elif [ "$M_PORT" = "12346" ]
	then
		M_NAO_IP=aipepper3.local
	else
		M_NAO_IP=10.0.164.58
	fi

	echo ""
	echo "--launch rosbridge on robot"


	ssh nao@$M_NAO_IP "echo '
#!/bin/sh
sudo /etc/init.d/naoqi restart
sleep 60
export ROS_NAMESPACE=$M_PORT
cd alrosbridge
echo -- launch rosbridge
bash ./run.sh & 
echo -- waiting for rosbridge to launch
sleep 45
echo -- re-routing to good roscore port
qicli call ALRosBridge.setMasterURI http://$ROSCORE_IP:$M_PORT
' > rosbridge.sh "
	ssh nao@$M_NAO_IP "chmod u+x /home/nao/rosbridge.sh"
	ssh -f nao@$M_NAO_IP "/home/nao/rosbridge.sh >/dev/null"

done

sleep 150





for WHATEVER in {1..12}
do
	echo ""
	echo "################################"
	echo "    Recording rosbags   "
	echo "################################"
	for M_PORT in {12345..12347}
	do
		export ROS_MASTER_URI=http://10.0.160.147:$M_PORT/
		rosbag record -o $M_PORT \
		/$M_PORT/alrosbridge/audio \
		/$M_PORT/alrosbridge/camera/depth/camera_info \
		/$M_PORT/alrosbridge/camera/depth/image_raw \
		/$M_PORT/alrosbridge/camera/bottom/camera_info \
		/$M_PORT/alrosbridge/camera/bottom/image_raw \
		/$M_PORT/alrosbridge/camera/front/camera_info \
		/$M_PORT/alrosbridge/camera/front/image_raw \
		/diagnostics_agg \
		/joint_states \
		/tf &
	done
	sleep 300 # record 5 minutes
	echo ""
	echo " --- moving rosbags"

done




# scp FILE 10.0.161.123:/media/raid/mmoreaux_raid




# M_PORT=12346
# M_NAO_IP=aipepper3.local
# ROSCORE_IP=10.0.160.147







# /$M_PORT/alrosbridge/audio \
# /$M_PORT/alrosbridge/camera/depth/camera_info \
# /$M_PORT/alrosbridge/camera/depth/image_raw \
# /$M_PORT/alrosbridge/camera/bottom/camera_info \
# /$M_PORT/alrosbridge/camera/bottom/image_raw \
# /$M_PORT/alrosbridge/camera/front/camera_info \
# /$M_PORT/alrosbridge/camera/front/image_raw \
# /diagnostics_agg \
# /joint_states \
# /tf
