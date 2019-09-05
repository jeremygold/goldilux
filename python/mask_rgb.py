import cv2

def mask_rgb(depth, rgb):
    depth_mask = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
    rgb = cv2.bitwise_and(rgb,rgb,mask = depth)
    return depth, rgb
