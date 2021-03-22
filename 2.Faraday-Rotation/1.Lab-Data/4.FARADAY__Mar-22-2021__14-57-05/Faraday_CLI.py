# This is the CLI for controlling the faraday rotation apparatus
from clilib import *
from clilib import VERBOSE
import clilib
import traceback
from pynput.keyboard import Key, Controller
import keyboard

# Print Welcome message
print(ASCII_ART)
print(bold(cs('Welcome to Faraday CLI!','#518ae5')))
print('''
A Comand Line Interface to control the Faraday Rotation Apparatus for data collection

You can type your commands in two ways:
    1. [:<number>] Numerically:
            for example ':21170' turns the polarizer by 170 degrees clockwise

    2. [<cmd> <number>] Linguistically:
            for example 'mbacw 170' or 'move_by_angle_cw 170' turns the polarizer by 170 degrees clockwise

Type 'help' for a list of all commands.

''')

# Connect to the devices
print("But first, let's connect the instrunments.")
arduino_address = input("\tArduino address (/dev/cu.usbmodem14101): ")
oscilloscope_address = input("\tOscilloscope Address (default): ")


try:
    if arduino_address == '':
        arduino = get_arduino(VERBOSE=VERBOSE)
    else:
        arduino = get_arduino(ADDRESS=arduino_address,VERBOSE=VERBOSE)

    if oscilloscope_address == '':
        oscilloscope = get_intstrunment(VERBOSE=VERBOSE)
    else:
        oscilloscope = get_intstrunment(ADDRESS=oscilloscope_address,VERBOSE=VERBOSE)

except:
    print(bold(cs("\nAn exception occurred",'red')))

else:
    print("\nOscilloscope and Arduino Are connected Successfully")

# oscilloscope = None

# Now start the loop
while True:
    msg = input(bold(cs('[FR]->> ','#3fbd80'))).strip()
    if msg == '': continue
    
    try:
        output = parse_input(msg,arduino,oscilloscope,sleep=sleep,VERBOSE=clilib.VERBOSE)
    except:
        print(cs('~parser (error): ' ,'red') + 'Command Error')
        traceback.print_exc()
        output = -1

    # print(cs('--ARDUINO: ','blue') + arduino.readline())

