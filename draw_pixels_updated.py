# Ryan Gloekler, Hunt Vacuum Microelectronics Lab, MGXI Project
# @author: regloekler@ucdavis.edu
# last updated 11/3/2023

# Operation: Run draw_pixels_updated.py from the terminal. This will create a data
# file containing background signal, for the first 150 samples. The program will then
# terminate. Subsequent runs will not terminate, unless by the user, and will instead
# plot the live data, so that changes at the photodiode interface can be seen in
# real time. The values displayed have the average of the background data subtacted from
# them, so as to ensure that as much noise can be cut from the sensor readings as possible.

# This file has been replaced.. Use this one for live monitoring of the PD_array,
# rather than data collection. Data collection should be handled with read_pixels_fast.py

# NOTE: For this code to work, simple firmware writing the data to serial is needed. This code is
# now deprecated.

from datetime import *
from matplotlib import pyplot as plt
from matplotlib.pyplot import draw
import numpy as np
import serial, re, sys, csv, os, time

bg_data = 'background_pixelData.csv' # used to create csv files...
data_csv = 'bg_subtracted_data.csv'  # used to create new data files (bg_sub)

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

# create a new array that can be plotted (expected data format)
def make_plottable(input_data):
    plottable_data = []
    for val in range(0,2): plottable_data.append(input_data)
    return plottable_data

# creates a new csv file that background data can be written to
def create_csv(filenm):
    # create a csv file to write background noise data to, and a header array
    file = open('./' + filenm, 'w', encoding = 'UTF8', newline='')
    header = ['Pixel 1', 'Pixel 2', 'Pixel 3', 'Pixel 4', 'Pixel 5', 'Pixel 6', 'Pixel 7',
    'Pixel 8', 'Pixel 9', 'Pixel 10', 'Pixel 11', 'Pixel 12', 'Pixel 13', 'Pixel 14', 'Pixel 15', 'Pixel 16', 'TIME']

    writer = csv.writer(file)
    writer.writerow(header)
    return writer

# get the averaged data from the existing data file
def collect_csv_data():
    # read from csv file, and get the average of each column for
    # background subtraction

    data_array = []
    with open(bg_data, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for i, line in enumerate(reader):
            data_array.append(line)
        data_array.pop(0)

    averaged = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for row in range(len(data_array)):
        data_row = data_array[row][0].split(',')
        for val in range(len(data_row)):
            averaged[val] += float(data_row[val])

    averaged = [element / len(data_array) for element in averaged]
    return averaged

# main loop: creates figure, sets up serial communication, gets data from serial,
# performs background subtraction, and live plots the PD array data
def main():
    averaged_time = []
    timer_counter = 0
    # establish comms with the arduino
    ser = serial.Serial(port='COM4', baudrate=9600, timeout = 1)

    # setup regex, and grab some serial data
    non_decimal = re.compile(r'[^\d,]+')

    placeholder = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.0, 0.8, 0.5, 0.2]

    # Set the figure size, and scale
    plt.rcParams["figure.figsize"] = [7, 3.50]
    plt.rcParams["figure.autolayout"] = True


    print('\nPlotting light-intensity map')

    # set up the figure for plotting pixels
    fig, ax = plt.subplots(1,1)
    image = make_plottable(placeholder)
    im = ax.imshow(image, cmap='Reds', vmin = 0, vmax= 1)
    ax.set_title('PD Array Output')
    ax.set_xlabel('Pixel Number')

    # initiate the main loop of the program... Grab and plot data
    # log the first several hundred samples to a csv file for background subtraction

    # handle the case that we don't need background data...
    if bg_data in os.listdir('./'):
        background_counter = -1
        print('Background data collected. Plotting current data.')

        writer = None
        averaged = collect_csv_data()
        data_writer = create_csv(data_csv)

    # if we do need background data...
    if bg_data not in os.listdir('./'):
        writer = create_csv(bg_data)
        data_writer = None

        background_counter = 0
        print('Collecting 150 background samples...')

    while True:
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
        plottable = [[]]

        """ SKIPPING BG SUBTRACTION FOR NOW
        if bg_data in os.listdir('./'): # dont bg sub if there is no bg
            for val in range(len(scaled)):
                try:
                    scaled[val] = float(scaled[val]) - float(averaged[val]) # perform the background subtraction, and plot
                except:
                    print("Couldn't update.. Trying again")
        """
        print(scaled)
        plottable = make_plottable(scaled)
        try: # update the canvas...
            image = plottable
            im.set_data(image)
            fig.canvas.draw_idle()
            plt.pause(0.00001)
        except:
            print('Couldnt update canvas... Data error.')


        # write the scaled data to the appropriate spreadsheet
        if writer: writer.writerow(scaled)
        else:
            scaled.append(str(datetime.now())) # add the time to the data...
            data_writer.writerow(scaled)

        # check conditionals for background data
        if background_counter > -1: background_counter += 1
        if background_counter >= 150: exit('Finished Collecting Background data.')
        final_time = time.perf_counter()

        timer_counter += 1
        averaged_time.append(final_time - initial_time)
        if timer_counter % 200 == 0:
            print(np.mean(averaged_time))
    file.close()

if __name__ == '__main__':
    main()
