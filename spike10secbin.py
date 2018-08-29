#!/usr/bin/python3
# Takes input from MEA-tools output, sorts into channels by 10 second bins

import os
import numpy as np
import pandas as pd
from collections import Counter

def organizeSpikes(file):
    raw_data = pd.read_csv(file)
    longest_time = raw_data.loc[raw_data['time'].idxmax()]
    longest_time_ten = int(round(longest_time.loc['time'],-1))
    
    # Establish list of electrode labels
    electrode_list = [] 
    range_list = [range(12,18),range(21,29),range(31,39),range(41,49),range(51,59),range(61,69),range(71,79),range(82,88)]
    for i in range_list:
        electrode_list.extend(i)

    # Establish times from 0 to longest 10 second bin and beginning/end times for each bin 
    beg_times = list(range(0,longest_time_ten,10))
    end_times = list(range(10,longest_time_ten+10,10))

    # Index line for times
    index_times = []

    for i,j in zip(beg_times,end_times):
            index_times.append(str(i) + '_' + str(j))

    # List of lists to transform to pd dataframe
    spike_count_lists = []
    
    # Bin values into time frames
    time_array = np.array(raw_data['time'])
    for i,j in zip(beg_times,end_times):

        # Get values that are in between whatever start/end time for that bin
        vals_in_time_indices = np.where(np.logical_and(time_array>=i,time_array<j))
        
        # Use indices to get channel number and count those values
        count_series = raw_data['electrode'].loc[vals_in_time_indices]
        
        # Counter dict object to get values for all electrodes as keys
        hist_counts = Counter(count_series)
        counts_list = []
        for k in electrode_list:
            counts_list.append(hist_counts[k])
        
        # Add counts_list for time frame to dataframe
        spike_count_lists.append(counts_list)
    
    # Df from resulting list of lists
    spike_counts_df = pd.DataFrame(spike_count_lists, index=index_times, columns=electrode_list)

    # Copy Df and filter out columns that have too many zeroes based on mode
    filtered_df = spike_counts_df.copy()
    # Get bool series of where mode of column=0, subset out everything else
    filtered_df = filtered_df[(filtered_df.mode().iloc[0]!=0).index[filtered_df.mode().iloc[0]!=0]]
    
    
    return(spike_counts_df, filtered_df)
    
    

if __name__ == "__main__":

    # Walk through files in all subdirs from directory being run from
    # Does not work with files already processed
    fileDir = os.getcwd()
    for root, dirs, files in os.walk(fileDir):
        for dir in dirs:
            os.chdir(os.path.abspath(root+"/"+dir))
            print(os.getcwd())
            for filename in os.listdir('.'):
                print(filename)
                if filename.endswith('.csv') and 'spike' not in filename and 'filtered' not in filename:
                    output_df, output_filtered_df = organizeSpikes(filename)[0], organizeSpikes(filename)[1]

                    '''
                    For separate file writing to csv

                    Print to file, make new filename
                    new_filename = "spike_counts_" + str(filename)
                    new_filtered_filename = "filtered_" + str(filename)
                    output_df.to_csv(new_filename, mode='w')
                    output_filtered_df.to_csv(new_filtered_filename, mode='w')
                    '''
                    # Write to Excel files, first sheet is filtered, second is not
                    writer = pd.ExcelWriter('analyzed_'+filename[:-4]+'.xlsx')
                    output_filtered_df.to_excel(writer,'Filtered')
                    output_df.to_excel(writer,'Spike Counts')
                    writer.save()
                    


                    