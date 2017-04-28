from flask import Flask, render_template
import struct
import time
import threading

try:
    import serial
except ImportError:
    raise

app = Flask(__name__)

connection = None

VELOCITYCHANGE = 200
ROTATIONCHANGE = 300



serial_port = '/dev/ttyUSB0'


class direction():
    forward = False
    backward = False
    right = False
    left = False

class tetherDrive():
    callbackKeyUp = False
    callbackKeyDown = False
    callbackKeyLeft = False
    callbackKeyRight = False
    callbackKeyLastDriveCommand = ''

    def __init__(self):
        self.connection, self.port = self.onConnect()



    # sendCommandRaw takes a string interpreted as a byte array
    def sendCommandRaw(self, command):
        global connection

        try:
            if connection is not None:
                connection.write(command)
                print("drive")
            else:
                print("Not connected.")
        except serial.SerialException:
            self.connection = "Lost connection"
            print("Lost connection")
            connection = None

    # getDecodedBytes returns a n-byte value decoded using a format string.

    # Whether it blocks is based on how the connection was set up.
    def getDecodedBytes(self, n, fmt):
        global connection

        try:
            return struct.unpack(fmt, connection.read(n))[0]
        except serial.SerialException:
            self.connection = "Lost connection"
            print("Lost connection")
            connection = None
            return None
        except struct.error:
            print("Got unexpected data from serial port.")
            return None

    def sendCommandASCII(self, command):
        cmd = ""
        for v in command.split():
            cmd += chr(int(v))

        self.sendCommandRaw(cmd.encode())
        
        
    def robotChange(self, c):
        velocity = 0
        rotation = 0
        motion = False
        
        if c == '0':  # Stop
            motion = True
            print("Stop")
        elif c == 'Up':  # forward
            velocity += VELOCITYCHANGE
            motion = True
        elif c == 'Down':  # back
            velocity -= VELOCITYCHANGE
            motion = True
        elif c == 'Left':  # left
            rotation += ROTATIONCHANGE
            motion = True
        elif c == 'Right':  # right
            rotation -= ROTATIONCHANGE
            motion = True 
        elif c == 'Passive':  # Passive
            self.sendCommandASCII('128')
        elif c == 'Safe':  # Safe
            self.sendCommandASCII('131')
            print('safe')
        elif c == 'Full':  # Full
            self.sendCommandASCII('132')
        elif c == 'Clean':  # Clean
            self.sendCommandASCII('135')
        elif c == 'Docmod':  # Docmode
            self.sendCommandASCII('143')
        elif c == 'Beep':  # Beep
            self.sendCommandASCII('140 3 1 64 16 141 3')
            print(c)
        elif c == 'Reset':  # Reset
            self.sendCommandASCII('7')
        else:
            print(repr(c), "not handled")

        if motion:
            vr = velocity + (rotation / 2)
            vl = velocity - (rotation / 2)

            # create drive command
            cmd = struct.pack(">Bhh", 145, int(vr), int(vl))
            self.sendCommandRaw(cmd)


    def onConnect(self):
        global connection

        port = serial_port

        if port is not None:
            print("Trying " + str(port) + "... ")
            try:
                connection = serial.Serial(port, baudrate=115200, timeout=1)
                print("Connected!")
                return 0, port
            except:
                return 1, "No connection"


@app.route('/<cmd>')
def getCommand(cmd):
    runRobot.robotChange(cmd)
    return "Success"


@app.route('/')
def index():
    return render_template('index.html', header="CNIT425 Final Project", status=runRobot.connection,
                           port=runRobot.port)


if __name__ == '__main__':
    runRobot = tetherDrive()
    print("Robot Thread Started...")
    app.run(debug=False, host='0.0.0.0', threaded=True)

