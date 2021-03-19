# Environment Variables
VERBOSE = False
sleep = 0.001
ASCII_ART ='''
  ______                  _               _____       _        _   _             
 |  ____|                | |             |  __ \     | |      | | (_)            
 | |__ __ _ _ __ __ _  __| | __ _ _   _  | |__) |___ | |_ __ _| |_ _  ___  _ __  
 |  __/ _` | '__/ _` |/ _` |/ _` | | | | |  _  // _ \| __/ _` | __| |/ _ \| '_ \ 
 | | | (_| | | | (_| | (_| | (_| | |_| | | | \ \ (_) | || (_| | |_| | (_) | | | |
 |_|  \__,_|_|  \__,_|\__,_|\__,_|\__, | |_|  \_\___/ \__\__,_|\__|_|\___/|_| |_|
                                   __/ |                                         
                                  |___/                                          
'''



## COMMAND MAP ######################################################
#
# Every command is an integer that has the following structure
#                       'AAXXXX\n'
# Where the number AA denotes the command, and XXXX the value 
# associated with it.
# 
# As a result here is a list of commands:
#
# AA - Decipher
# -------------------------------------------------------------------
# 10 - Set current angle to 0
# 11 - Set current speed to XXXX
# 20 - Move to angle XXXX
# 21 - Move by angle XXXX Clockwise
# 22 - Move angle by XXXX Counter Clockwise
# 30 - Send the Current angle through the serial port
# -1 - Internal Commands (like help, etc.)
#
######################################################################

# Here is a dictionary with the commands
CMDS = {
    'set_angle':10,
    'sa': 10,

    'set_speed':11,
    'ss':11,

    'move_to_angle': 20,
    'mta': 20,

    'move_by_angle':21,
    'mba':21,
    'move_by_angle_cw': 21,
    'mbacw':21,

    'move_by_angle_ccw':22,
    'mbaccw':22,

    'read_angle':30,
    'ra':30,

    'set_sleep':-1,
    'sleep':-1,

    'read_monitor':-1,
    'read':-1,
    'r':-1,
}


from oscillovisa import *
from stringcolor import *
import time
import traceback

# Send Command ###################################################
def send_command(cmd,  arduino, sleep=0.001, VERBOSE=False):
    '''
    Writes a command to the arduino by sending the appropriate integer code to it.

    cmd: [Required] The integer value of the command, given either as string or number
    arduino: [Required] the serial port the arduino is in
    sleep (0.001): How long to sleep after sending the message in s
    VERBOSE (False): If true prints a confirmation message
    '''

    # If the command is not a string, convert it.
    if type(cmd) != str:
        cmd = str(int(cmd))
    
    # Send the command to the Arduino
    arduino.write(cmd.encode()+b'\n')
    time.sleep(sleep)

    if VERBOSE: print("Command '"+cmd+ "\\n' Sent successfully to "+ arduino.name)



# Read From arduino #################################################
def read_line( arduino,sleep=0.001,VERBOSE=False):
    '''
    Writes until new line in the serial buffer.

    arduino: [Required] the serial port object the arduino is in
    sleep (0.001): How long to sleep after sending the message in s
    VERBOSE (False): If true prints the value read

    Returns:
    msg: String that contains the received message
    '''

    msg = arduino.readline()
    time.sleep(sleep)

    if VERBOSE: print("Message from ["+arduino.name+"]: "+str(msg))

    return msg



#############################################################################################
# Here we will just write some wrappers to easily encapsulate our code. #####################
#############################################################################################

# Set current angle to zero
def set_angle(angle, arduino,sleep=0.001,VERBOSE=False):
    '''
    Sets the angle of the arduino by sending the appropriate integer code to it.

    angle: [Required] The integer value of the angle
    arduino: [Required] the serial port the arduino is in
    sleep (0.001): How long to sleep after sending the message in s
    VERBOSE (False): If true prints a confirmation message
    '''
    # Construct the command
    AA = CMDS['set_angle']
    XXXX = int(angle)%360

    cmd = AA*10000 + XXXX

    # Send te command
    send_command(cmd,arduino,sleep,VERBOSE)


