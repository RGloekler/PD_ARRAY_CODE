# Ryan Gloekler, Hunt Vacuum Microelectronics Lab
# regloekler@ucdavis.edu
# last updated 5/17/2023

# TODO: make sure plot has correct scaling values, make colors correct

from matplotlib import pyplot as plt
import numpy as np
import serial
import statistics as s
import time as t


def grab_serial():
    ser = serial.Serial('COM4', 9600, timeout=1)
    data = ser.readline()
    if data:
        print('Finished grabbing data from serial.')
    else:
        print('FAILED DATA COLLECTION')
        exit(1)
    return str(data)

""" OLD
# read from serial, and hold for 5 seconds waiting for data
def read_from_serial():
    # connect to serial port where Arduino is operating
    ser = serial.Serial('COM5', 9600, timeout=1)

    col_data = ''

    # set time for loop execution timeout,
    # allowing 5 seconds for data collection
    timeout = t.time() + 5

    # collect data from serial port, Arduino
    while(True):
        # break loop after collection time
        if t.time() > timeout: break

        # collect serial data
        if (ser.inWaiting() > 0):
            data_str = ser.read(ser.inWaiting()).decode('ascii')
            col_data += data_str

    print('Finished gathering data from serial...')
    return col_data.split('\n') # return the collected data
"""
# used for scaling a matrix of values - not used for averaged pixel value cases
def scale_values(data_array):
    scaled_array = np.empty(data_array.shape) # create new array for scaling

    for pixel in range(0, len(data_array)):
        for val in range(len(data_array[pixel])):
            ADC_val = data_array[pixel][val]      # get proper ADC value and scale
            val_norm = ADC_val / 1023             # max ADC value read from Arduino
            scaled_array[pixel][val] = val_norm   # update scaled value array

    return scaled_array

""" OLD
# process the data recieved from serial so that it can be plotted
def process_data(in_data):
    processed_data = []
    for val in in_data: processed_data.append(val.split(':')[0])

    # create a list containing the name of each unique pin, strip empty vals
    unique_prefixes = list(filter(None, set(processed_data)))

    # pin_data = np.empty((len(unique_prefixes), 1000))
    # create matrix for pin data storage
    pin_data = []
    for val in unique_prefixes: pin_data.append([val])

    # fill pin_data list with collected ADC values
    for val in range(len(unique_prefixes)):
        for data in in_data:
            if data.startswith(unique_prefixes[val]):
                pin_data[val].append(data.split(':')[1].strip())

    return pin_data
"""

def main():

    test_data = grab_serial().split(',')

    print(test_data)
    exit('grabbed.')

    # Set the figure size, and scale
    plt.rcParams["figure.figsize"] = [7, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # test reading from the serial COM4 port (Arduino data)
    data_collected = read_from_serial()

    # process and sort by pin number
    processed = process_data(data_collected)
    processed_sorted = sorted(processed, key=lambda x:x[0])

    print('\nPlotting light-intensity map')

    # create some test data (will come from pd array ADC eventually)
    # datavals = np.array([[0, 16, 32, 64, 128, 256, 512, 1023, 512, 256, 128, 64, 32, 16, 8]]) # , [44, 999, 444, 834, 112, 630]])

    # get the first element of each list and convert to integer for plotting
    # datavals_processed = np.array([[int(x[1:][0]) for x in processed_sorted]])

    # get an average of all pin values (over x microseconds?)
    # map each sub-list to integers, and take out the label from the start of
    # each list
    datavals_int = [list(map(int, x[1:])) for x in processed_sorted]
    datavals_avg = np.array([s.mean(x[1:]) for x in datavals_int])
    print(datavals_avg)

    # scale data for plotting
    # data = scale_values(datavals_avg)
    data = [[x / 1023 for x in datavals_avg]]
    print(data)

    # Plot the data using imshow with gray colormap
    plt.imshow(data, cmap='Greys', vmin = 0, vmax= 1)
    plt.title("Pixel Light Intensity, 10 us average sample")
    plt.xlabel('Pixel   ')
    plt.show()

if __name__ == '__main__':
    main()
