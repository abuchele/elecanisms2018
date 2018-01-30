# Elecanisms 2018 Miniproject 0

### Anna Buchele

## Circuit Directions

To run this project, first build a circuit: Connect a switch on one side to Vout, and connect the other side to an input going to D0, as well as a pull-down resistor connected to ground. 

## Running the Project

Navigate to the elecanisms2018/blinkpoll directory in terminal. Run scons. This should generate a hex file to write to the board. 

In order to put the board in bootloader mode, press and hold the red button, then press and hold the black button, then release the red button, and finally release the black button. 

Once the board is in bootloader mode, navigate to the elecanisms2018/bootloader/ directory, and run bootloadergui.py. The bootloader gui should show up. Press 'connect' to connect to the board. If it won't connect, the device is not in bootloader mode. Once the device is connected, go to File:Import Hex, and import the elecanisms2018/blinkpoll/blinkpoll.hex file we generated earlier. Press 'write'. The hex file should now be written to the board. Now press Disconnect/Run. LEDs 2 and 3 should be blinking on the board. If this isn't happening, the device is still in bootloader mode. Now press the switch- LED 1 should light up with the press of the switch. 

