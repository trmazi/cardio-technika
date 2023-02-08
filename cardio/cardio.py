import hid, sys
from cardio.data.constants import DataConstants

class CardIO:
    @classmethod
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

    @classmethod
    def pollCardIO(self, device: hid.Device) -> list:
        data = device.read(128, 200)
        if data == b'':
            return None
        else:
            card_id = data[1:]

            return str(card_id.hex()).upper()