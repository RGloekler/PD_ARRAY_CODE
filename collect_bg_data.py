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


def main():
    bg_data = 'background_data_test.csv'
    ser = serial.Serial(port='COM4', baudrate=9600, timeout = 1)

    # setup regex, and grab some serial data
    non_decimal = re.compile(r'[^\d,]+')

    placeholder = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.0, 0.8, 0.5, 0.2]

    # if we do need background data...
    if bg_data not in os.listdir('./'):
        writer = create_csv(bg_data)
        data_writer = None

        background_counter = 0
        print('Collecting 150 background samples...')

        for i in range (0, 149):
            initial_time = time.perf_counter()
            # grab a new set of data from each of the pixels
            new_data = grab_serial(ser).split(',')

            # convert all values to integers, so they may be scaled
            for val in range(len(new_data)):
                converted = non_decimal.sub('', new_data[val])
                if converted: new_data[val] = int(converted)

            # scale the values for plotting, and get an array from them that can be
            # plotted
            scaled = scale_values(new_data)
            print(scaled)
    else:
        exit('Background data already exists..')


if __name__ == '__main__':
    main()
