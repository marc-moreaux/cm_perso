


source /home/mmoreaux/.bashrc
source /home/mmoreaux/.bashindigo

# source /home/mmoreaux/catkin_ws_ork/devel/setup.bash

# for M_PORT in {12345..12347}
# do 
#   if [ "$M_PORT" = "12345" ]
#   then
#     sourceindigo
#     NAO_IP='jarc.local'
#   elif [ "$M_PORT" = "12346" ]
#   then
#     sourceindigo
#     NAO_IP='aipepper3.local'
#   else
#     source ~/work/catkin_ws_naoqi_driver/devel/setup.bash
#     NAO_IP='pepperlaurent.local'
#   fi
#   export ROS_MASTER_URI=http://$ROS_IP:$M_PORT/
#   export ROS_NAMESPACE=$M_PORT
#   echo "$M_PORT"


#   echo ""
#   echo "################################"
#   echo "    launching roscore at :   "
#   echo "  $ROS_MASTER_URI       "
#   echo "################################"

#   roscore -p $M_PORT &
#   sleep 5  
  
# done


roscore &


# go to folder with rosbags
cd ~/rosbag/test/

for M_PORT in {12345..12347}
do
	mkdir image$M_PORT
	cd image$M_PORT

	ROS_MASTER_URI=http://10.0.160.147:$M_PORT/
	ROS_NAMESPACE=$M_PORT
	
	rosrun image_view extract_images _sec_per_frame:=0.01 image:=/$M_PORT/camera/front/image_raw &

	cd ..
done

TIME=30
sleep $TIME
pgrep -f image_view | xargs kill



for M_PORT in {12345..12347}
do
	cd image$M_PORT
	# count objects
	SUM=0; for a in *jpg; do SUM=$(( $SUM+1 )) ; done
	FPS=`bc -l <<< $SUM/$TIME`

	mencoder -audiofile  mf://*.jpg -mf w=320:h=240:type=jpg:fps=$FPS -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=2400 :mbd=2:keyint=132:v4mv:vqmin=3:lumi_mask=0.07:dark_mask=0.2:mpeg_quant:scplx_mask=0.1:tcplx_mask=0.1:naq -o whatever.avi &

	cd ..
done

