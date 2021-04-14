# Faraday Rotation | Faraday-Controller

**[Back to CODE](https://github.com/PanosEconomou/advanced-lab/tree/main/2.Faraday-Rotation/2.Code)**  
**[Return to Main](https://github.com/PanosEconomou/advanced-lab)**

## Overview

This is everything that one needs to install on their computer in order to control for the faraday rotation apparatus. This has been developed and tested for Mac on Big Sur. This should be combined with the Arduino Code found [here](https://github.com/PanosEconomou/advanced-lab/tree/main/2.Faraday-Rotation/2.Code/Arduino_CLI_Parser).

1. **[clilib](https://github.com/PanosEconomou/advanced-lab/blob/main/2.Faraday-Rotation/2.Code/Faraday_Controller/clilib.py)**  
    Python library that contains all the commands that can be used to eithet build a command line interface application, or write a python script that controlls the faraday rotation apparatus.
2. **[oscillovisa](https://github.com/PanosEconomou/advanced-lab/blob/main/2.Faraday-Rotation/2.Code/Faraday_Controller/oscillovisa.py)**  
    Python library that is responsible for connecting to all the Faraday Rotation equipment, i.e. the oscilloscope and arduino.

## Examples

The rest of the files in this directory are examples of the application of clilib and oscillovisa. Specifically. [Faraday_CLI.py](https://github.com/PanosEconomou/advanced-lab/blob/main/2.Faraday-Rotation/2.Code/Faraday_Controller/Faraday_CLI.py) is a command line interface built with *clilib*, while [proceedure1.py](https://github.com/PanosEconomou/advanced-lab/blob/main/2.Faraday-Rotation/2.Code/Faraday_Controller/proceedure1.py) is a script that contains an experimental proceedure to measure data from the oscilloscope while moving the polarizer over a range of angles.

## Syntax

It is simple to write scripts that control the Faraday Rotation apparatus. Here we briefly go over how to do this.

To load the arduino and turn the polarizer one has to simply execute the following script:

    import oscillovisa
    import clilib

    # To get the arduino object
    arduino = oscillovisa.get_arduino(address='ARDUINO_SERIAL_ADDRESS')

    # To control its angle
    clilib.move_to_angle(arduino,ANGLE_IN_DEGREES)

To get data from the oscilloscope one can execute this script. The following saves the data from oscilloscope channels [1,2,3] and saves them to a file. It also plots the same data using matplotlib.

    import oscillovisa
    import clilib
    import matplotlib.pyplot as plt

    # To get the oscilloscope object
    oscilloscope = oscillovisa.get_instrunment(address='OSCILLOSCOPE_SERIAL_ADDRESS')

    # To save the data to csv
    oscillovisa.get_data_csv(oscilloscope,channels=[1,2,3],directory='./')

    # to plot the oscilloscope
    oscillovida.plot_oscilloscope(oscilloscope,channels=[1,2,3])
    plt.show()
