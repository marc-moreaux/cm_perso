#!/usr/bin/python

''' Python video slicer
Takes a video path as inout and produces 30 seconds slices of this video

Example output:
./parser.py --input './YDXJ0007.mp4' --output_path slices
'''

import os
import subprocess
import argparse


def get_args():
    '''Parse the arguments recieved'''
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Script splits a video into slices')
    # Add arguments
    parser.add_argument(
        '-i', '--input', type=str, help='input video to split', required=True)
    parser.add_argument(
        '-o', '--output_path', type=str, help='output path where to store the videos',
        required=False, default='./slices/')
    args = parser.parse_args()
    return args

# read the arguments
args = get_args()
video_path = args.input
cwd = os.path.dirname(video_path)
dest_d = os.path.join(cwd, 'slices')
video_name = os.path.basename(video_path)

# Maybe create the directory
if not os.path.isdir(dest_d):
    os.makedirs(dest_d)

# Split in 30 seconds slices
for t in range(0, 60*14, 30):
    time = '00:{:02d}:{:02d}'.format(t/60, t%60)
    output_file = video_name.split('.')[0] + '_' + time + '.' + video_name.split('.')[1]
    video_cpy_path = os.path.join(dest_d + output_file)
    
    # Maybe delete existing file
    if os.path.isfile(video_cpy_path):
        print 'deleting {}'.format(video_cpy_path)
        os.remove(video_cpy_path)
    # Do the copy
    cmd = 'ffmpeg -i {} -ss {} -t 00:00:30.00 -vcodec h264 -acodec mp3 {}'.format(
        os.path.join(cwd, video_name),
        time,
        video_cpy_path)
    print cmd
    subprocess.call([cmd], shell=True)


    
