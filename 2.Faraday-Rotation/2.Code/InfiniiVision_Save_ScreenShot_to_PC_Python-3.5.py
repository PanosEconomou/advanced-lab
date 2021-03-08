# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 10:49:17 2017
Python Version 3.5

@author: GRSU

Description: This program reads the screen image data from an InfiniiVision 
oscilloscope and saves it to a local directory on the controller PC.
Feel free to change the save directory or type of image file.
Note: This program doesn't work with Windows-based Infiniium oscilloscopes, see the 
Infiniium example for the modified example.
Tested with DSOX3000A/T-series, DSOX2000-series, DSOX4000-series (firmware: 2.41.2015102200)
Tested with DSO6000-series (firmware: 6.20)
"""

import pyvisa as visa
import os  #needed to check the working directory

#Replace the VISA address shown here with the VISA address of your InfiniiVision.
#You'll find the VISA address within the IO Libraries installed on your PC.
VISA_ADDRESS = "TCPIP0::10.112.139.73::inst0::INSTR"
 
#Directory path to visa32.dll so it can be used by pyVISA
rm = visa.ResourceManager('C:\\Windows\\System32\\visa32.dll') # this uses pyvisa
## Open session using rm, which is the resource manager, and the visa address.
GSInfiniivision = rm.open_resource(VISA_ADDRESS)
## Set Global Timeout
GSInfiniivision.timeout = 10000
## Clear the instrument bus
GSInfiniivision.clear()
    
#Check Communication with the scope and print its name.
IDN = GSInfiniivision.query("*IDN?")
print(IDN)

#Check whether scope is an older InfiniiVision or a newer X-Series InfiniiVision.
#This is done by parsing the scope's identification string and looking for the 'X'.
IDN = IDN.split(',') # IDN parts are separated by commas, so parse on the commas
#mfg = IDN[0] # Python indices start at 0
model = IDN[1]
#SN = IDN[2]
#FW = IDN[3]

scopeTypeCheck = list(model)
if scopeTypeCheck[3] == "-" or scopeTypeCheck[1] == "9":
    generation = "X_Series"
else:
    generation = "Older_Series"
del IDN, scopeTypeCheck, model

#Set the directory where you want the screen image to save
os.chdir('C:\\Data')  #change the working directory
workingdirectory = os.getcwd()  #check working directory again

print ("The working directory is now: " + workingdirectory)


##############################################################################################################################################################################
##############################################################################################################################################################################
## Get and parse the IDN string to determine scope generation
##############################################################################################################################################################################
##############################################################################################################################################################################





    # The following function takes the raw PNG image data, which is an IEEE binary 
    #block, and interprets the header.  The header tells us how many bytes are
    #in the image file.  The function strips off the header and outputs the 
    #rest of the data to be saved to a .png file.
    #Note: A python function can be defined anywhere in the program, as long 
    #as it is defined prior to being called.
def binblock_raw(data_in):

    #Grab the beginning section of the image file, which will contain the header.
    Header = str(data_in[0:12])
    print("Header is " + str(Header))
    
    #Find the start position of the IEEE header, which starts with a '#'.
    startpos = Header.find("#")
    print("Start Position reported as " + str(startpos))
    
    #Check for problem with start position.
    if startpos < 0:
        raise IOError("No start of block found")
        
    #Find the number that follows '#' symbol.  This is the number of digits in the block length.
    Size_of_Length = int(Header[startpos+1])
    print("Size of Length reported as " + str(Size_of_Length))
    
    ##Now that we know how many digits are in the size value, get the size of the image file.
    Image_Size = int(Header[startpos+2:startpos+2+Size_of_Length])
    print("Number of bytes in image file are: " + str(Image_Size))
    
    # Get the length from the header
    offset = startpos+Size_of_Length
    
    # Extract the data out into a list.
    return data_in[offset:offset+Image_Size]
    
###########################################################################


GSInfiniivision.query(':SYSTEM:DSP "";*OPC?') # Turns off previously displayed (non-error) messages

#The following command defines whether the image background will be black or white.
#If you want to save ink, turn on this 'inksaver' setting.
GSInfiniivision.write(":HARDCOPY:INKSAVER OFF")
# Ask scope for screenshot in png format
if generation == "Older_Series":
    GSInfiniivision.write(":DISPlAY:DATA? PNG, SCREEN, COLOR") # The older InfiniiVisions have 3 parameters
elif generation == "X_Series":
    GSInfiniivision.write(":DISPlAY:DATA? PNG, COLOR") # The newer InfiniiVision-Xs do not have the middle parameter above

Image_Data = GSInfiniivision.read_raw()
print("Image has been read.\n")
#Returns image data as a List of floating values
Image_Data = binblock_raw(Image_Data)

#open a file and write the data to it.
#Feel free to change the file name.
filename = workingdirectory + "\\Scope_Image.png"
print(filename)
gsfile = open(filename, "wb") # wb means open for writing in binary; can overwrite
print(str(gsfile))
gsfile.write(Image_Data)
gsfile.close()
