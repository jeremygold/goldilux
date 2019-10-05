#!/usr/bin/env python3
# import freenect

import frame_convert2
import numpy as np
import cv2

from webcam_capture import WebcamCapture
from dilate_erode import dilate_erode
from color_tunnel import color_tunnel
from sobel import sobel
from mask_rgb import mask_rgb
from blob_detect import blob_detect
from depth_threshold import *
from warp import warp

def run_pipeline(pipeline, capture):
    # depth, timestamp = freenect.sync_get_depth()
    # rgb = frame_convert2.video_cv(freenect.sync_get_video()[0])
    depth, rgb = capture.get_frame()

    for step in pipeline:
        depth, rgb = step(depth, rgb)

    cv2.imshow('Depth', depth)

def main():
    global cap
    cv2.namedWindow('Depth')
    cv2.createTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
    cv2.createTrackbar('depth',     'Depth', current_depth, 2048, change_depth)
    print('Press ESC in window to stop')

    pipeline = [
        depth_threshold,
        # blob_detect,
        # dilate_erode,
        sobel,
        color_tunnel,
        warp
    ]

    capture = WebcamCapture()

    while 1:
        run_pipeline(pipeline, capture)
        if cv2.waitKey(10) == 27:
            break

main()
