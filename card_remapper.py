# Card remapping tool
import sys, hid, argparse
from cardio.cardio import CardIO
from cardio.remapper import CardRemapper

class RemapperTool:
    '''
    Tool to remap physical cards to virtual ones. 
    Good for non-original cards or networks that only support one card.
    '''
    def __init__(self, card_path: str, cardio: hid.Device) -> None:
        self.remapper = CardRemapper(card_path)
        self.cardio = cardio

    def readCard(self) -> None:
        p_card = CardIO.pollCardIO(self.cardio)
        if p_card != None:
            p_card = bytes(p_card, 'ascii')
            s_card = p_card.decode('ascii')
            print(f'Found physical card: {s_card}!')

            def get_virt():
                return input('Please enter the ID of the card you\'d like to remap: ')
            
            virt = get_virt()
            while len(virt) != 20:
                print(f'The ID needs to be 20 characters long! You gave {len(virt)} character(s)')
                virt = get_virt()
            virt = virt.encode('ascii')

            self.remapper.addMapping(p_card, virt)
            self.remapper.saveCards()
            print('Saved! Please tap another card, or press CTRL+C to exit.\n')

        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--card_file', type=str, default="./cards.json")
    args = parser.parse_args()
    
    cardio = CardIO.loadCardIO()
    main_class = RemapperTool(args.card_file, cardio)

    print('Welcome to CardIO Technika remapper tool!')
    print('Please tap a card to get started! Press CTRL+C to save and exit.\n')

    while True:
        try:
            main_class.readCard()
        except KeyboardInterrupt:
            print('goodbye!')
            sys.exit()