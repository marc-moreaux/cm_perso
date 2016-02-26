#!/bin/bash

print_help(){
	echo ""
	echo " --se déplacer sur le serveur"
}

ssh -t 10.0.161.123 "cd /media/raid/mmoreaux_raid/ ; bash"