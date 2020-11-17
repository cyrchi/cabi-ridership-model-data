# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 12:41:25 2020

@author: Cyrus Chimento

Purpose: Gather Capital Bikeshare ridership data for GEOG654 Spatial
         Modeling final project. This script extracts csv files of 
         bikeshare trip data, summarizes ridership by station, and 
         creates a new file of monthly ridership data, with mean 
         ridership and natural log mean ridership for each month.
         Writes the results to a new csv file.

References:

1. https://www.newbedev.com/python/howto/how-to-iterate-over-files-in-a-given-directory/
2. https://stackoverflow.com/questions/8858008/how-to-move-a-file
3. https://docs.python.org/3/library/zipfile.html
4. https://www.geeksforgeeks.org/python-read-csv-using-pandas-read_csv/
5. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.join.html
6. https://datatofish.com/export-dataframe-to-csv/
7. https://stackoverflow.com/questions/19384532/get-statistics-for-each-group-such-as-count-mean-etc-using-pandas-groupby
8. https://cmdlinetips.com/2020/04/how-to-get-column-names-as-list-in-pandas/#:~:text=We%20can%20get%20the%20names,using%20Pandas%20method%20%E2%80%9Ccolumns%E2%80%9D.&text=Pandas'%20columns%20method%20returns%20the%20names%20as%20Pandas%20Index%20object.&text=We%20can%20convert%20the%20Pandas,using%20the%20tolist()%20method.&text=And%20now%20we%20have%20Pandas'%20dataframe%20column%20names%20as%20a%20list.
9. https://www.geeksforgeeks.org/log-and-natural-logarithmic-value-of-a-column-in-pandas-python/
10. https://www.kite.com/python/answers/how-to-find-the-mean-of-a-pandas-dataframe-column-in-python#:~:text=To%20calculate%20the%20mean%20of,a%20list%20of%20DataFrame%20columns.

"""

import zipfile
import os
import pandas
import numpy

directory = r"C:\Users\cyrus\Desktop\GIS\UMD\GEOG654_Spatial_Modeling\Final\Source_Data\CB_Ridership"
zipfiles = os.listdir(directory) # create a list of zipfiles in the directory

for file in zipfiles:
    if file[-12:] == "tripdata.zip": # only get the correct files
        zipReference = zipfile.ZipFile(directory + "\\" + file, 'r') # read the zip file to an object
        zipReference.extractall(directory + "\\CB_Ridership_Monthly_CSV") # extract the zipfile
    
# new working directory with CSV files for each month
workingDirectory = r"C:\Users\cyrus\Desktop\GIS\UMD\GEOG654_Spatial_Modeling\Final\Source_Data\CB_Ridership\CB_Ridership_Monthly_CSV"
csvFiles = os.listdir(workingDirectory) # create a list of csv files in the directory
stationCountsPath = directory + "\\StationCounts.csv" # path to the output csv
counter = 0
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

# loop through each month's ridership data file
for file in csvFiles:
    if file[-12:] == "tripdata.csv": # only get the correct files
        # read csv into a dataframe
        df = pandas.read_csv(workingDirectory + "\\" + file)
        if counter == 0: # if first file
            # count the number of trips per station into a new dataframe
            dfCounts = df.groupby("Start station number").size().reset_index(name=months[counter] + "_COUNT")
        if counter > 0:
            # count the number of trips per station into a new dataframe
            summary = df.groupby("Start station number").size().reset_index(name=months[counter] + "_COUNT")
            # join to the first dataframe based on station number
            dfCounts = dfCounts.join(summary.set_index("Start station number"), on="Start station number")
        counter += 1 # iterate the counter

columnList = dfCounts.columns.tolist() # get a list of the columns

# find the average monthly rides per station (row averages)
dfCounts["AVE_RDRSHP"] = dfCounts[columnList[2:]].mean(axis=1)
# find the natural log of average monthly rides
dfCounts["LOG_RDRSHP"] = numpy.log(dfCounts["AVE_RDRSHP"])

# write dataframe to output csv
dfCounts.to_csv(stationCountsPath)

