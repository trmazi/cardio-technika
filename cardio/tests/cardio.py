import hid, sys
from cardio.data.constants import DataConstants

class CardIOTest:

    def loadCardIO(self):
        devices = hid.enumerate(DataConstants.CARDIO_VID, DataConstants.CARDIO_PID)
        if len(devices) == 0:
            print('Unable to find any CardIO Readers!\nPlease make sure to plug in a CardIO device.')
            sys.exit()

        print(f'Found {len(devices)} CardIO device(s)!')

        for device in devices:
            if device['serial_number'] != DataConstants.CARDIO_SN:
                print(f'This CardIO device is not Player 1!n\Refusing to connect!')
                sys.exit()
            
            device = hid.Device(DataConstants.CARDIO_VID, DataConstants.CARDIO_PID, DataConstants.CARDIO_SN, device['path'])

if __name__ == '__main__':
    cardio_test = CardIOTest()

    CardIOTest.loadCardIO(cardio_test)