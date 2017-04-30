cd iRobot_Pi_Server/Final
sudo python3 app.py & sudo raspivid -o - -t 0 -hf -w 480 -h 270 -fps 24| cvlc -q stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' :demux=h264
