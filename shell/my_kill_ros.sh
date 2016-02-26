

pkill roscore
pkill naoqi_driver
pkill rviz
pkill rosbag
pgrep -f nodelet | xargs kill
pgrep -f object_recognition_core | xargs kill