#!venv/bin/python3
import threading
import cv2
import rtmidi

client = None
lastNote = None
note1On = False
width = 500
midiout = None

imageWidth = 1280
imageHeight = 1024
sampleRegion = 50

noteOnFlags = {
    "Note1": False,
    "Note2": False,
    "Note3": False
}


def nothing(x):
    pass


def init_midi():
    global midiout
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    print("Available ports: " + str(available_ports))

    if available_ports:
        midiout.open_port(0)
        print("Opened MIDI port " + str(available_ports))
    else:
        midiout.open_virtual_port("My virtual output")


def createRegionControls(note, x, y):
    cv2.createTrackbar(note + "Y", "Laser", 0, imageHeight, nothing)
    cv2.setTrackbarPos(note + "Y", "Laser", x)
    cv2.createTrackbar(note + "X", "Laser", 0, imageWidth, nothing)
    cv2.setTrackbarPos(note + "X", "Laser", y)


def init():
    cv2.namedWindow('Laser')
    cv2.createTrackbar("Threshold", "Laser", 0, 255, nothing)
    cv2.setTrackbarPos("Threshold", "Laser", 211)

    createRegionControls("Note1", 311, 651)
    createRegionControls("Note2", 381, 569)
    createRegionControls("Note3", 485, 621)


def noteOn(note):
    global midiout
    note_on = [0x90, int(note), 112]
    midiout.send_message(note_on)


def noteOff(note):
    global midiout
    note_off = [0x80, int(note), 0]
    midiout.send_message(note_off)


def checkNote(thresh, slider, note):
    noteY = cv2.getTrackbarPos(slider + "Y", "Laser")
    noteX = cv2.getTrackbarPos(slider + "X", "Laser")

    noteCrop = thresh[noteY:noteY + sampleRegion, noteX:noteX + sampleRegion]
    noteSum = cv2.countNonZero(noteCrop)

    if noteOnFlags[slider] == False:
        if noteSum < 100:
            print("Playing note: " + str(note) + "sum: " + str(noteSum))
            noteOnFlags[slider] = True
            noteOn(note)

    if noteSum > 100:
        # print("Stopping note: " + str(note) + "sum: " + str(noteSum))
        noteOnFlags[slider] = False
        noteOff(note)

    return noteX, noteY


def show_webcam():
    global client
    global lastNote
    global note1On

    cam = cv2.VideoCapture(0)
    cam.set(3, imageWidth)
    cam.set(4, imageHeight)

    while True:
        ret_val, img = cam.read()

        b, g, r = cv2.split(img)

        thresh = cv2.getTrackbarPos("Threshold", "Laser")
        ret, thresh1 = cv2.threshold(r, thresh, 255, cv2.THRESH_BINARY)

        note1X, note1Y = checkNote(thresh1, "Note1", 60)
        note2X, note2Y = checkNote(thresh1, "Note2", 65)
        note3X, note3Y = checkNote(thresh1, "Note3", 72)

        cv2.rectangle(thresh1, (note1X, note1Y), (note1X + sampleRegion, note1Y + sampleRegion), (255), 1)
        cv2.rectangle(thresh1, (note2X, note2Y), (note2X + sampleRegion, note2Y + sampleRegion), (255), 1)
        cv2.rectangle(thresh1, (note3X, note3Y), (note3X + sampleRegion, note3Y + sampleRegion), (255), 1)

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
    init_midi()
    show_webcam()
    del midiout
