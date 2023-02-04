# CardIO Test Suite
import sys
from cardio.tests.cardio import CardIOTest

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