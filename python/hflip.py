import cv2

def hflip(depth, rgb, model):
    depth = cv2.flip(depth, 1)

    return depth, rgb
