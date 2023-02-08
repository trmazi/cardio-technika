# cardio-technika
 A Technika/Cyclon card reader interface for CardIO.

## How to use

If you don't want to use .py files...
Go ahead and grab the latest release, use that instead!
Release includes all dependencies already, just run and go.

### `cardio_technika.py`
Here's the main software. To use it, here are the basic steps.
- Install Com0Com or some other virtual null modem tool
- Add a pair of COM ports as `COM6` -> `COM9`
  - You can change `COM9` but `COM6` MUST be set as this is where the game looks
- Install all required packages using the `requirements.txt` file
- Start `cardio_technika.py` with a CardIO plugged in and you should be good to go!

Arguments
- `--com_port`: Serial port to listen on. Defaults to `COM9`
- `--baud_rate`: Baud rate to talk at. Defaults to 9600
- `--card_file`: Place to look for virtual cards. Defaults to `./cards.json`

### `card_remapper.py`
This is a simple tool that lets you scan a physical card and pair it with a virtal ID. This is good for non-technika cards.
Simply install requirements, plug in a CardIO, run it. 

### `cardio_test`
To run the test for CardIO, simply install the python requirements, plug in a CardIO device, and run `python .\test_cardio`!

You'll get some info about your device, and will be asked to tap a card.

### `serial_test`
This is a test tool for verfying communication between the game and python.
Simply run it and set up a null modem connector.
