# Import the relevant libraries
import numpy as np 
import os
from datetime import datetime 

# These are relevant to collecting data

# Lists CSV Files in directory
def list_csv(directory = '.',PRINT=False):
    ''' Returns a list of all the '.csv' files in a given directory '''

    x = [x for x in os.listdir(directory) if x.endswith('.csv')]
    x = sorted(x)
    if PRINT: 
        print('List of .csv files in '+directory)
        for i,X in enumerate(x):
            print('\t',i,':',X)
    return x


# To create a CSV file 
def create_csv(name = '__time__.csv',directory='', titles = ['SAMPLE1','SAMPLE2','SAMPLE3'], data = [np.array([1,2,3]),None,np.array([1.2,3.4,5.6,7.8])]):
    ''' Creates a '.csv' file in a given directory. '''
    
    # Handle some exceptions
    if len(titles) < len(data): raise Exception("Data has more entries than titles")
    elif len(titles) > len(data): 
        for i in range(len(titles)-len(data)): data.append(None)
    
    if name.find('.csv') == -1:
        name+='.csv'
    
    if name == '__time__.csv': 
        now = datetime.now()
        name = now.strftime("%b-%d-%Y__%H-%M-%S.csv")

    # Now get to work
    # Get the maximum height of the table
    max_size = 0
    for datum in data:
        if type(datum) == np.ndarray:
            max_size = max([max_size,len(datum)])

    # open and create a CSV file
    FILE = open(directory+name,'xt')

    # First write the header:
    for i in range(len(titles)):
        delim = '\n' if i == len(titles)-1 else ','
        FILE.write(titles[i]+delim)

    # Now write data to the file:
    for i in range(max_size):
        for j in range(len(titles)):
            delim = '\n' if j == len(titles)-1 else ','

            if type(data[j]) == np.ndarray:
                if len(data[j]) > i:
                    FILE.write(str(data[j][i])+delim)
                else:
                    FILE.write('0'+delim)
            else:
                FILE.write('0'+delim)
    
    FILE.close()
    print(name+' created successfully')

