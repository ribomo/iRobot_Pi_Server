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



serial_port = '/dev/tty.usbserial-DA01NW1L'


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

        if c == '0':  # forward
            pass
        elif c == '1':  # forward
            velocity += VELOCITYCHANGE
        elif c == '2':  # back
            velocity -= VELOCITYCHANGE
        elif c == '3':  # left
            rotation += ROTATIONCHANGE
        elif c == '4':  # right
            rotation -= ROTATIONCHANGE
        elif c == 'p':  # Passive
            self.sendCommandASCII('128')
        elif c == 's':  # Safe
            self.sendCommandASCII('131')
        elif c == 'f':  # Full
            self.sendCommandASCII('132')
        elif c == 'c':  # Clean
            self.sendCommandASCII('135')
        elif c == 'd':  # Docmode
            self.sendCommandASCII('143')
        elif c == 'b':  # Beep
            self.sendCommandASCII('140 3 1 64 16 141 3')
            print(c)
        elif c == 'r':  # Reset
            self.sendCommandASCII('7')
        else:
            print(repr(c), "not handled")

        vr = velocity + (rotation / 2)
        vl = velocity - (rotation / 2)

        # create drive command
        cmd = struct.pack(">Bhh", 145, int(vr), int(vl))
        self.sendCommandRaw(cmd)

    def robotModeChange(self, mode):
        if mode == 'P':  # Passive
            self.sendCommandASCII('128')
        elif mode == 'S':  # Safe
            self.sendCommandASCII('131')
        elif mode == 'F':  # Full
            self.sendCommandASCII('132')
        elif mode == 'C':  # Clean
            self.sendCommandASCII('135')
        elif mode == 'D':  # Docmode
            self.sendCommandASCII('143')
        elif mode == 'SPACE':  # Beep
            self.sendCommandASCII('140 3 1 64 16 141 3')
        elif mode == 'R':  # Reset
            self.sendCommandASCII('7')
        else:
            print(repr(mode), "not handled")

    def robotMotionChange(self, d):
        velocity = 0
        rotation = 0
        if d == '1':  # forward
            velocity += VELOCITYCHANGE
        elif d == '2':  # back
            velocity -= VELOCITYCHANGE
        elif d == '3':  # left
            rotation += ROTATIONCHANGE
        elif d == '4':  # right
            rotation -= ROTATIONCHANGE
        # +forward -backward
        # +left -right

        # compute left and right wheel velocities
        vr = velocity + (rotation / 2)
        vl = velocity - (rotation / 2)

        # create drive command
        cmd = struct.pack(">Bhh", 145, int(vr), int(vl))
        self.sendCommandRaw(cmd)
        time.sleep(1)






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
    app.run(debug=True, host='0.0.0.0')

