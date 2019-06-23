# robotics-roomba-python
Programmed an iRobot Roomba in python using a raspberry pi

Integrated a raspberry pi with an iRobot Roomba so that I could push custom Python code to a roomba.

Roomba API referenced:
https://www.irobotweb.com/~/media/MainSite/PDFs/About/STEM/Create/iRobot_Roomba_600_Open_Interface_Spec.pdf

Main areas of focus include: 
-Reading in Sensor data from the roomba such as its Bumpers, Wheel Drops, Buttons, and IR Sensors.
-Referencing Sensor data and sending commands to the roomba to do different actions such as Moving, avoiding obstacles, and following walls
-Implementing a PID Controller(control loop feedback mechanism)to correct the roombas trajectory during its movements
-Bonus was getting the roomba to play a song by referencing the Roomba's note frequencies

Included are four files: Move.py, Robot.py, SerialInterface.py, PID.py.
Move.py - this file is the main program that will be executing commands to make the roomba do things
Robot.py - this file is the interface for communicating with the roomba, it contains all of the functions required to run
SerialInterface.py - contains the functions required to establish a connection to the Roomba.
PID.py - this file contains code that creates a PID Controller

