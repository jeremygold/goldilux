import cv2

def sobel(depth, rgb, model):
    hSobel = cv2.Sobel(depth, cv2.CV_32F, 0, 1, -1)
    vSobel = cv2.Sobel(depth, cv2.CV_32F, 1, 0, -1)
    depth = cv2.add(hSobel, vSobel)

    depth = cv2.convertScaleAbs(depth)
    depth = cv2.GaussianBlur(depth, (3, 3), 0)
    _, depth = cv2.threshold(depth, 80, 255, cv2.THRESH_BINARY)
    return depth, rgb
