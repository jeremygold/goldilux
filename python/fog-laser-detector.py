#!/usr/bin/env python3
import cv2
import paho.mqtt.client as mqtt
import threading

client = None
lastNote = None
note1On = False
width = 500

noteOn = {
    "Note1": False,
    "Note2": False,
    "Note3": False
}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


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
    cv2.setTrackbarPos("Threshold", "Laser", 100)

    cv2.createTrackbar("Note1", "Laser", 0, 1024, nothing)
    cv2.setTrackbarPos("Note1", "Laser", 276)

    cv2.createTrackbar("Note2", "Laser", 0, 1024, nothing)
    cv2.setTrackbarPos("Note2", "Laser", 338)

    cv2.createTrackbar("Note3", "Laser", 0, 1024, nothing)
    cv2.setTrackbarPos("Note3", "Laser", 425)


def noteOff(note):
    global client
    client.publish("note-off", note)


def checkNote(thresh, slider, note):
    noteY = cv2.getTrackbarPos(slider, "Laser")
    noteCrop = thresh[noteY:noteY+50, 0:width]
    noteSum = cv2.countNonZero(noteCrop)

    if noteOn[slider] == False:
        if noteSum < 100:
            print("Playing note: " + str(note) + "sum: " + str(noteSum))
            noteOn[slider] = True
            client.publish("note-on", note)

    if noteSum > 100:
        print("Stopping note: " + str(note) + "sum: " + str(noteSum))
        noteOn[slider] = False
        client.publish("note-off", note)

    return noteY


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
        ret, thresh1 = cv2.threshold(r, thresh, 255, cv2.THRESH_BINARY)

        note1Y = checkNote(thresh1, "Note1", 60)
        note2Y = checkNote(thresh1, "Note2", 65)
        note3Y = checkNote(thresh1, "Note3", 72)

        cv2.rectangle(thresh1, (0, note1Y), (width, note1Y + 50), (255), 2)
        cv2.rectangle(thresh1, (0, note2Y), (width, note2Y + 50), (255), 2)
        cv2.rectangle(thresh1, (0, note3Y), (width, note3Y + 50), (255), 2)

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
