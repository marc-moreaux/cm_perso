

print_help () {
	echo ""
	echo "---- launch table reco with roscore"
	echo "-- usage : my_ROS_view_plans.sh"
	echo "-- ex : my_ROS_view_plans.sh 12345"
	echo ""
}



if [ -z "$1" ]
then
	print_help
	exit
fi


echo ""
echo "---- launching on port $1 : "
echo "-- nodelet_manager "
echo "-- nodelet depth_registered/image_rect "
echo "-- nodelet depth_registered/points "


# launch nodlet manager
rosrun nodelet nodelet manager __name:=nodelet_manager &




ROS_MASTER_URI=http://10.0.160.147:$1/

# with the 2 following nodlets, rectify the rgb image and the depth point cloud so they match together.
rosrun nodelet nodelet load depth_image_proc/register nodelet_manager __name:=nodelet1 \
rgb/camera_info:=/$1/camera/front/camera_info \
depth/camera_info:=/$1/camera/depth/camera_info \
depth/image_rect:=/$1/camera/depth/image_raw \
depth_registered/image_rect:=/$1/camera/depth_registered/image_rect &

rosrun nodelet nodelet load depth_image_proc/point_cloud_xyzrgb nodelet_manager __name:=nodelet2 \
rgb/camera_info:=/$1/camera/front/camera_info \
rgb/image_rect_color:=/$1/camera/front/image_raw \
depth_registered/image_rect:=/$1/camera/depth_registered/image_rect \
points:=/$1/camera/depth_registered/points &


# with the 2 following nodlets, rectify the rgb image and the depth point cloud so they match together.
rosrun nodelet nodelet load depth_image_proc/register nodelet_manager __name:=nodelet1 \
rgb/camera_info:=/naoqi_driver_node/camera/front/camera_info \
depth/camera_info:=/naoqi_driver_node/camera/depth/camera_info \
depth/image_rect:=/naoqi_driver_node/camera/depth/image_raw \
depth_registered/image_rect:=/naoqi_driver_node/camera/depth_registered/image_rect &

rosrun nodelet nodelet load depth_image_proc/point_cloud_xyzrgb nodelet_manager __name:=nodelet2 \
rgb/camera_info:=/naoqi_driver_node/camera/front/camera_info \
rgb/image_rect_color:=/naoqi_driver_node/camera/front/image_raw \
depth_registered/image_rect:=/naoqi_driver_node/camera/depth_registered/image_rect \
points:=/naoqi_driver_node/camera/depth_registered/points &



#rosrun object_recognition_core detection -c `rospack find object_recognition_linemod`/conf/detection_pepper.ros.ork
rosrun object_recognition_core detection -c `rospack find object_recognition_tabletop`/conf/detection_$1.table.ros.ork &
