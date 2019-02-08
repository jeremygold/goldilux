#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import numpy as np


threshold = 100
current_depth = 0
last_image = None

def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value


def show_depth():
    global threshold
    global current_depth
    global last_image

    depth, timestamp = freenect.sync_get_depth()
    depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    h, w = depth.shape[:2]

    if(last_image != None):
        scaled = cv2.resize(last_image, None, fx=1.1, fy=1.1)[0:h,0:w]

        image = cv2.add(scaled, depth)

        last_image = cv2.bitwise_not(image)
        cv2.imshow('Depth', image)
    else:
        last_image = depth


def show_video():
    cv2.imshow('Video', frame_convert2.video_cv(freenect.sync_get_video()[0]))


cv2.namedWindow('Depth')
cv2.namedWindow('Video')
cv2.createTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
cv2.createTrackbar('depth',     'Depth', current_depth, 2048, change_depth)

print('Press ESC in window to stop')


while 1:
    show_depth()
    # show_video()
    if cv2.waitKey(10) == 27:
        break
