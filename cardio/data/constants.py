from typing import Tuple
class DataConstants:
    '''
    All core stuff for data handling
    '''
    CARDIO_VID = 7375
    CARDIO_PID = 21074
    CARDIO_SN = 'CARDIOP1'

    @classmethod
    def get_card_type(self, type: bytes) -> str:
        return {
            b'\x01': 'NFC',
            b'\x02': 'FelICa',
            b'\x03': 'MiFare Classic'
        }[type]

    CARD_UID = [0x00]*4
    CARD_DATA = [0x00]*16

    REQUEST_AUTH_KEY = b'\x02\x00\x09\x35\x32\x00\x37\x21\x53\x6a\x72\x40\x03\x12' # (key = 37 21 53 6a 72 40)
    REQUEST_AUTH_CYCLON = b'\x02\x00\t52\x00retsam\x03\x13' # (key = 114, 101, 116, 115, 97, 109, 0)
    REQUEST_CARD_INSERTED = b'\x02\x00\x02\x31\x30\x03\x02'
    REQUEST_FIND_CARD = b'\x02\x00\x02\x35\x30\x03\x06'
    REQUEST_EJECT_CARD = b'\x02\x00\x02\x32\x30\x03\x01'
    REQUEST_CARD_UID = b'\x02\x00\x02\x35\x31\x03\x07'
    REQUEST_CARD_S0_B1 = b'\x02\x00\x04\x35\x33\x00\x01\x03\x02'
    REQUEST_CARD_S0_B2 = b'\x02\x00\x04\x35\x33\x00\x02\x03\x01'

    RESPONSE_AUTH_KEY = b'\x02\x00\x04\x35\x32\x00\x59\x03'
    RESPONSE_CARD_INSERTED_FALSE = b'\x02\x00\x03\x31\x30\x4e\x03'
    RESPONSE_CARD_INSERTED_TRUE = b'\x02\x00\x03\x35\x30\x59\x03'
    RESPONSE_CARD_EJECT = b'\x02\x00\x03\x32\x30\x59\x03'
    RESPONSE_UID_HEADER = b'\x02\x00\x07\x35\x31\x59'
    RESPONSE_CARD_S0_B1_HEADER = b'\x02\x00\x15\x35\x33\x00\x01\x59'
    RESPONSE_CARD_S0_B2_HEADER = b'\x02\x00\x15\x35\x33\x00\x02\x59'
    RESPONSE_TAIL = b'\x03'

    REQUEST_TYPE_STATIC = 0
    REQUEST_TYPE_GENERATED = 1

    STATUS_AUTH_KEY = 1
    STATUS_CARD_INSERTED = 2
    STATUS_FIND_CARD = 3
    STATUS_FIND_CARD_OK = 8
    STATUS_EJECT_CARD = 4
    STATUS_GET_UID = 5
    STATUS_GET_S0_B1 = 6
    STATUS_GET_S0_B2 = 7

    STATUS_STR = {
        STATUS_AUTH_KEY: 'AUTH_KEY',
        STATUS_CARD_INSERTED: 'IS_CARD_INSERTED?',
        STATUS_FIND_CARD: 'FIND_CARD',
        STATUS_EJECT_CARD: 'EJECT_CARD',
        STATUS_GET_UID: 'GET_UID',
        STATUS_GET_S0_B1: 'GET_CARD_SECTOR_0_BLOCK_1',
        STATUS_GET_S0_B2: 'GET_CARD_SECTOR_0_BLOCK_2',
    }

    @classmethod
    def processRequest(self, requested_data: bytes) -> Tuple[int, int]:
        '''
        Given a request in binary, return a tuple stating what the game wants, and the type of said response.
        '''
        status = {
            self.REQUEST_AUTH_KEY: self.STATUS_AUTH_KEY,
            self.REQUEST_AUTH_CYCLON: self.STATUS_AUTH_KEY,
            self.REQUEST_CARD_INSERTED: self.STATUS_CARD_INSERTED,
            self.REQUEST_FIND_CARD: self.STATUS_FIND_CARD,
            self.REQUEST_EJECT_CARD: self.STATUS_EJECT_CARD,
            self.REQUEST_CARD_UID: self.STATUS_GET_UID,
            self.REQUEST_CARD_S0_B1: self.STATUS_GET_S0_B1,
            self.REQUEST_CARD_S0_B2: self.STATUS_GET_S0_B2
        }[requested_data]

        d_type = {
            self.REQUEST_AUTH_KEY: self.REQUEST_TYPE_STATIC,
            self.REQUEST_AUTH_CYCLON: self.REQUEST_TYPE_STATIC,
            self.REQUEST_CARD_INSERTED: self.REQUEST_TYPE_STATIC,
            self.REQUEST_FIND_CARD: self.REQUEST_TYPE_STATIC,
            self.REQUEST_EJECT_CARD: self.REQUEST_TYPE_STATIC,
            self.REQUEST_CARD_UID: self.REQUEST_TYPE_GENERATED,
            self.REQUEST_CARD_S0_B1: self.REQUEST_TYPE_GENERATED,
            self.REQUEST_CARD_S0_B2: self.REQUEST_TYPE_GENERATED
        }[requested_data]

        print(f'Game sent request: {self.STATUS_STR[status]}')

        return (status, d_type)

    @classmethod
    def sendGeneric(self, request_status: int, reqest_type: int) -> bytes:
        '''
        For sending responses that are GENERIC.
        For generated responses, please use their dedicated function.
        Given a request status and type, process it and return the expected response.
        '''
        if reqest_type != self.REQUEST_TYPE_STATIC:
            return None

        data = {
            self.STATUS_AUTH_KEY: self.RESPONSE_AUTH_KEY,
            self.STATUS_CARD_INSERTED: self.RESPONSE_CARD_INSERTED_FALSE,
            self.STATUS_FIND_CARD: self.RESPONSE_CARD_INSERTED_FALSE,
            self.STATUS_FIND_CARD_OK: self.RESPONSE_CARD_INSERTED_TRUE,
            self.STATUS_EJECT_CARD: self.RESPONSE_CARD_EJECT
        }[request_status]
        print(f'Responding with: {str(data)}')

        return data

    @classmethod
    def sendUID(self, request_status: int, card_uid: list[int]) -> bytes:
        '''
        Given the status and pulled card UID, return bytes of what game wants.
        '''
        if request_status != self.STATUS_GET_UID:
            return None

        if len(card_uid) != len(self.CARD_UID):
            return None

        data = b''
        data += self.RESPONSE_UID_HEADER
        data += bytes(card_uid)
        data += self.RESPONSE_TAIL
        print(f'Responding with: {str(data)}')

        return data

    @classmethod
    def sendCardID(self, request_status: int, card_id: list[int]) -> bytes:
        '''
        Given the request status and pulled card ID, decide which part
        of the card ID the game wants, return said part.
        '''
        header = None
        if request_status == self.STATUS_GET_S0_B1:
            header = self.RESPONSE_CARD_S0_B1_HEADER
            card_part = bytes(card_id[:16])
        elif request_status == self.STATUS_GET_S0_B2:
            header = self.RESPONSE_CARD_S0_B2_HEADER
            card_part = bytes(card_id[16:20]) + (b'\x00'*12)
        else:
            return None

        if len(card_part) != len(self.CARD_DATA):
            return None

        data = b''
        data += header
        data += card_part
        data += self.RESPONSE_TAIL
        print(f'Responding with: {str(data)}')
        
        return data

    @classmethod
    def calcBCC(self, data: bytes):
        bcc = 0
        for byte in data:
            bcc ^= byte
        return bytes([bcc])