# @author Ryan Gloekler, UC Davis. Hunt Vacuum Microectronics Lab
# regloekler@ucdavis.edu
# Last updated: 2/28/2024

# NOTE: this program expects that the data being processed (csv file) contains
# only one shot, seperate shots of interest into seperate csv files.

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
    print('\nPlotting data closest to ' + str(time_val) + 'ms.')

    # Set the figure size, and scale
    plt.rcParams["figure.figsize"] = [7, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # set up the figure for plotting pixels
    fig, ax = plt.subplots(1,1)
    image = data
    im = ax.imshow(image, cmap='Reds', vmin = 0, vmax= 1)
    ax.set_title('PD Array Output')
    ax.set_xlabel('Pixel Number')
    plt.show() # plot the last sample recieved
    return


def main():
    if len(sys.argv) < 2:
        exit("Provide excel file name and desired time")
    else:
        filenm, time = sys.argv[1], float(sys.argv[2])
        excel_data = []

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
    datapoint = excel_data[sample_value][:-2]
    scaled_converted = [float(val) for val in datapoint]
    plottable = make_plottable(scaled_converted)

    plot_sample(plottable, time)
    return

if __name__ == "__main__":
    main()
