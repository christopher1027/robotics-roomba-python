import os
import Robot
import SerialInterface
import math
import thread
import threading
import time
import PID

""" 
*************************************************************************************************
THIS IS THE BOILER PLATE

THIS PROGRAM IS THE MAIN PROGRAM THAT WILL BE EXECUTING COMMANDS TO MAKE THE ROBOT DO THINGS

*************************************************************************************************
"""  

def main():
    #this establishes a connection to the robot
    #names the robot r
    r = Robot.robot()
    #Initializes the Robot setting it to passive and safe mode
    r.start()
    #self.connection.close()
    print("robot started")
    time.sleep(2)
    #self.connection.open()
    #project three movement - using IR sensors and PID
    #using iterative method so a "while" runs for ever
    print("entering the loop")
    while True:
        print("In the loop")
        #if the clean button is pressed robot will turn off
        if (r.readButton() == 1):
            r.stop()
            pass
        elif (r.readButton() == 0):
            print("BUTTON NO PRESSED")
            print("readIRRight()")
            #LETS SEE IF IR SENSORS OUTPUT
            r.readIRRight()
            print("Following WALL")
            #NOW CALL THE WALL FOLLOWING FUNCTION
            r.followWall()
            #this is the iteration time
            time.sleep(1)
        time.sleep(1)
        pass
    '''
    decided to not use threads due to data feed back complications
    tBumper = threading.Thread(target = r.readBumper)
    tBumper.start()
    tButton = threading.Thread(target = r.readButton)
    tButton.start()
    '''
#Runs this deffinition called main
if __name__ == '__main__':
    main()