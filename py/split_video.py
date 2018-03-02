#!/usr/bin/python

''' Python video slicer
Takes a video path as input and produces 30 seconds slices of this video

Example output:
./parser.py --input './kitchen_001a.mp4' --output_path slices --text_formating 1
'''

import os
import subprocess
import argparse
import re


def get_video_length(file_path):
    '''Retrun the lenght of a video in seconds
    '''
    result = subprocess.Popen(["ffprobe", file_path],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    duration = [x for x in result.stdout.readlines() if "Duration" in x][0]
    # '  Duration: 00:09:45.05, start: 0.000000, bitrate: 12001 kb/s\n'
    regex = '[\d]+:[\d]+:[\d]+'
    time = re.search(regex, duration).group(0)
    _hour, _min, _sec = time.split(":")
    time_sec = int(_hour) * 60 * 60 + int(_min) * 60 + int(_sec)
    return time_sec


def get_args():
    '''Parse the arguments recieved'''
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Script splits a video into slices')
    # Add arguments
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help='input video to split',
        required=True)
    parser.add_argument(
        '-o',
        '--output_path',
        type=str,
        help='output path where to store the videos',
        required=False,
        default='./slices/')
    parser.add_argument(
        '-f',
        '--text_formating',
        type=int,
        help='Wether to use video index(1) or time(2)',
        required=False,
        default=1)
    args = parser.parse_args()
    return args


def split_videos(cwd, dest_d, video_name, args):
    ''' Takes a video of many minutes as input and splits it into 30 seconds splits

    Arguments
        cwd: current working directory (str)
        dest_d: destination directory (str)
        video_name: name of the video (str)
    '''
    video_path = os.path.join(cwd, video_name)
    
    # Maybe create the directory
    if not os.path.isdir(dest_d):
        os.makedirs(dest_d)

    # Split in 30 seconds slices
    video_lenght = get_video_length(video_path)
    for i, t in enumerate(range(0, video_lenght, 30)):
        time = '00:{:02d}:{:02d}'.format(t/60, t%60)
        if args.text_formating == 1:
            output_file = video_name.split('.')[0] + '_{0:0=3d}.mp4'.format(i)
        else:
            output_file = video_name.split('.')[0] + '_{}.mp4'.format(time)
        video_cpy_path = os.path.join(dest_d, output_file)
        
        # Maybe delete existing file
        if os.path.isfile(video_cpy_path):
            print 'deleting {}'.format(video_cpy_path)
            os.remove(video_cpy_path)

        # Do the copy
        cmd = 'ffmpeg -i {} -ss {} -t 00:00:30.00 -vcodec h264 -acodec mp3 {}'.format(
            video_path,
            time,
            video_cpy_path)
        print cmd
        subprocess.call([cmd], shell=True)


if __name__ == "__main__":
    # read the arguments
    args = get_args()
    video_path = args.input
    cwd = os.path.dirname(video_path)
    dest_d = os.path.join(cwd, args.output_path)
    video_name = os.path.basename(video_path)

    # Call the splitting function
    split_videos(cwd, dest_d, video_name, args)

    
