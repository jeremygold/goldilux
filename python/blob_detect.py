import cv2

def blob_detect(depth, rgb):
    h, w = depth.shape[:2]

    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 0
    params.maxThreshold = 255
    params.minArea = 200
    params.maxArea = w * h
    params.filterByArea = True

    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByColor = False
    params.filterByInertia = False

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(depth)
    print("Detected " + str(len(keypoints)))
    for keypoint in keypoints:
        cX = int(keypoint.pt[0])
        cY = int(keypoint.pt[1])
        radius = int(keypoint.size / 2.0)
        # put circle at top of detected blob
        cY -= radius
            
        location = str(cX) + "," + str(cY)
        cv2.circle(depth, (cX, cY), 10, (255, 0, 255), -1)
        cv2.putText(depth, location, (cX-25, cY-25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        # if(last_note >= 0):
        #     # Already playing a note
        #     if(cY > y_threshold):
        #         # Center is below line, stop playing
        #         client.publish("note-off", last_note)
        #         last_note = -1
        #     else:
        #         # Center is still above the line, leave current note
        #         client.publish("note-off", last_note)
        #         note = int(map_range((0, w), (88, 0), cX))
        #         # Only change if we've moved by 2 semitones
        #         if(abs(note - last_note) > 2):
        #             last_note = note
        #             client.publish("note-on", note)
        #         pass
        # else:
        #     # No active note
        #     if(cY < y_threshold):
        #         # Center is above the line, start a new note
        #         note = int(map_range((0, w), (88, 0), cX))
        #         last_note = note
        #         client.publish("note-on", note)

        #     else:
        #         # Center is below the line, don't start anything
        #         pass
    # image = depth

    # overlay = cv2.bitwise_xor(rgb, image)
    # cv2.line(image, (0, y_threshold), (w, y_threshold), (0, 255, 0), 3)

    # overlay_with_keypoints = cv2.drawKeypoints(overlay, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return depth, rgb