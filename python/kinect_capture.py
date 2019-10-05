# import freenect

class KinectCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        # depth, timestamp = freenect.sync_get_depth()
        # rgb = frame_convert2.video_cv(freenect.sync_get_video()[0])
        return depth, rgb