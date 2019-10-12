import cv2
import numpy as np

threshold = 110
current_depth = 0
# threshold = 177
# current_depth = 574
y_threshold = 300

def change_threshold(value):
    global threshold
    threshold = value

def change_depth(value):
    global current_depth
    current_depth = value

def depth_threshold(depth, rgb, model):
    global threshold
    global current_depth
    depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)

    return depth, rgb
