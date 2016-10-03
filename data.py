import csv
import numpy as np
import matplotlib.pyplot as plt
import math

def get_header_list(filename, my_delimiter):
    '''(str,str) --> list
    This function opens a file and returns the column names (list) in the
    header of the file, given a filename (str) and a delmiter (Str).

    >>> get_header_list('glass_shrimp.csv', ',')
    ['Salinity (ppt)', 'Mean heart rate (beats/min)', 'Confidence interval']
    '''
    data_file = open(filename,'r')
    reader = csv.reader(data_file, delimiter=my_delimiter)

    for line in reader:
        return line
    data_file.close()


def read_columns(filename, columns, my_delimiter):
    '''(str, list, str) --> array
    This function returns an array, given a filename (str), a list of
    columns and a delimiter (str). The array contains the columns from the
    file which are in the given list of ints.

    >>> read_columns('glass_shrimp.csv', [0, 2], ',')
    array([[  5.,  57.],
           [ 10.,  37.],
           [ 15.,  35.],
           [ 20.,  33.]])
    '''
    data = np.genfromtxt(filename, delimiter=my_delimiter, skip_header = 1,
                         usecols=columns)
    np.set_printoptions(suppress=True) #gives small floating point values
    return data

def get_avg_all_rows(my_array, columns):
    '''(array, list) --> array
    This function returns an array containing the mean of each specific
    column, given a 2D array and a list of ints representing columns.

    >>> get_avg_all_rows(np.array([[0, 1, 2], [2, 2, 3]]), [1, 2])
    array([ 1.5,  2.5])
    '''

    data = np.mean(my_array[:,columns], axis=0)
    np.set_printoptions(suppress=True)
    return data

def get_data_in_range(my_array, column, lower_range, upper_range):
    ''' (array, int, float, float) --> array
    This function returns a 2D array, given a 2D array, a column index (int)
    and two floats for lower and upper range. the 2D array that is returned
    contains all columns and those rows whose values in the given column fall
    between the given lower and upper range values.

    >>> get_data_in_range(np.array([[2, 1], [2.5, 3], [5, 7]]), 0, 2.5, 4.0)
    array([[ 2.5,  3. ]])
    '''
    #slice array for upper range and than lower range using np.where
    data = my_array[np.where(my_array[:,column] <= upper_range)]
    new_data = data[np.where(data[:,column] >= lower_range)]
    return new_data


def get_axis_sizes(my_array, x_axis_columns, y_axis_columns):
    '''(array, int, list) --> float, float, float ,float
    This function returns four floats, given an array, an int of x-axis
    column and a list of ints of the y-axis columns. The floats that are
    returned are x_min, x_max, y_min, y_max.

    >>> get_axis_sizes(np.array([[5, 10, 19], [13, 25, 4]]), 0, [1, 2])
    (4.0, 14.0, 1.0, 28.0)
    '''

    #find min and mix values of x_axis_columns and y_axis_columns
    lowest_x = np.min(my_array[:, x_axis_columns])
    highest_x = np.max(my_array[:, x_axis_columns])

    lowest_y = np.min(my_array[:, y_axis_columns])
    highest_y = np.max(my_array[:, y_axis_columns])

    #set axis min and max values to fall below and above actual data points
    #use math.ceil and math.floor for rounding
    x_max = float(math.ceil(((highest_x - lowest_x)* 0.1) + highest_x))
    x_min = float(math.floor(lowest_x -((highest_x - lowest_x)* 0.1)))
    y_max = float(math.ceil(((highest_y - lowest_y)* 0.1) + highest_y))
    y_min = float(math.floor(lowest_y -((highest_y - lowest_y)* 0.1)))

    return x_min, x_max, y_min, y_max


def multi_plot(my_array, x_axis_columns, y_axis_columns, filename, title,
               x_label, y_label):
    '''
    This function returns a file for a scatter plot, given a 2D array, the
    index of the x-column (int), a list of ints representing the y-columns
    to be plotted, the filename (str) to write the plot to, a title (str),
    an x-label (str) and a y-label (str).
    '''

    #titles, labels and axis range
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.axis(get_axis_sizes(my_array, x_axis_columns, y_axis_columns))

    #plot
    low_x = aug_data[ : , x_axis_columns]
    low_y = aug_data[ : , y_axis_columns[0]]

    avg_x = aug_data[ : , x_axis_columns]
    avg_y = aug_data[ : , y_axis_columns[1]]

    high_x = aug_data[ : , x_axis_columns]
    high_y = aug_data[ : , y_axis_columns[2]]

    plt.plot(low_x,low_y,'bo')     #plots lows
    plt.plot(avg_x,avg_y, 'ro')    #plots averages
    plt.plot(high_x,high_y, 'go')  #plots highs
    plt.savefig(filename)

if __name__ == '__main__':
    filename = 'toronto_monthly_temps.csv'

    data = read_columns(filename, [0,1,2,3,4], ',')
    aug_data = data[np.where(data[: , 1] == 8.)]
    aug_data = aug_data[22:]

    multi_plot(aug_data, 0, [2,3,4], 'plot.png','August High, Average and \
Low Temperatures vs. Year', 'Year', 'High, Average and Low in C')
