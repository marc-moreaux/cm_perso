

print_help () {
	echo ""
	echo "---- I'll echo you vars given port"
	echo "-- usage : my_ROS_var.sh 12345"

}



if [ -z "$1" ]
then
	print_help
	exit
fi

echo "ROS_MASTER_URI=http://10.0.160.147:$1/"
echo "ROS_NAMESPACE=$1"
