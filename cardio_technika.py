# CardIO Technika
# A DJMAX Technika / Beatcraft Cyclon card reader emulator
# For hooking with CardIO.
import serial, sys, hid, time, argparse
from cardio.data.constants import DataConstants

class CardIOTechnika:
    def __init__(self, serial_port: str, serial_baud: int) -> None:
        self.port = serial_port
        self.baud = serial_baud

        self.card_UID = [0x00] * 4
        self.card_ID = [0x00] * 20
        self.auth_bad = False
        self.eject_tries = 0 # Max of 4 eject tries before we agree to eject when auth is bad.

        self.reading_cards = False

    def loadCardIO(self):
        devices = hid.enumerate(DataConstants.CARDIO_VID, DataConstants.CARDIO_PID)
        if len(devices) == 0:
            print('Unable to find any CardIO Readers!\nPlease make sure to plug in a CardIO device.')
            sys.exit()

        print(f'Found {len(devices)} CardIO device(s)!\nNote that ONLY the FIRST CardIO will be used!')

        for device in devices:
            if device['serial_number'] != DataConstants.CARDIO_SN:
                print(f'This CardIO device is not Player 1!n\Refusing to connect!')
                sys.exit()

            if device['path'].decode('utf-8')[-3:] == 'KBD':
                continue
            
            device = hid.Device(DataConstants.CARDIO_VID, DataConstants.CARDIO_PID, DataConstants.CARDIO_SN, device['path'])
            print(f'\nCardIO Information:\nSerial: {device.serial}\nProduct: {device.product}\nManufacturer: {device.manufacturer}')

            return device

    def pollCardIO(self, device: hid.Device) -> list:
        data = device.read(128, 200)
        if data == b'':
            return None
        else:
            card_id = data[1:]

            return str(card_id.hex()).upper()

    def openSerial(self) -> serial.Serial:
        '''
        Opens the serial port.
        '''
        com = serial.Serial(self.port, self.baud)
        com.flushInput()
        com.flushOutput()
        return com

    def readSerial(self, com: serial.Serial, cardio: hid.Device) -> None:
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
                
                # Here's where we start polling the CardIO.
                if stype == DataConstants.REQUEST_TYPE_STATIC:
                    if status == DataConstants.STATUS_AUTH_KEY:
                        if self.card_ID[-12:] == b'000000000000':
                            status = DataConstants.STATUS_AUTH_KEY_BAD
                            self.card_ID = [0x00] * 20
                            self.card_UID = [0x00] * 4
                            self.auth_bad = True

                    elif status == DataConstants.STATUS_FIND_CARD:
                        cardid = self.pollCardIO(cardio)
                        if cardid != None:
                            cardid = bytes(cardid, 'ascii')

                            while len(cardid) < 20:
                                cardid += b'0'
                            self.card_ID = cardid
                            self.card_UID = cardid[:4]
                            self.auth_bad = False
                            self.eject_tries = 0

                            status = DataConstants.STATUS_FIND_CARD_OK

                    elif status == DataConstants.STATUS_EJECT_CARD:
                        if self.auth_bad and self.eject_tries <= 4:
                            status = DataConstants.STATUS_EJECT_CARD_NO
                            self.eject_tries += 1

                    response = DataConstants.sendGeneric(status, stype)

                elif stype == DataConstants.REQUEST_TYPE_GENERATED:
                    if status == DataConstants.STATUS_GET_UID:
                        response = DataConstants.sendUID(status, self.card_UID)

                    elif status in [DataConstants.STATUS_GET_S0_B1, DataConstants.STATUS_GET_S0_B2]:
                        response = DataConstants.sendCardID(status, self.card_ID)
            
                time.sleep(.1)
                com.write(response + DataConstants.calcBCC(response))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--com_port', type=str, default="COM9")
    parser.add_argument('--baud_rate', type=int, default=9600)
    args = parser.parse_args()

    main_class = CardIOTechnika(args.com_port, args.baud_rate)
    
    com = main_class.openSerial()
    cardio = main_class.loadCardIO()

    print('\nWelcome to CardIO Technika!\nThis software will let you use a CardIO Reader on DJMax Technika and Beatcraft Cyclon.')
    print('Please connect a game to get started.\n')

    while True:
        try:
            main_class.readSerial(com, cardio)
        except KeyboardInterrupt:
            print('goodbye!')
            sys.exit()