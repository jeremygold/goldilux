#!/usr/bin/env python3
import freenect
import cv2
import frame_convert2
import numpy as np
import random
import paho.mqtt.client as mqtt

threshold = 400
current_depth = 260
last_image = None
scale = 1.10
client = None
y_threshold = 300
last_note = -1

def change_threshold(value):
    global threshold
    threshold = value

def change_depth(value):
    global current_depth
    current_depth = value

def map_range(a, b, s):
    (a1, a2), (b1, b2) = a, b
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def show_depth(warp = False):
    global threshold
    global current_depth
    global last_image
    global client
    global last_note

    depth, timestamp = freenect.sync_get_depth()
    rgb = frame_convert2.video_cv(freenect.sync_get_video()[0])
    depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    depth_rgb = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
    h, w = depth.shape[:2]

    if(not last_image is None):
        x_offset = int(w * (scale - 1.0) / 2.0)
        y_offset = int(h * (scale - 1.0) / 2.0)
        scaled = cv2.resize(last_image, None, fx=scale, fy=scale)[y_offset:h+y_offset,x_offset:w + x_offset]

        color_img = np.zeros((h, w, 3), dtype=np.uint8)
        color_img[:, :] = [random.randint(1,255), random.randint(1,255), random.randint(1,255)]

        color_scale = cv2.bitwise_and(color_img, scaled)
        image = cv2.bitwise_or(color_scale, depth_rgb)

        # overlay = cv2.bitwise_xor(rgb, image)
        cv2.line(image, (0, y_threshold), (w, y_threshold), (0, 255, 0), 3)

        # overlay_with_keypoints = cv2.drawKeypoints(overlay, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        if True:
            params = cv2.SimpleBlobDetector_Params()
            params.minThreshold = 0
            params.maxThreshold = 255
            params.minArea = 200
            params.maxArea = w * h
            params.filterByArea = True

            params.filterByCircularity = False
            params.filterByConvexity = False
            params.filterByColor = False
            params.filterByInertia = False


            detector = cv2.SimpleBlobDetector_create(params)
            keypoints = detector.detect(depth)
            print("Detected " + str(len(keypoints)))
            for keypoint in keypoints:
                cX = int(keypoint.pt[0])
                cY = int(keypoint.pt[1])
                    
                location = str(cX) + "," + str(cY)
                cv2.circle(image, (cX, cY), 15, (255, 0, 255), -1)
                cv2.putText(image, location, (cX-25, cY-25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

                # if(last_note >= 0):
                #     # Already playing a note
                #     if(cY > y_threshold):
                #         # Center is below line, stop playing
                #         client.publish("note-off", last_note)
                #         last_note = -1
                #     else:
                #         # Center is still above the line, leave current note
                #         client.publish("note-off", last_note)
                #         note = int(map_range((0, w), (88, 0), cX))
                #         # Only change if we've moved by 2 semitones
                #         if(abs(note - last_note) > 2):
                #             last_note = note
                #             client.publish("note-on", note)
                #         pass
                # else:
                #     # No active note
                #     if(cY < y_threshold):
                #         # Center is above the line, start a new note
                #         note = int(map_range((0, w), (88, 0), cX))
                #         last_note = note
                #         client.publish("note-on", note)

                #     else:
                #         # Center is below the line, don't start anything
                #         pass


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
            # cv2.imshow('Depth', overlay)
            cv2.imshow('Depth', image)

        last_image = image

    else:
        last_image = depth_rgb

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def init_mqtt():
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    # At home
    client.connect('192.168.1.105', 1883, 60)
    # At work
    # client.connect('192.168.5.184', 1883, 60)
    client.loop_start()

cv2.namedWindow('Depth')
# cv2.namedWindow('Video')
cv2.createTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
cv2.createTrackbar('depth',     'Depth', current_depth, 2048, change_depth)

print('Press ESC in window to stop')

# init_mqtt()

while 1:
    show_depth()
    if cv2.waitKey(10) == 27:
        break
