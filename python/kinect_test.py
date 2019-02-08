#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import numpy as np
import random
import paho.mqtt.client as mqtt


threshold = 200
current_depth = 500
last_image = None
scale = 1.05
client = None

def change_threshold(value):
    global threshold
    threshold = value

def change_depth(value):
    global current_depth
    current_depth = value

def show_depth(warp = False):
    global threshold
    global current_depth
    global last_image
    global client

    depth, timestamp = freenect.sync_get_depth()
    rgb = frame_convert2.video_cv(freenect.sync_get_video()[0])
    depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    depth_rgb = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
    h, w = depth.shape[:2]

    if(last_image != None):
        x_offset = int(w * (scale - 1.0) / 2.0)
        y_offset = int(h * (scale - 1.0) / 2.0)
        scaled = cv2.resize(last_image, None, fx=scale, fy=scale)[y_offset:h+y_offset,x_offset:w + x_offset]

        color_img = np.zeros((h, w, 3), dtype=np.uint8)
        color_img[:, :] = [random.randint(1,255), random.randint(1,255), random.randint(1,255)]

        color_scale = cv2.bitwise_and(color_img, scaled)
        image = cv2.bitwise_or(color_scale, depth_rgb)

        overlay = cv2.bitwise_xor(rgb, image)

        m = cv2.moments(depth)
        cX = int(m["m10"] / m["m00"])
        cY = int(m["m01"] / m["m00"])

        cv2.circle(overlay, (cX, cY), 15, (255, 0, 255), -1)

        client.publish("test", int(cX / 4.0))

        
#        detector = cv2.SimpleBlobDetector()
#        keypoints = detector.detect(depth)
#        print("Detected " + str(keypoints))
#
#        overlay_with_keypoints = cv2.drawKeypoints(depth, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        if(warp):
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

            warped = cv2.warpPerspective(overlay, M, (w, h))

            cv2.imshow('Depth', warped)
        else:
            cv2.imshow('Depth', overlay)

        last_image = image

    else:
        last_image = depth_rgb

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def init_mqtt():
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect('192.168.1.105', 1883, 60)
    client.loop_start()

cv2.namedWindow('Depth')
# cv2.namedWindow('Video')
cv2.createTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
cv2.createTrackbar('depth',     'Depth', current_depth, 2048, change_depth)

print('Press ESC in window to stop')

init_mqtt()

while 1:
    show_depth()
    if cv2.waitKey(10) == 27:
        break
