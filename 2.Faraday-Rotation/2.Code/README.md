# Optical Tweezers | RESOURCES
**[Back to Faraday Rotation](https://github.com/PanosEconomou/advanced-lab/tree/main/2.Faraday-Rotation)**

**[Return to Main](https://github.com/PanosEconomou/advanced-lab)**

## Overview
All the code developed for the lab can be found here, as well as installation instructions and some limited documentation. Specifically we developed the Following:
- **oscillovisa**: A python library that handles communications with a VISA enabled oscilloscpe connected via USB.
- **CLIlib**: A python library that defines all the necessary Command Line Interface Methods to control an Arduino and an Oscilloscope connected to the same computer. It also includes our custom communication protocol for the communications with the arduino.
- **Faraday CLI**: A full fledged command line interface built in python that allows the user to control the Faraday Rotation Aparatus completely remotely.
- **Arduino CLI Parser**: The arduino companion to *CLIlib*, is the code that allows the arduino to decipher the data sent to it thorugh the serial monitor.

## Contents
1. [**Arduino CLI Parser**](https://github.com/PanosEconomou/advanced-lab/tree/main/2.Faraday-Rotation/2.Code/Arduino_CLI_Parser)
2. [**Arduino Handshake** *(Depreciated)*](https://github.com/PanosEconomou/advanced-lab/tree/main/2.Faraday-Rotation/2.Code/Arduino_Handshake)
3. [**Arduino Python Control** *(Depreciated)*](https://github.com/PanosEconomou/advanced-lab/tree/main/2.Faraday-Rotation/2.Code/Arduino_Python_Control)
4. [**Faraday CLI**](https://github.com/PanosEconomou/advanced-lab/tree/main/2.Faraday-Rotation/2.Code/Faraday_Controller)
5. [**Oscillovisa**](https://github.com/PanosEconomou/advanced-lab/tree/main/2.Faraday-Rotation/2.Code/Visa_Files)

## Notes
Installation instructions for each library can be found in the respective folders. We recommend any standard python environment, however the user might need to install some further dependencies. We list such dependencies in the README of each folder. The code was developed and tested for UNIX systems. If the user attempts to install in a windows version, please follow the relevant documentation for [*pySerial*](https://pypi.org/project/pyserial/) and especially [*VISA*](https://www.ni.com/en-lb/support/downloads/drivers/download.ni-visa.html).
