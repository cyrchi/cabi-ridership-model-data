# Capital Bikeshare Ridership Model

I used the above scripts to collect and engineer data to create Ordinary Least Squares (OLS) regression and Geographically Weighted Regression (GWR) models for Capital Bikeshare ridership in the Washington, DC region. This replicated part of a study ([Station-Level Forecasting of Bikesharing Ridership: Station Network Effects in Three U.S. Systems](https://journals.sagepub.com/doi/10.3141/2387-06)) to identify changes after 10 years of system operation.

- **bikeshare_data.py**: This script extracts csv files of  bikeshare trip data, summarizes ridership by station, and creates a new file of monthly ridership data, with mean ridership and natural log mean ridership for each month. Writes the results to a new csv file.
- **census_data.py**: This script uses the cenpy module to collect ACS data from different tables at the tract level, calculate a few new fields using these data and write the geopandas dataframe to a shapefile. There is also sample code for plotting a map of one of the census variables to double check.
- **weather_data.py**: This script cleans weather data and calculates the number of days per month with precipitation greater than or equal to 0.01 at each station, then calculates an annual average for each station, and writes the results to a csv.
