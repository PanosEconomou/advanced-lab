# Lookup environment variable MSOX3000_IP and use it as the resource
# name or use the TCPIP0 string if the environment variable does
# not exist
from msox3000 import MSOX3000
from os import environ
resource = environ.get('MSOX3000_IP', 'USB0::0x0957::0x173D::MY50340583::INSTR')

# create your visa instrument
instr = MSOX3000(resource)
instr.open()

# set to channel 1
#
# NOTE: can pass channel to each method or just set it
# once and it becomes the default for all following calls. If pass the
# channel to a Class method call, it will become the default for
# following method calls.
instr.channel = '1'

# Enable output of channel, if it is not already enabled
if not instr.isOutputOn():
    instr.outputOn()

# Install measurements to display in statistics display and also
# return their current values here
print('Ch. {} Settings: {:6.4e} V  PW {:6.4e} s\n'.
          format(instr.channel, instr.measureVoltAverage(install=True),
                     instr.measurePosPulseWidth(install=True)))

# Add an annotation to the screen before hardcopy
instr.annotateColor("CH{}".format(instr.channel))
instr.annotate('{}\\n{} {}'.format('Example of Annotation','for Channel',instr.channel))

# Change label of the channel to "MySig"
instr.channelLabel('MySig')

# Make sure the statistics display is showing for the hardcopy
instr._instWrite("SYSTem:MENU MEASure")
instr._instWrite("MEASure:STATistics:DISPlay ON")

## Save a hardcopy of the screen to file 'outfile.png'
instr.hardcopy('outfile.png')

# Change label back to the default and turn it off
instr.channelLabel('{}'.format(instr.channel))
instr.channelLabelOff()

# Turn off the annotation
instr.annotateOff()

# turn off the channel
instr.outputOff()

# return to LOCAL mode
instr.setLocal()

instr.close()