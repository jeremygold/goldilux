import cv2
import numpy as np

num_strings = 16
laser_layer = None

def lasers(depth, rgb):
    global laser_layer
    width = depth.shape[1]
    if (type(laser_layer) is not np.ndarray): 
        laser_layer = depth.copy()

    for i in range(1,num_strings + 1):
        x = float(i) * width / num_strings 
        laser_layer = cv2.line(laser_layer, (int(x), 0), (int(x), 200), [0, 0,255], 5)

    laser_layer = cv2.blur(laser_layer, (5, 5))

    for i in range(1,num_strings + 1):
        x = float(i) * width / num_strings 
        laser_layer = cv2.line(laser_layer, (int(x), 0), (int(x), 200), [255, 255, 255], 3)

    depth = cv2.add(depth, laser_layer)
    return depth, rgb
