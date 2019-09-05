#!/usr/bin/env python3

import freenect
import cv2
import frame_convert2
import numpy as np

from dilate_erode import dilate_erode
from color_tunnel import color_tunnel
from sobel import sobel
from mask_rgb import mask_rgb
from blob_detect import blob_detect

threshold = 177
current_depth = 574
y_threshold = 300

def change_threshold(value):
    global threshold
    threshold = value

def change_depth(value):
    global current_depth
    current_depth = value

def map_range(a, b, s):
    (a1, a2), (b1, b2) = a, b
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def capture_frame():
    depth, timestamp = freenect.sync_get_depth()
    rgb = frame_convert2.video_cv(freenect.sync_get_video()[0])
    return depth, rgb

def depth_threshold(depth, rgb):
    global threshold
    global current_depth
    depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)

    return depth, rgb


def warp(depth, rgb):
    h, w = depth.shape[:2]
    src = np.array([
        [0,0],
        [w-1,0],
        [w-1,h-1],
        [0,h-1]], dtype= "float32")

    dst = np.array([
        [150,50],
        [w-1,0],
        [w-1,h-1],
        [150,h-51]], dtype= "float32")

    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(depth, M, (w, h))

    return warped, rgb


def run_pipeline(pipeline):
    depth, rgb = capture_frame()

    for step in pipeline:
        depth, rgb = step(depth, rgb)

    cv2.imshow('Depth', depth)


def main():
    cv2.namedWindow('Depth')
    cv2.createTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
    cv2.createTrackbar('depth',     'Depth', current_depth, 2048, change_depth)
    print('Press ESC in window to stop')

    pipeline = [
        depth_threshold,
        blob_detect,
        # dilate_erode,
        sobel,
        color_tunnel
    ]

    while 1:
        run_pipeline(pipeline)
        if cv2.waitKey(10) == 27:
            break

main()
