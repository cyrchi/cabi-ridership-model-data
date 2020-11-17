# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 13:40:05 2020

@author: Cyrus Chimento

Purpose: Collect census data for the GEOG654 Spatial Modeling final project.
         This script uses the cenpy module to collect ACS data from different
         tables at the tract level, calculate a few new fields using these data
         and write the geopandas dataframe to a shapefile. There is also sample
         code for plotting a map of one of the census variables to double check.

References:

1. https://towardsdatascience.com/my-python-pandas-cheat-sheet-746b11e44368
2. https://enviroatlas.epa.gov/enviroatlas/DataFactSheets/pdf/Supplemental/NumberofHouseholdsWithZeroVehicles.pdf
3. https://censusreporter.org/topics/table-codes/
4. https://www.azavea.com/blog/2015/08/25/how-to-get-census-data-for-maps-in-5-steps/
5. https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
6. https://nbviewer.jupyter.org/github/ljwolf/cenpy/blob/master/notebooks/product-api.ipynb?flush_cache=true
7. https://towardsdatascience.com/scraping-us-census-data-via-cenpy-9aeab12c877e
8. https://geopandas.org/reference.html#geopandas.GeoDataFrame.to_file
9. https://geopandas.org/io.html

"""

# import modules
from cenpy import products
import geopandas
import matplotlib.pyplot as plot

# get census data
censusTracts = products.ACS(2017).from_csa(
        'Washington-Arlington-Alexandria',
        level='tract',
        variables= [
            'B01003_001E', # total population
            'B19013_001E', # household median income last 12 months
            'B02001_001E', # race: total
            'B02001_002E', # white
            'B08301_001E', # means of transportation to work: total
            'B08301_010E', # transit
            'B08301_019E', # walking
            'B08301_018E', # bicycling
            'B15003_001E', # educational attainment: total
            'B15003_022E', # bachelor's degree
            'B15003_023E', # master's degree
            'B15003_024E', # professional degree
            'B15003_025E', # doctoral degree
            'C24050_006E'  # industry by occupation for the civilian population: retail trade
            ]
        )

# calculate percentage of nonwhite residents
censusTracts['P_NOWHITE'] = (censusTracts['B02001_001E'] - censusTracts['B02001_002E']) / censusTracts['B02001_001E']
# calculate percentage alternative commuters
censusTracts['P_ALT_COMMUT'] = (censusTracts['B08301_010E'] + censusTracts['B08301_019E'] + censusTracts['B08301_018E']) / censusTracts['B08301_001E']
# calculate percentage bachelor degree
censusTracts['P_BACHELORS'] = (censusTracts['B15003_022E'] + censusTracts['B15003_023E'] + censusTracts['B15003_024E'] + censusTracts['B15003_025E']) / censusTracts['B15003_001E']

# legend for the plot
legendProperties = {'label': "Percent of 2017 Population",'orientation': "vertical"}

# plot
censusTracts.plot(
    column='P_BACHELORS', 
    cmap='OrRd', 
    edgecolor="black",
    legend=True,
    legend_kwds=legendProperties
    )

plot.title('Bachelor\'s Degree')
    
# write to a shapefile
censusTracts.to_file(r"C:\Users\cyrus\Desktop\GIS\UMD\GEOG654_Spatial_Modeling\Final\Source_Data\CensusData_2017\CensusData_2017.shp")



