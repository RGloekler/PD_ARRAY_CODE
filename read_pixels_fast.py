from datetime import *
from matplotlib import pyplot as plt
from matplotlib.pyplot import draw
import numpy as np
import serial, re, sys, csv, os, time


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
    file = open('./' + filenm, 'w', encoding = 'UTF8', newline='')
    header = ['Pixel 1', 'Pixel 2', 'Pixel 3', 'Pixel 4', 'Pixel 5', 'Pixel 6', 'Pixel 7',
    'Pixel 8', 'Pixel 9', 'Pixel 10', 'Pixel 11', 'Pixel 12', 'Pixel 13', 'Pixel 14', 'Pixel 15', 'Pixel 16', 'TIME']

    writer = csv.writer(file)
    writer.writerow(header)
    return writer

# since the heavy lifting is done in firmware, we just need to read all the
# data from serial here...
def main():
    # create a csv to store the data in...
    file_writer = create_csv('data_test.csv')

    ser = serial.Serial(port='COM4', baudrate=115200, timeout = 1)
    while True:
        line = grab_serial(ser).split(', ')
        if line: print(line)

if __name__ == '__main__':
    main()
