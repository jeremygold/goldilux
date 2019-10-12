import cv2
import numpy as np

laser_layer = None

def lasers(depth, rgb, model):
    global laser_layer
    active_string = model["active_string"]
    num_strings = model["num_strings"]

    width = depth.shape[1]
    laser_layer = depth.copy()

    for i in range(1, num_strings + 1):
        if i == active_string:
            color = [0, 255, 0]
        else: 
            color = [0, 0, 255]

        x = float(i) * width / num_strings
        laser_layer = cv2.line(laser_layer, (int(x), 0), (int(x), 200), color, 10)

    laser_layer = cv2.blur(laser_layer, (15, 15))

    for i in range(1,num_strings + 1):
        x = float(i) * width / num_strings
        laser_layer = cv2.line(laser_layer, (int(x), 0), (int(x), 200), [255, 255, 255], 3)

    depth = cv2.add(depth, laser_layer)
    return depth, rgb
