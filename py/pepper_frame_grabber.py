#!/usr/bin/python

''' Pepper frame grabber
Reads frames retrieved from pepper

Example output:
./pepper_frame_grabber --ip 10.0.10.1
'''

import naoqi
from naoqi import ALProxy
import vision_definitions
import argparse
import time

import numpy as np
from PIL import Image
import cv2


def get_args():
    '''Parse the arguments recieved'''
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Reads frames retrieved from pepper')
    # Add arguments
    parser.add_argument(
        '-i', '--ip', type=str, help='IP of your pepper', required=True)
    parser.add_argument(
        '-p', '--port', type=int, help='Port to connect to',
        required=False, default=10)
    parser.add_argument(
        '-f', '--frames', type=int, help='Amount of frames to grab',
        required=False, default=10)
    parser.add_argument(
        '-r', '--return_img', type=bool, help='Return the frame as string',
        required=False, default=False)
    args = parser.parse_args()
    return args


class Stream:
    """
    Manage here an image comming from naoqi.
    """

    port = 9559
    resolution = 2    # VGA
    colorSpace = 11   # RGB

    def __init__(self, ip, port=-1):
        if(port != -1):
            self.port = port
        self.ip = ip

        self.camProxy = ALProxy("ALVideoDevice", ip, self.port)
        self.videoClient = self.camProxy.subscribe("python_client", self.resolution, self.colorSpace, 5)
        cv2.namedWindow("myWindow")
        cv2.setMouseCallback('myWindow', self.onmouse)

        self.selection = None
        self.drag_start = None
        self.tracking_state = 0
        self.show_backproj = False

    def onmouse(self, event, x, y, flags, param):
        x, y = np.int16([x, y]) # BUG
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
            self.tracking_state = 0
        if self.drag_start:
            if flags & cv2.EVENT_FLAG_LBUTTON:
                h, w = self.image.shape[:2]
                xo, yo = self.drag_start
                x0, y0 = np.maximum(0, np.minimum([xo, yo], [x, y]))
                x1, y1 = np.minimum([w, h], np.maximum([xo, yo], [x, y]))
                self.selection = None
                if x1-x0 > 0 and y1-y0 > 0:
                    self.selection = (x0, y0, x1, y1)
            else:
                self.drag_start = None
                if self.selection is not None:
                    self.tracking_state = 1

    def getImage(self):
        t0 = time.time()
        naoImage = self.camProxy.getImageRemote(self.videoClient)
        t1 = time.time()
        print "acquisition delay ", t1 - t0

        self.imWidth = naoImage[0]
        self.imHeight = naoImage[1]
        self.array = naoImage[6]
        _image = Image.frombytes("RGB", (self.imWidth, self.imHeight), self.array)
        self.image = np.array(_image)
        self.image = self.image[:, :, ::-1].copy()
        cv2.imshow('myWindow', self.image)
        ch = 0xFF & cv2.waitKey(5)
        return ch
        
    def __del__(self):
        self.camProxy.unsubscribe(self.videoClient);
        cv2.destroyAllWindows()


args = get_args()
ip = args.ip
port = args.port
n_frames = args.frames

im = Stream(ip, port)
if args.return_img is True:
    im.getImage()
    print 'image :'
    print str(im.image)
else:
    for i in range(n_frames):
        key = im.getImage()
        if key == 27:
            break
del im