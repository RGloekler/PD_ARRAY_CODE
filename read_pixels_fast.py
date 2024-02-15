# @author Ryan Gloekler, UC Davis. Hunt Vacuum Microectronics Lab
# regloekler@ucdavis.edu

from datetime import *
from matplotlib import pyplot as plt
from matplotlib.pyplot import draw
import numpy as np
import serial, re, sys, csv, os

# grab current data from the serial bus
def grab_serial(ser):
    line = ser.readline()
    #line = sys.stdout.write(str(ser.readline()))
    sys.stdout.flush()
    return str(line)

# used for scaling a matrix of values - not used for averaged pixel value cases
def scale_values(data_array):
    # normalize
    for val in range(len(data_array)):
        try: data_array[val] /= 1023
        except: print("Couldn't convert... Trying again")
    return data_array

# creates a new csv file that background data can be written to
def create_csv(filenm):
    # create a csv file to write background noise data to, and a header array
    file = open('./' + filenm, 'a', encoding = 'UTF8', newline='')
    header = ['Pixel 1', 'Pixel 2', 'Pixel 3', 'Pixel 4', 'Pixel 5', 'Pixel 6', 'Pixel 7',
    'Pixel 8', 'Pixel 9', 'Pixel 10', 'Pixel 11', 'Pixel 12', 'Pixel 13', 'Pixel 14', 'Pixel 15', 'Sample No.', 'Serial Time']

    writer = csv.writer(file)
    writer.writerow(header)
    return writer

# since the heavy lifting is done in firmware, we just need to read all the
# data from serial here...
def main():
    # search for csv, create one if it is not found
    filenm = 'data_test.csv'
    if filenm not in os.listdir('.'):
        file_writer = create_csv(filenm) # create a csv to store image data
    else: file_writer = csv.writer(open(filenm, 'a', encoding = 'UTF8', newline=''))

    ser = serial.Serial(port='COM4', baudrate=115200, timeout = 1) # set up serial communication
    non_decimal = re.compile(r'[^\d,]+') # setup regex for data parsing

    while True:
        line = grab_serial(ser).split(', ') # constantly poll serial until new data is recieved

        if len(line) > 2: # get only proper pixel data from serial
            processed = [] # create processing array
            # convert all values to integers, omit all other characters
            for val in range(len(line)):
                converted = non_decimal.sub('', line[val])
                processed.append(converted)

            # trim array to include only floating point values
            processed = [int(val) for val in processed]

            # scale values to range of 0-1, omitting the sample number row
            scaled = scale_values(processed[0:-1])
            scaled.append(processed[-1])
            scaled.append(str(datetime.now()))
            print(scaled)

            # write the current set of pixel data to csv, and close file
            file_writer.writerow(scaled)

if __name__ == '__main__':
    main()
