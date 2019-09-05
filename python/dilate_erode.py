import cv2
import numpy as np

def dilate_erode(depth, rgb):
    kernel = np.ones((5,5), np.uint8) 
    depth = cv2.dilate(depth, kernel, iterations=1)
    depth = cv2.erode(depth, kernel, iterations=1)
    return depth, rgb
