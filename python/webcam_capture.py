import cv2

class WebcamCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        _, frame = self.cap.read()
        depth = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        rgb = frame
        return depth, rgb