#!/usr/bin/env python

import numpy as np
import cv2

lastImage = None

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    h = cv2.Sobel(frame, cv2.CV_32F, 0, 1, -1)
    v = cv2.Sobel(frame, cv2.CV_32F, 1, 0, -1)
    img = cv2.add(h, v)


    img = cv2.convertScaleAbs(img)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    ret, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
    if not lastImage is None:
        img = cv2.addWeighted(img, 1.0, lastImage, 0.9, 0.5)
    lastImage = img

    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()