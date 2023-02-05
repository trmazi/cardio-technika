# Reader tests
import serial
from cardio.data.constants import DataConstants

class ReaderTest:
    '''
    Testing suite that talks to the game on a COM port.

    Tests these functions:
        - Responds to game
        - Sends security code
        - Ejects card
        - Inserts card
        - Sends UID
        - Sends both data chunks
    '''

    def __init__(self, COMPORT: str, baud: int) -> None:
        self.port = COMPORT
        self.baud = baud

    def openSerial(self) -> serial.Serial:
        '''
        Opens the serial port.
        '''
        com = serial.Serial(self.port, self.baud)
        com.flushInput()
        com.flushOutput()
        return com

    def readSerial(self, com: serial.Serial) -> None:
        '''
        Reads data from the serial port, decides what to do with said data.
        Given the opened serial port.
        '''
        s_data = com.read(128)

        if s_data != b'':
            status, stype = DataConstants.processRequest(s_data)
            
            # Clean this up in the future.
            if stype == DataConstants.REQUEST_TYPE_STATIC:
                DataConstants.sendGeneric(status, stype)

            elif stype == DataConstants.REQUEST_TYPE_GENERATED:
                if status == DataConstants.STATUS_GET_UID:
                    DataConstants.sendUID(status, hex(0000))

                elif status in [DataConstants.STATUS_GET_S0_B1, DataConstants.STATUS_GET_S0_B2]:
                    DataConstants.sendCardID(status, hex(0000))
