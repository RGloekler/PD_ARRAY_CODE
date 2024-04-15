# @author Ryan Gloekler, UC Davis. Hunt Vacuum Microectronics Lab
# regloekler@ucdavis.edu
# Last updated: 2/28/2024

# NOTE: this program expects that the data being processed (csv file) contains
# only one shot, seperate shots of interest into seperate csv files.

# Operation: Run the script as: py read_excelData.py 'datafile.csv' x [animate]
# where x is the time values you would like to visualize, and animate is an optional
# parameter, allowing for a playback animation of all 100 datapoints over 10 seconds
# (10ms data collection period)

import os, sys, csv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import draw

# create a new array that can be plotted (expected data format)
def make_plottable(input_data):
    plottable_data = []
    for val in range(0,2): plottable_data.append(input_data)
    return plottable_data

# grab the apporpriate sample number (divide time by .1 ms)
def time_to_row(sample_time):
    # each row represents a sample, taken 100 us apart
    sample_length = 0.1 # ms
    sample_num = sample_time / sample_length
    sample_rounded = round(sample_num)
    return sample_num, sample_rounded

def plot_sample(data, time_val):
    # Set the figure size, and scale
    plt.rcParams["figure.figsize"] = [7, 3.50]
    plt.rcParams["figure.autolayout"] = True

    print('\nPlotting data closest to ' + str(time_val) + 'ms.')

    # set up the figure for plotting pixels
    fig, ax = plt.subplots(1,1)
    ax.set_title('PD Array Output at ' + str(time_val) + 'ms')
    ax.set_xlabel('Pixel Number')

    image = data
    im = ax.imshow(image, cmap='Reds', vmin = 0, vmax= 1)
    plt.show() # plot the last sample recieved
    return


def main():
    global ANIMATE
    ANIMATE = False
    if len(sys.argv) < 2:
        exit("Provide excel file name and desired time")
    else:
        filenm, time = sys.argv[1], float(sys.argv[2])
        excel_data = []

    if len(sys.argv) > 3:
        ANIMATE = True
        print('Animating data over 10ms.')

    print("Displaying data from the data point closest to " + str(time) + "ms")
    sample_value = time_to_row(time)[1]

    # catch out of bounds time values
    if sample_value > 100: sample_value = 100
    if sample_value < 1:   sample_value = 1

    with open(filenm, mode = 'r') as datafile:
        linereader = csv.reader(datafile)
        for line in linereader: excel_data.append(line)

    # remove header from excel data
    excel_data.pop(0)
    if ANIMATE:
        # set up the figure for plotting pixels
        # Set the figure size, and scale
        plt.rcParams["figure.figsize"] = [7, 3.50]
        plt.rcParams["figure.autolayout"] = True

        fig, ax = plt.subplots(1,1)
        image = make_plottable([1] * 15)
        im = ax.imshow(image, cmap='Reds', vmin = 0, vmax= 1)
        ax.set_title('PD Array Output')
        ax.set_xlabel('Pixel Number')

        for i in range(len(excel_data) - 1):
            datapoint = excel_data[i][:-2]
            scaled_converted = [float(val) for val in datapoint]
            plottable = make_plottable(scaled_converted)

            image = plottable
            im.set_data(image)
            fig.canvas.draw_idle()
            plt.pause(0.1) # pause for 100ms before drawing next frame
            # this means that 100 samples * .1 s = 10s
            # therefore, we are animating 10ms of data over 10s

    else:
        datapoint = excel_data[sample_value][:-2]
        scaled_converted = [float(val) for val in datapoint]
        plottable = make_plottable(scaled_converted)

        plot_sample(plottable, time)
    return

if __name__ == "__main__":
    main()
