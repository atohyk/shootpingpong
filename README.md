# shootpingpong
simple arduino sketch and python opencv to obtain the location of a blob in a web cam video and shoot a ping pong at it

## Prerequisites 
+ Python 3
+ Python OpenCV wrapper (and OpenCV) installed
+ Arduino IDE
+ An Arduino

## Instructions
+ Flash Arduino code
+ Connect pitch servo to pin 9
+ Connect yaw servo to pin 10
+ Trigger comes from pin 3
+ Edit python script to point to the com port Arduino is connected to
+ If no built in webcam, connect a webcam and edit python script to point OpenCV to the webcam
+ Run python script
+ Press "q" to exit
