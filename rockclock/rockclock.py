#!/usr/bin/python3

import signal
import queue
from .transmitter import Transmitter
from .receiver import Receiver
from .rockblock import RockBlock

import serial


_queue = None
transmitter = None
receiver = None


def term_handler(signum, frame):
    global transmitter
    transmitter.stop()


def main():
    global transmitter

    _queue = queue.Queue()

    clock_conn = serial.Serial("/dev/ttyUSB0", 9600, timeout=2)
    print("Clock connection acquired on /dev/ttyUSB0")
    rb = RockBlock("/dev/ttyAMA0")

    transmitter = Transmitter(rb, _queue)
    receiver = Receiver(clock_conn, _queue)

    receiver.start()
    transmitter.start()

    signal.signal(signal.SIGTERM, term_handler)

    # Wait until transmitter terminates then kill receiver
    transmitter.join()
    receiver.stop()
