import serial

"""
*************************************************************************************************
THIS IS THE BOILER PLATE

THIS CLASS CONTAINS THE FUNCTIONS REQUIRED TO ESTABLISH A CONNECTION TO A ROBOT
 - usefull incase multiple robots wish to be established

*************************************************************************************************
""" 
class face:
    connection = None
    def __init__(self):
        self.connect()
    def write(self,cmd):
        self.connection.write(cmd)
    def connect(self):
        self.connection = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
    def closeConnection(self):
        self.connection.close()
    def read(self,cmd):
        data = self.connection.read(cmd)
        return data