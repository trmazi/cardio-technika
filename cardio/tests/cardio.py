import hid, sys
from cardio.data.constants import DataConstants

class CardIOTest:

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

    def pollCardIO(self, device: hid.Device):
        data = device.read(128, 200)
        if data == b'':
            return None
        else:
            card_type = data[:1]

            card_id = data[1:]
            if card_id[-4:] == b'\x00\x00\x00\x00':
                card_id = card_id[:4]
                card_type = b'\x03'
            card_id = str(card_id.hex()).upper()
            
            print(f'\nYour card information:\nType: {DataConstants.get_card_type(card_type)}\nCardID: {card_id}')

if __name__ == '__main__':
    cardio_test = CardIOTest()
    device = cardio_test.loadCardIO()

    print('\n\nReader was set up properly!')
    print('Tap a card now to read the ID.')
    while True:
        try:
            cardio_test.pollCardIO(device)
        except KeyboardInterrupt:
            print('goodbye!')
            sys.exit()