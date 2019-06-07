#!/usr/bin/env python3
import cv2
import paho.mqtt.client as mqtt
import threading

client = None
lastNote = None
note1On = False

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    global midiout
    print(msg.topic + ": " + str(msg.payload))


def nothing(x):
    pass


def init_mqtt():
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.1.229", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_start()


def init():
    cv2.namedWindow('Laser')
    cv2.createTrackbar("Threshold", "Laser", 0, 255, nothing)
    cv2.setTrackbarPos("Threshold", "Laser", 180)

    cv2.createTrackbar("Note1", "Laser", 0, 1024, nothing)
    cv2.setTrackbarPos("Note1", "Laser", 290)

    cv2.createTrackbar("Note2", "Laser", 0, 1024, nothing)
    cv2.setTrackbarPos("Note2", "Laser", 390)

    cv2.createTrackbar("Note3", "Laser", 0, 1024, nothing)
    cv2.setTrackbarPos("Note3", "Laser", 490)


def noteOff(note):
    global client
    client.publish("note-off", note)


def show_webcam():
    global client
    global lastNote
    global note1On

    cam = cv2.VideoCapture(0)
    cam.set(3, 1280)
    cam.set(4, 1024)

    while True:
        ret_val, img = cam.read()

        b, g, r = cv2.split(img)

        thresh = cv2.getTrackbarPos("Threshold", "Laser")
        note1Y = cv2.getTrackbarPos("Note1", "Laser")

        ret, thresh1 = cv2.threshold(r, thresh, 255, cv2.THRESH_BINARY)

        note1Crop = thresh1[note1Y:note1Y+50, 0:1280]
        note1Sum = cv2.countNonZero(note1Crop)

        lastNote = 60
        if note1On == False:
            if note1Sum < 100:
                print("Playing note: " + str(note1Sum))
                note1On = True
                client.publish("note-on", lastNote)

        if note1Sum > 100:
            print("Stopping note: " + str(note1Sum))
            note1On = False
            client.publish("note-off", lastNote)

        # print("Note1Sum: " + str(note1Sum))

        cv2.rectangle(thresh1, (0, note1Y), (1280, note1Y + 50), (255), 2)
        cv2.imshow('Laser', thresh1)

        key = cv2.waitKey(1)

        if key != -1:
            print("Key: ", str(key))
        if key == 27:
            client.loop_stop(force=False)
            break  # esc to quit
        elif key >= 97:
            lastNote = key - 37
            client.publish("note-on", lastNote)
            timer = threading.Timer(1.0, noteOff, [lastNote])
            timer.start()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    init()
    init_mqtt()
    show_webcam()
