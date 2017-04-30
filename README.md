# README For Raspberry Pi Server
This README contains all the information you need to set up the video streaming server and the iRobot control server

## Dependency
- Python3
- Pyserial
- Flask

To install all of the dependency, enter following commend in terminal:
1. sudo apt-get install Python3
2. python3 install pyserial
3. python3 install flask

## Run
- Unzip the file into a destination of your choose
- To run both the video streaming server and the robot server you need to call the bash script provdied, simply run: sh openStream.sh it will start the video stream server and iRobot control server at the same time.

## Notice
- The Android device and the server need to be on the same Wi-Fi network, the port 80 and port 8090 need to be open to the network.
- Wi-Fi network needed to allow connection between devices
- This program may require root permission.

## Contact
Feel free to add new issues on github, and we will answer them ASAP.

## MIT License

Copyright © 2017 Guojie Wen, Jingyi Tang, Ribo Mo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
