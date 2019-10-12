import cv2
import numpy as np

def warp(depth, rgb, model):
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

