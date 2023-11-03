# Ryan Gloekler, Hunt Vacuum Microelectronics Lab, MGXI Project
# @author: regloekler@ucdavis.edu
# last updated 11/3/2023

from datetime import *
from matplotlib import pyplot as plt
from matplotlib.pyplot import draw
import numpy as np
import serial, re, sys, csv, os


# create a new array that can be plotted (expected data format)
def make_plottable(input_data):
    plottable_data = []
    for val in range(0,2): plottable_data.append(input_data)
    return plottable_data


# open the passed csv file, and play back its contents
def main():
    # check that we got an input file
    if len(sys.argv) != 2: exit('Make sure file input is correct.')

    # make sure the provided file exists
    filenm = sys.argv[-1]
    if filenm not in os.listdir('./'): exit('File not in directory')

    read_data = []

    # open the file and write its contents to an array.
    with open("./" + filenm, "r") as file:
        reader = csv.reader(file, delimiter="\t")

        # get each value, and take off their time-stamps
        for i, line in enumerate(reader):
            read_data.append(line[0].split(',')[:-1])
        read_data.pop(0)

    # convert to floating point data from strings...
    converted = []
    for val in read_data: converted.append([float(i) for i in val])

    print('\nPlotting light-intensity map')
    placeholder = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.0, 0.8, 0.5, 0.2]

    # Set the figure size, and scale
    plt.rcParams["figure.figsize"] = [7, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # set up the figure for plotting pixels
    fig, ax = plt.subplots(1,1)
    image = make_plottable(placeholder)
    im = ax.imshow(image, cmap='Reds', vmin = 0, vmax= 1)
    ax.set_title('PD Array Output')
    ax.set_xlabel('Pixel Number')

    for val in converted:
        plottable = make_plottable(val)
        try: # update the canvas...
            image = plottable
            im.set_data(image)
            fig.canvas.draw_idle()
            plt.pause(0.11) # wait 0.11 seconds before updating. Simulates average COM read time
        except:
            print('Couldnt updata canvas... Data error.')

    print('Playback complete.')
    file.close()
if __name__ == "__main__":
    main()
