import SerialInterface
import struct
import time
import PID

"""
*************************************************************************************************
THIS IS THE BOILER PLATE

THIS PROGRAM IS THE INTERFACE FOR COMMUNICATING WITH THE ROBOT, IT CONTAINS ALL OF THE FUNCTIONS 
REQUIRED TO RUN (Specific to a robot)

*************************************************************************************************
"""  
# some module-level definitions for the robot commands
START = chr(128)    # already converted to bytes...
BAUD = chr(129)     # + 1 byte
CONTROL = chr(130)  # deprecated for Create
SAFE = chr(131)
FULL = chr(132)
POWER = chr(133)
SPOT = chr(134)     # Same for the Roomba and Create
CLEAN = chr(135)    # Clean button - Roomba
COVER = chr(135)    # Cover demo - Create
MAX = chr(136)      # Roomba
DEMO = chr(136)     # Create
DRIVE = chr(137)    # + 4 bytes
MOTORS = chr(138)   # + 1 byte
LEDS = chr(139)     # + 3 bytes
SONG = chr(140)     # + 2N+2 bytes, where N is the number of notes
PLAY = chr(141)     # + 1 byte
SENSORS = chr(142)  # + 1 byte
FORCESEEKINGDOCK = chr(143)  # same on Roomba and Create
# the above command is called "Cover and Dock" on the Create
DRIVEDIRECT = chr(145)       # Create only
STREAM = chr(148)       # Create only
QUERYLIST = chr(149)       # Create only
PAUSERESUME = chr(150)       # Create only

#sensors
BUMPSANDWHEELDROPS = chr(7)
CLIFFLEFT = chr(9)
CLIFFFRONTLEFT = chr(10)
CLIFFFRONTRIGHT = chr(11)
CLIFFRIGHT = chr(12)
VIRTUALWALL = chr(13)
BUTTONS = chr(18)
DISTANCE = chr(19)
ANGLE = chr(20)
VELOCITY = chr(39)

#INFARED
IRpower = chr(138)
IRleft = chr(129)
IRright = chr(131)
IRforward = chr(130)
IRstop = chr(137)

#PREDEFINED 
STRAIGHT = 0x8000
CLOCKWISE = 0xFFFF
CCLOCKWISE = 0x0001

#*************************************************************************************************
#ROBOT FUNCTIONS
#*************************************************************************************************

class robot:
    connect = None
    def __init__(self):
        #This is where you would start the Robot
        self.connect = SerialInterface.face()
        self.start()
        #this sets all sensor data to 0
        '''
        self.leftWheelDrop = 0
        self.rightWheelDrop = 0
        self.leftBump = 0
        self.rightBump = 0
        self.wallSensor = 0
        self.leftCliff = 0
        self.frontLeftCliff = 0
        self.frontRightCliff = 0
        self.rightCliff = 0
        self.virtualWall = 0
        '''
    def drive(self,velocity,radius):
        print("Drive started\n")
        print(velocity, radius)
        # send the two values to be broken apart into their high/low components
        velHighVal, velLowVal = _toTwosComplement2Bytes(velocity)
        radiusHighVal, radiusLowVal = _toTwosComplement2Bytes(radius)
        # Writes the correct Opcode, and then pushes the two components of each number to the robot
        # (velocity,Radius)
        cmd = struct.pack( "cBBBB", DRIVE, velHighVal, velLowVal, radiusHighVal, radiusLowVal)
        self.connect.write(cmd)

    def driveDirect(self,velocityLeft,velocityRight):
        print("Drive Direct started\n")
        print(velocityLeft, velocityRight)
        # send the two velocity values to be broken apart into their high/low components
        leftHiVal, leftLowVal = _toTwosComplement2Bytes(velocityLeft)
        rightHiVal, rightLowVal = _toTwosComplement2Bytes(velocityRight)
        # Writes the correct Opcode, and then pushes the two components of each number to the robot
        cmd = struct.pack( "cBBBB", DIRECTDRIVE, rightHiVal, rightLowVal, leftHiVal, leftLowVal)
        self.connect.write(cmd)

    def playSong(self):
        self.connect.write(PLAY + 1)

    def setSong(self):
        song = struct.pack( "BBBBBBBBBBBBB", SONG, 1, 5, 43, 32, 41, 32, 40, 32, 38, 32, 36, 32)
        self.connect.write(song)
        print("setSong()" + song)

    def Off(self):
        #173 turns the robot off and changes that state to off
        self.connect.write(STOP)

    def resetRobot(self):
        self.connect.write(BUMPSANDWHEELDROPS)

    def FULL(self):
        #132 turns robot on and changes to FULL mode.  Executes commands regardless of wheel drop or not.
        self.connect.write(FULL)

    def start(self):
        #128 is the start command written to the robot and automatically
        #changes the state to passive
        self.connect.write(START)
        #changes the state to safe
        self.connect.write(SAFE)



