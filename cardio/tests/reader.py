# Reader tests
import serial, time
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

        self.query_cnt = 0

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

        Workflow:
            - Game sends request
            - Reader says "i am ready"
            - Game sends "confirmed"
            - Reader sends response
        '''
        if com.in_waiting:
            s_data = com.read_all()
            time.sleep(.1)
            com.write(b'\x06')

            confirm = com.read_all()
            time.sleep(.1)
            if confirm == b'\x05':
                status, stype = DataConstants.processRequest(s_data)
                
                # Clean this up in the future.
                if stype == DataConstants.REQUEST_TYPE_STATIC:
                    if status == DataConstants.STATUS_FIND_CARD: # Really dumb way of slowing this down
                        self.query_cnt += 1
                    if self.query_cnt == 5:
                        status = DataConstants.STATUS_FIND_CARD_OK
                        self.query_cnt = 0

                    response = DataConstants.sendGeneric(status, stype)

                elif stype == DataConstants.REQUEST_TYPE_GENERATED:
                    if status == DataConstants.STATUS_GET_UID:
                        response = DataConstants.sendUID(status, [0x0F, 0x8F, 0x16, 0xB7])

                    elif status in [DataConstants.STATUS_GET_S0_B1, DataConstants.STATUS_GET_S0_B2]:
                        card = "DBFKXMQQHQHPSDFBYVXW"
                        response = DataConstants.sendCardID(status, bytes(card, 'ASCII'))
            
                time.sleep(.1)
                com.write(response + DataConstants.calcBCC(response))