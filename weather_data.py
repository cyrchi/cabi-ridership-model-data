# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 17:00:15 2020

@author: Cyrus Chimento

Purpose: Reconfigure precipitation data for GEOG654 Spatial Modeling
         final project. This script cleans weather data and calculates
         the number of days per month with precipitation greater
         than or equal to 0.01 at each station, then calculates an annual
         average for each station, and writes the results to a csv.

References:

1. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html
2. https://www.interviewqs.com/ddi_code_snippets/extract_month_year_pandas
3. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_csv.html

"""

import pandas

# read in the weather data 
df = pandas.read_csv(r"C:\Users\cyrus\Desktop\GIS\UMD\GEOG654_Spatial_Modeling\Final\Source_Data\WeatherData.csv")

df['PRCP'] = df['PRCP'].fillna(0) # replace null values with zero
df["month"] = pandas.DatetimeIndex(df['DATE']).month # add a month column and populate using date

# count number of days per month where precipitation is over 0.01in, and group by station, then month
precDays = df.loc[df['PRCP'] >= 0.01].groupby(["STATION", "month"]).size() # series
averagePrecDays = precDays.mean(level="STATION") # find the mean number of precipitation days per month at each station

# write to csv
averagePrecDays.to_csv(r"C:\Users\cyrus\Desktop\GIS\UMD\GEOG654_Spatial_Modeling\Final\Source_Data\AvePrecipitationbyStation.csv")