#BUMPER ACTIONS
#*************************************************************************************************
    #no duplicate code
    #can assume PID iterates once per second (main move program)
    def followWall(self): #Using right wall in demonstraition 
        print("Begining to follow a Wall\n")
        #uses PID and set distance value (two inches) to follow wall
        #best values .09, .0026, .003
        control = PID.__init__(200, 0.015, 0.004, 0.003, 0.003)
        control.update(self.readIRRight)
        #PRINT OUT THE CONTROLLER VALUES
        '''
        if > xxx
            go right
            control.update(self.readIRRight)
        if < xxx 
            go left
            control.update(self.readIRRight)
        if = xxx
            go straight
            control.update(self.readIRRight)
        '''

            
    def bothBumperAction(self):
        print("Both Bumpers Action()\n")
        move = random.randint(1, 2)
        if(move == 1):
            self.drive(75,CLOCKWISE) #90 degrees the right
            time.sleep(2)
        if(move == 0):
            self.drive(75,CCLOCKWISE) #90 degrees the right
            time.sleep(2)

    def leftBumperAction(self):
        print("left Bumper Action()\n")
        self.drive(75,CLOCKWISE) #90 degrees the right
        time.sleep(2)

    def rightBumperAction(self): 
        print("right Bumper Action()\n")
        self.drive(75,CCLOCKWISE) #90 degrees the right
        time.sleep(2)

#END BUMPER ACTIONS
#*************************************************************************************************


#Sensor Reading functions
#*************************************************************************************************    
    #WALL FOLLOWING FUNCTIONS
    def readWall():
        print("readWall() started\n")
        #51 is the right wall bumper
        self.connect.write(SENSORS + chr(51))
        msg = self.connect.read(1)
        byte = struct.unpack(msg)
        print(byte)
        return(byte)

    #Read State of Buttons 
    #Returns either 1 or 0   
    def readButton(self):
        print("readButton() started\n")
        self.connect.write(SENSORS + BUTTONS)
        msg = self.connect.read(1)
        time.sleep(.05)
        byte = self.unpack(msg)
        cleanButton = bool(byte & 0x01)
        time.sleep(1)
        #RETURN STATE OF BUTTONS TO BE USED IN Move.py
        return(cleanButton)

    #this method reads and returns the IR values
    def readIRLeft(self):
        print("readIRLeft() started\n")
        #turns on IR
        self.connect.write(SENSORS + IRpower)
        time.sleep(.05)
        #Requests left IR data
        self.connect.write(SENSORS + IRleft)
        time.sleep(.05)
        #Reads left IR data
        IRdata = self.connect.read(1)
        time.sleep(.05)
        #based on bit or byte return parse acordingly
        return(IRdata)

    #this method reads and returns the IR values
    #supposed to be an unsigned int
    def readIRRight(self):
        print("readIRRight() started\n")
        #turns on IR
        self.connect.write(SENSORS + IRpower)
        time.sleep(.05)
        #Requests right IR data
        self.connect.write(SENSORS + IRright)
        time.sleep(.05)
        #Reads left IR data
        IRdata = self.connect.read(1)
        time.sleep(.05)
        unpackedIRdata = struct.unpack(IRdata)
        print(unpackedIRdata)
        #based on bit or byte return parse acordingly
        return(unpackedIRdata)
    
    #Read State of Bumpers
    def readBumper(self):
        print("readBumper() started\n")
        self.connect.write(SENSORS + BUMPSANDWHEELDROPS)
        msg = self.connect.read(1)
        byte = self.unpack(msg)
        print("msg\n")
        print(byte)
        leftWheelDrop = bool(byte & 0x08)
        rightWheelDrop = bool(byte & 0x04)#self._bitOfByte(2,byte)
        leftBump = bool(byte & 0x02)#self._bitOfByte(1,byte)
        rightBump = bool(byte & 0x01)#self._bitOfByte(0,byte)
        #If any WheelDrop or Bumper is activated sets value to 1
        bumpWheelSensors = leftWheelDrop or rightWheelDrop or leftBump or rightBump 
        return bumpWheelSensors

    def readCliff(self):
        #Reading of all Cliff packets
        print("readCliff() started\n")
        while True:
            self.connect.write(SENSORS + CLIFFLEFT + CLIFFFRONTLEFT + CLIFFFRONTRIGHT + CLIFFRIGHT + VIRTUALWALL)
            cliffSensors = (self.connect.read(5))
            print("cliffSensors: " + cliffSensors)
        return(cliffSensors)

    def readAngleDistance(self):
        #Reading of the Angle and Distance
        print("readAngleDistance() started\n")
        while True:
            self.connect.write(SENSORS + ANGLE)
            angle = self.connect.read(1)
            print("Angle: " + angle)

            self.connect.write(SENSORS + DISTANCE)
            distance = self.connect.read(1)
            print("Distance: " + distance)

    def unpack(self, packet):
        #unpacks a struct and returns the bit in the packet
        print(packet)
        return struct.unpack('b', packet)[0]

    def _bitOfByte( bit, byte ):
        """ returns a 0 or 1: the value of the 'bit' of 'byte' """
        if bit < 0 or bit > 7:
            print 'Your bit of', bit, ' is out of range (0-7)'
            print 'returning 0'
            return 0
        return ((byte >> bit) & 0x01)

    def _bytesOfR( r ):
        """ for looking at the raw bytes of a sensor reply, r """
        print 'raw r is', r
        for i in range(len(r)):
            print 'byte', i, 'is', ord(r[i])
        print 'finished with formatR'

    def _toTwosComplement2Bytes( value ):
        # if positive or zero, it's OK
        if value >= 0:
            eqBitVal = value
        # if it's negative, I think it is this
        else:
            eqBitVal = (1<<16) + value
        return ( (eqBitVal >> 8) & 0xFF, eqBitVal & 0xFF )
#END Sensor Reading functions
#************************************************************************************************