
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