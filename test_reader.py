# Reader Test Suite
import sys
from cardio.tests.reader import ReaderTest

reader = ReaderTest('COM9', 9600)

com = reader.openSerial()
if com == None:
    print('Port failed to open!')
    sys.exit()

print('COM port opened!')
print('Please connect a game now.')

while True:
    try:
        reader.readSerial(com)
    except KeyboardInterrupt:
        print('goodbye!')
        sys.exit()