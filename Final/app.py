from flask import Flask, render_template
import struct
import time
import sys, glob  # for listing serial ports

try:
    import serial
except ImportError:
    raise

app = Flask(__name__)

connection = None

VELOCITYCHANGE = 200
ROTATIONCHANGE = 300

serial_port = '/dev/tty.usbserial-DA01NW1L'


class tetherDrive():
    def __init__(self):
        self.header = 'LET DRIVE'
        self.connection, self.port = self.onConnect()
        self.moveForward()


    # sendCommandRaw takes a string interpreted as a byte array
    def sendCommandRaw(self, command):
        global connection

        try:
            if connection is not None:
                connection.write(command)
            else:
                print("Not connected.")
        except serial.SerialException:
            print("Lost connection")
            connection = None

    # getDecodedBytes returns a n-byte value decoded using a format string.

    # Whether it blocks is based on how the connection was set up.
    def getDecodedBytes(self, n, fmt):
        global connection

        try:
            return struct.unpack(fmt, connection.read(n))[0]
        except serial.SerialException:
            print("Lost connection")
            connection = None
            return None
        except struct.error:
            print("Got unexpected data from serial port.")
            return None

    def sendCommandASCII(self, command):
        cmd = ""
        for v in command.split():
            cmd += v.encode()

        self.sendCommandRaw(cmd)

    def moveForward(self):
        self.sendCommandASCII('131')


    def onConnect(self):
        global connection

        port = serial_port

        if port is not None:
            print("Trying " + str(port) + "... ")
            try:
                connection = serial.Serial(port, baudrate=115200, timeout=1)
                return 0, port
            except:
                return 1


@app.route('/')
def index():
    app = tetherDrive()
    return render_template('index.html', header=app.header, status=app.connection,
                           port=app.port)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
