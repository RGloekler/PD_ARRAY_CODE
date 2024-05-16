# @author Ryan Gloekler, UC Davis. Hunt Vacuum Microectronics Lab
# regloekler@ucdavis.edu
# Reads and processes Serial data recieved from Arduino ADC module, sampling at 10KHz for 10ms.
# Plots the average data across the sensor over this time period.
# Stores data samples for each shot in 'data_collection_dump.csv' for later analysis
# Last updated: 2/28/2024

from datetime import *
from time import *
from matplotlib import pyplot as plt
from matplotlib.pyplot import draw
import serial, re, sys, csv, os
import numpy as np

#------------------------ DEFINE HELPER FUNCTIONS ------------------------------

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
        try: data_array[val] /= 1023 # arduino uses a 10-bit ADC, 1024 values
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
    file = open('./' + filenm, 'a', encoding = 'UTF8', newline='')
    header = ['Pixel 1', 'Pixel 2', 'Pixel 3', 'Pixel 4', 'Pixel 5', 'Pixel 6', 'Pixel 7',
    'Pixel 8', 'Pixel 9', 'Pixel 10', 'Pixel 11', 'Pixel 12', 'Pixel 13', 'Pixel 14', 'Pixel 15', 'Pixel 16', 'Sample No.', 'Serial Time']

    writer = csv.writer(file)
    writer.writerow(header)
    return writer

#----------------------- IMPLEMENT MAIN FUNCTIONALITY --------------------------
# since the heavy lifting is done in firmware, we just need to read all the
# data from serial here...
def main():
    # search for csv, create one if it is not found
    filenm = 'shot_data/data_collection_dump.csv'
    if filenm not in os.listdir('./'):
        file_writer = create_csv(filenm)
    else:
        file_writer = csv.writer(open(filenm, 'a', encoding = 'UTF8', newline=''))

    # set up serial communication
    ser = serial.Serial(port='COM3', baudrate=115200, timeout = 1)
    # setup regex for data parsing
    non_decimal = re.compile(r'[^\d,]+')

    # set sample counter to 0
    counter = 0

    # main loop of operation - constanty scan serial,
    # until we recieve data from ADC (firmware has been triggered)
    averaged = []
    averaged_np = []
    new_shot = True
    while True:
        line = grab_serial(ser).split(', ')
        if len(line) > 2: # get only proper pixel data from serial

            # if a shot has occurred, create a new CSV file for it.
            if new_shot:
                cur_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
                print(cur_time)
                new_shot = False # set the new shot flag, so we dont re-create files for each line
            
                newfile = 'shot_data/background_' + cur_time +'.csv'
                if newfile not in os.listdir('./'):
                    file_writer = create_csv(newfile)
                else:
                    file_writer = csv.writer(open(newfile, 'a', encoding = 'UTF8', newline=''))


            
            # create processing array and start counting data points
            processed = []
            counter += 1

            # convert all values to integers, omit all other characters
            for val in range(len(line)):
                converted = non_decimal.sub('', line[val])
                processed.append(converted)

            # trim array to include only floating point values
            processed = [int(val) for val in processed]

            # scale values to range of 0-1, omitting the sample number row
            scaled = scale_values(processed[0:-1])

            # convert data to floating point and get a plottable version for later
            scaled_converted = [float(val) for val in scaled]
            averaged.append(scaled_converted)
            plottable = make_plottable(scaled_converted)

            # add metadata to the data, for final excel readability
            scaled.append(processed[-1])
            scaled.append(str(datetime.now()))
            print(scaled)

            # write the current set of pixel data to csv, and close file
            file_writer.writerow(scaled)
            
            # if recieved a complete set of data, plot it
            if counter % 100 == 0:
                # if we are ready to finish handling this shot, average data
                # for plotting

                # print(averaged)

                # create a numpy array object to handle averaging
                # uncomment this block to enable averaging over the total 10ms
                # period
                print('\nPLOTTING DATA AVERAGED OVER 10ms')
                np_array = np.array(averaged)
                averaged_np = np.mean(np_array, axis=0)
                plottable = make_plottable(averaged_np)

                # Set the figure size, and scale
                plt.rcParams["figure.figsize"] = [7, 3.50]
                plt.rcParams["figure.autolayout"] = True

                print('\nPlotting light-intensity map...')

                # set up the figure for plotting pixels
                fig, ax = plt.subplots(1,1)
                image = plottable
                im = ax.imshow(image, cmap='Reds', vmin = 0, vmax= 1)
                ax.set_title('PD Array Output')
                ax.set_xlabel('Pixel Number')
                plt.show() # plot the last sample recieved
                averaged = [] # reset the averaging list for the next shot
                
                new_shot = True # reset shot flag for next shot data collection

if __name__ == '__main__':
    main()