def set_speed(speed, arduino,sleep=0.001,VERBOSE=False):
    '''
    Sets the speed of the stepper motor by sending the appropriate integer code to it.

    speed: [Required] The integer value of the speed in rpm
    arduino: [Required] the serial port the arduino is in
    sleep (0.001): How long to sleep after sending the message in s
    VERBOSE (False): If true prints a confirmation message
    '''
    # Construct the command
    AA = CMDS['set_speed']
    XXXX = int(speed)

    cmd = AA*10000 + XXXX

    # Send te command
    send_command(cmd,arduino,sleep,VERBOSE)


def move_to_angle(angle, arduino,sleep=0.001,VERBOSE=False):
    '''
    Moves the polarizer to the angle by sending the appropriate integer code to it.

    angle: [Required] The integer value of the angle
    arduino: [Required] the serial port the arduino is in
    sleep (0.001): How long to sleep after sending the message in s
    VERBOSE (False): If true prints a confirmation message
    '''
    # Construct the command
    AA = CMDS['move_to_angle']
    XXXX = int(angle)%360

    cmd = AA*10000 + XXXX

    # Send te command
    send_command(cmd,arduino,sleep,VERBOSE)


def move_by_angle_cw(angle, arduino,sleep=0.001,VERBOSE=False):
    '''
    Moves the polarizer by an angle clockwise.

    angle: [Required] The integer value of the angle
    arduino: [Required] the serial port the arduino is in
    sleep (0.001): How long to sleep after sending the message in s
    VERBOSE (False): If true prints a confirmation message
    '''
    # Construct the command
    AA = CMDS['move_by_angle_cw']
    XXXX = int(angle)%360

    cmd = AA*10000 + XXXX

    # Send te command
    send_command(cmd,arduino,sleep,VERBOSE)


def move_by_angle_ccw(angle, arduino,sleep=0.001,VERBOSE=False):
    '''
    Moves the polarizer by an angle counter clockwise.

    angle: [Required] The integer value of the angle
    arduino: [Required] the serial port the arduino is in
    sleep (0.001): How long to sleep after sending the message in s
    VERBOSE (False): If true prints a confirmation message
    '''
    # Construct the command
    AA = CMDS['move_by_angle_ccw']
    XXXX = int(angle)%360

    cmd = AA*10000 + XXXX

    # Send te command
    send_command(cmd,arduino,sleep,VERBOSE)


def read_angle(arduino,sleep=0.001,VERBOSE=VERBOSE):
    '''
    Reads the current angle from the arduino.

    arduino: [Required] the serial port the arduino is in
    sleep (0.001): How long to sleep after sending the message in s
    VERBOSE (False): If true prints a confirmation message

    Returns:
    angle: An integer of the angle obtained from the arduino
    '''
    # Construct the command
    AA = CMDS['read_angle']
    cmd = AA*10000

    # Send te command
    send_command(cmd,arduino,sleep,VERBOSE)

    # Read the output from the serial monitor
    msg = read_line(arduino,sleep,VERBOSE)
    
    # Parse the message
    angle = int(float(msg))

    if VERBOSE: print(bold(cs('~parser: ','yellow')) + '%d'%angle)

    return angle


def set_sleep(SLEEP):
    '''
    Sets the default sleep value for a command to be executed

    SLEEP (0.001): [Required] the sleep time in s
    '''
    global sleep
    sleep = SLEEP

    print(cs('~parser:','yellow')+' sleep = %.3e s'%sleep)


def set_verbose():
    '''
    Sets the default VERBOSE value for a command to be executed

    verbose (False): [Required] the VERBOSITY
    '''
    global VERBOSE
    VERBOSE = not VERBOSE

    print(cs('~parser:','yellow')+' VERBOSE = ' + str(VERBOSE))


def read_monitor(arduino,sleep=sleep,VERBOSE=VERBOSE):
    '''
    Reads the contents of the serial monitor of the arduino up until the next line
    '''

    msg = arduino.readline()
    time.sleep(sleep)
    print(cs('--ARDUINO: ','blue') + msg)

    return msg

def help():
    '''
    Displays a list of Commands.
    '''

    print(bold('Here is a list of Commands'))
    for pair in FCMDS.items():
        print(bold('\n-> '+pair[0]))
        print(pair[1].__doc__[1:int(pair[1].__doc__.index('\n',1))])

        


# FUNCTION DICTIONARY

