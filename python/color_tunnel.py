import cv2
import numpy as np
import random

last_image = None
scale = 1.10

def color_tunnel(depth, rgb, model):
    global last_image

    if(not last_image is None):
        h, w = depth.shape[:2]
        x_offset = int(w * (scale - 1.0) / 2.0)
        y_offset = int(h * (scale - 1.0) / 2.0)
        scaled = cv2.resize(last_image, None, fx=scale, fy=scale)[y_offset:h+y_offset,x_offset:w + x_offset]

        kernel = np.ones((5,5), np.uint8) 
        scaled = cv2.dilate(scaled, kernel, iterations = 1)

        color_img = np.zeros((h, w, 3), dtype=np.uint8)
        color_img[:, :] = [random.randint(1,255), random.randint(1,255), random.randint(1,255)]

        color_scale = cv2.bitwise_and(color_img, scaled)
        depth = cv2.bitwise_or(color_scale, depth)


    last_image = depth
    return depth, rgb