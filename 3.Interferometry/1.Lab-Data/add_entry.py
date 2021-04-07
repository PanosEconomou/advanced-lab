# This script adds an entry to the current lab session based on the template

import os
from datetime import datetime 
from shutil import copyfile

# IDENTIFIER
CODENAME = 'INTERFEROMETRY'

# Get the lab session number
session_number = max([int(x[0]) for x in os.listdir('.') if x[1] == '.']) + 1

# Get the new directory name
now = datetime.now()
name = now.strftime(str(session_number)+"."+CODENAME+"__%b-%d-%Y__%H-%M-%S")

# Make the new directory
os.mkdir(name)

# Copy the tutorial directory to the new one
copyfile('0.TEMPLATE/csvlib.py',name+'/csvlib.py')
copyfile('0.TEMPLATE/data.csv',name+'/data.csv')
copyfile('0.TEMPLATE/README.md',name+'/README.md')
copyfile('0.TEMPLATE/0.Template.ipynb',name+'/'+str(session_number)+'.ANALYSIS.ipynb')