FCMDS = {
    'set_angle':set_angle,
    'sa': set_angle,

    'set_speed':set_speed,
    'ss':set_speed,

    'move_to_angle': move_to_angle,
    'mta': move_to_angle,

    'move_by_angle':move_by_angle_cw,
    'mba':move_by_angle_cw,
    'move_by_angle_cw': move_by_angle_cw,
    'mbacw':move_by_angle_cw,

    'move_by_angle_ccw':move_by_angle_ccw,
    'mbaccw':move_by_angle_ccw,

    'read_angle':read_angle,
    'ra':read_angle,

    'set_verbose':set_verbose,
    'verbose':set_verbose,
    
    'set_sleep':set_sleep,
    'sleep':set_sleep,

    'get_data_csv':get_data_csv,
    'data':get_data_csv,

    'plot_oscilloscope':plot_oscilloscope,
    'plot':plot_oscilloscope,

    'read_monitor':read_monitor,
    'read':read_monitor,
    'r':read_monitor,

    'help':help
}

#############################################################################################
# Finally we need a parser for the user input. ##############################################
#############################################################################################

# In the CLI commands are structured like so
# 
# CMD                   Decipher
# ---------------------------------------------------------------------------
# :<number>             Just sends the numerical command
# <command> <number>    Executes the command with optional argument <number>


# Checks if a command is valid
def valid(cmd):
    '''
    Checks if a command is valid based on the available commands

    cmd: [Required] integer of the command

    Returns:
    [bool,str]: bool is True if the command is correct, and False if it is not
    If the command is not valid, then str contains the error message
    '''

    AA = int(cmd/10000)
    XXXX = int(cmd%10000)

    # Check for the right number of digits
    if cmd > 999999:
        return [False,' Command '+str(int(cmd))+' has the wrong number of digits']
    
    # Check if the command is in the list
    if AA not in CMDS.values():
        return [False,' Command '+str(int(cmd))+' not recognised']
    
    # Check if the arithmetic value is within the limits
    if AA in [10,20,21,22]:
        if XXXX < 0:
            return [False,"Angle can't be negative (and needs to be in degrees)"]

        if XXXX > 360:
            return [False,"Angle can't be greater than 360 (and needs to be in degrees)"]

    if AA in [11]:
        if XXXX == 0:
            return [False,"Speed can't be zero (and needs to be in rpm)"]

    return [True,'Recognised Command']


# Parses the input from the command prompt
def parse_input(msg,arduino,oscilloscope,sleep=0.001,VERBOSE=False):
    '''
    Parses the input form the Command Line Interface and sends the appropriate instruction

    msg: [Required] The string command
    arduino: [Required] the serial port the arduino is in
    sleep (0.001): How long to sleep after sending the message in s
    VERBOSE (False): If true prints a confirmation message

    Returns:
    Command output if there is one
    -1 if there is an error
    '''

    # If it is a simple numerical command, just send it
    if msg[0] == ':':
        cmd = int(msg[1:7])

        # Check the validity of the command
        VALID, error = valid(cmd)
        if not VALID: 
            print(cs('~parser (error): ' ,'red') + error)
            return -1
        
        # Execute the command
        return send_command(cmd,arduino,sleep=sleep,VERBOSE=VERBOSE)
    
    # If the command is in the proper way to write it
    else:
        if len(msg.split(' ')) == 2:
            # Split the message in spaces
            aa,xxxx = msg.split(' ')
            AA = CMDS[aa]

            # If it is a system command
            if AA == -1:
                # Check for errors
                if aa not in FCMDS.keys():
                    print(cs('~parser (error): ' ,'red') + 'Command not recognized')
                    return -1
                else:
                    return FCMDS[aa](float(msg.split(' ')[1]))

            XXXX = int(xxxx)
            cmd = AA*10000 + XXXX

            # Check the validity of the command
            VALID, error = valid(cmd)
            if not VALID: 
                print(cs('~parser (error): ' ,'red') + error)
                return -1
            
            #Execute the command
            return FCMDS[aa](XXXX,arduino,sleep=sleep,VERBOSE=VERBOSE)
        
        elif len(msg.split(' ')) == 1:
            # Check for errors
            if msg not in FCMDS.keys():
                print(cs('~parser (error): ' ,'red') + 'Command not recognized')
                return -1

            if msg in CMDS.keys():
                return FCMDS[msg](arduino,sleep=sleep,VERBOSE=VERBOSE)

            if FCMDS[msg] in [get_data_csv,plot_oscilloscope]:
                return FCMDS[msg](oscilloscope,VERBOSE=VERBOSE)
            else:
                return FCMDS[msg]()
