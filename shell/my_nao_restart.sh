#!/bin/bash


print_help () {
	echo ""
	echo "---- restart the naoqi on a distant machine"
	echo "-- usage : nao_restart.sh distIP"
	echo "-- ex : nao_restart.sh jarc.local"
	echo "-- or : nao_restart.sh 10.0.164.12"
	echo ""
}


if [ -z "$1" ]
then
	print_help
	exit
fi


echo ""
echo "-- restarting naoqi on $1"

# ssh nao@$1 "echo 'sudo /etc/init.d/naoqi restart' > tmp.sh"
# ssh nao@$1 "chmod u+x /home/nao/tmp.sh"
# ssh -f nao@$1 "/home/nao/tmp.sh >/dev/null"

ssh -f nao@$1 "sudo /etc/init.d/naoqi restart &>/dev/null"




# for NAO_IP in jarc.local aipepper3.local pepperlaurent.local
# do
# ssh -f nao@$NAO_IP "qicli call ALMotion.setAngles HeadYaw 0 0.5" &&
# sleep 1 &&
# ssh -f nao@$NAO_IP "qicli call ALMotion.setAngles HeadPitch .4 0.5" &
# done


