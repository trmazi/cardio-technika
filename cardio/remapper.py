import json, os, sys

class CardRemapper:
    '''
    Functions for remapping a physical card to a virtual one.
    '''
    def __init__(self, card_path: str) -> None:
        self.filepath = card_path
        if not os.path.exists(self.filepath):
            print('Unable to locate cards.json!\nPlease make sure your path is correct.')
            sys.exit()

        self.cards = self.loadCards()
        print(f"Found {len(self.cards.keys())} remapped card(s)!\n")

    def addMapping(self, physical: bytes, virtual: bytes) -> None:
        '''
        Given a physical card ID and a virtual one, add to the data.
        '''
        physical = physical.decode('ascii')
        virtual = virtual.decode('ascii')
        self.cards[physical] = virtual
        return None

    def getMapping(self, card_id: bytes) -> bytes:
        '''
        Given a card_id, return either a virtual card or the source card,
        depending on if it's in the cards file.
        '''
        card_id = card_id.decode('ascii')
        card_id = self.cards.get(card_id, card_id)
        bytes(card_id, 'ascii')
        return card_id

    def loadCards(self) -> dict:
        '''
        Given the path to the cards.json file, return it as a dict.
        '''
        file = open(self.filepath, 'r')
        file_json = json.loads(file.read())
        file.close()

        return file_json

    def saveCards(self) -> None:
        '''
        Saves cards to the cards.json file.
        '''
        file = open(self.filepath, 'w')
        file.write(json.dumps(self.cards, indent=4))
        file.close()

        return None