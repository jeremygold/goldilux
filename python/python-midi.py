#!/usr/bin/env python3

import time
import rtmidi
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.

midiout = None


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("note-on")
    client.subscribe("note-off")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    global midiout
    print(msg.topic + ": " + str(msg.payload))

    if(msg.topic == "note-on"):
        note_on = [0x90, int(msg.payload), 112]
        midiout.send_message(note_on)

    if(msg.topic == "note-off"):
        note_off = [0x80, int(msg.payload), 0]
        midiout.send_message(note_off)


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


def init_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.1.105", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()


init_midi()
init_mqtt()

del midiout
