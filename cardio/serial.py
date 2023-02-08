import serial

class Serial:
    @classmethod
    def openSerial(self, port: str, baud: int) -> serial.Serial:
        '''
        Opens the serial port.
        '''
        com = serial.Serial(port, baud)
        com.flushInput()
        com.flushOutput()
        return com