


source /home/mmoreaux/.bashrc
source /home/mmoreaux/.bashindigo



echo "#################################"
echo "###    Launch a roscore "
echo "#################################"
roscore &
sleep 3

# For every of these bags, extract the sound and pictures then make the videos
for BAGS_DIR in {toAnotate10/ toAnotate3/ toAnotate6/ toAnotate8/ goodBags5/ toAnotate11/ toAnotate5/ toAnotate7/ toAnotate9/}
do
	cd $BAGS_DIR


	echo "#################################"
	echo "### For every bag in the folder "
	echo "### 1st - run a image extractor "
	echo "### 2nd - run a rosbag "
	echo "#################################"
	for M_BAG in *.bag
	do
		echo "###  converting $M_BAG"
		echo ""
		mkdir image${M_BAG%.bag}
		cd image${M_BAG%.bag}

		# Get the ip to have the proper topic name
		if [[ $M_BAG == *"12345"* ]]
		then
			M_PORT=12345
		elif [[ $M_BAG == *"12346"* ]]
		then
			M_PORT=12346
		elif [[ $M_BAG == *"12347"* ]]
		then
			M_PORT=12347
		fi


		# Run the image extractor and run the rosbag
		rosrun image_view extract_images _sec_per_frame:=0.01 image:=/$M_PORT/camera/front/image_raw &
		sleep 1
		echo "source /home/mmoreaux/.bashrc
	source /home/mmoreaux/.bashindigo
	rosbag play $BAGS_DIR/$M_BAG 
	" | bash &

		cd $BAGS_DIR
		TIME=160
		sleep $TIME

		# Kill the image_view module
		pgrep -f image_view | xargs kill
	done

	echo "#################################"
	echo "### For every bag in the folder, "
	echo "###  extract the sound "
	echo "#################################"
	python ~/catkin_ws_recording/src/naoqi_listen/bag_listen.py $BAGS_DIR



	for M_BAG in *.bag
	do
		BAG_LENGHT=$(rosbag info $M_BAG | grep "duration:" | grep -o "[0123456798.]*" | grep -o "[0123456789.]*$" | tail -1)
		cd image${M_BAG%.bag}
		# count objects
		SUM=0; for a in *jpg; do SUM=$(( $SUM+1 )) ; done
		FPS=`bc -l <<< $SUM/$BAG_LENGHT`

		mencoder -audiofile ../${M_BAG%.bag}.wav -oac copy mf://*.jpg -mf w=320:h=240:type=jpg:fps=$FPS -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=2400 :mbd=2:keyint=132:v4mv:vqmin=3:lumi_mask=0.07:dark_mask=0.2:mpeg_quant:scplx_mask=0.1:tcplx_mask=0.1:naq -o whatever.avi &
		cd $BAGS_DIR
	done


	sleep 15
	cd $BAGS_DIR
	tar cfzv videos.tar.gz image*/whatever.avi

done