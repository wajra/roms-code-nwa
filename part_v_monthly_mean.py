from part_iii_mean_o2 import get_file_index
import os
import re
import glob
from pandas import DataFrame
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import pyroms
import pyroms_toolbox
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma


# Create a netCDF4 file with monthly averages for a certain date
# Haul date is a datetime object
def create_monthly_mean(haul_date):
    print(type(haul_date))
    haul_date = pd.to_datetime(haul_date)
    print(type(haul_date))
    daily_index = get_file_index()
    start_date = haul_date - relativedelta(months=1)
    end_date = haul_date + relativedelta(months=2)
    print(start_date)
    print(end_date)
    file_paths = daily_index.loc[start_date:end_date, 'file_path'].tolist()
    # First let's try for O2
    o2_list = []
    for file_path in file_paths:
        daily_o2 = pyroms.utility.get_nc_var('o2', file_path)[0]
        # Bottom O2
        o2_list.append(daily_o2[0])
    # Get the mean O2 for bottom layer
    mean_o2 = np.mean(ma.array(o2_list), axis=0)
    print(mean_o2.shape)
    # Write this file as 'o2_bottom_monthly_average'
    print('Success')


# A method where we enter a date, and a pair of coordinates
# then we return the mean [O2] for the sea bottom and surface
def get_o2_mean(haul_date, haul_lon, haul_lat):
    # Timedelta object of 30 days
    td_30 = timedelta(days=30)
    # Haul date is a string that we convert to a datetime object
    haul_date_dt = datetime.datetime.strptime(haul_date, '%Y-%m-%d')
    print('OK')


# A method where we enter a date, and a pair of coordinates
# then we return the mean [O2] for the sea bottom and surface
def get_small_zplk_mean(haul_date, haul_lon, haul_lat):
    return None


if __name__ == '__main__':
    daily_index = get_file_index()
    # Set up the grid for later plotting
    grd = pyroms.grid.get_ROMS_grid('NWA')
    lon = grd.hgrid.lon_rho
    lat = grd.hgrid.lat_rho
    # Call 'get_o2_mean'
    get_o2_mean('2016-05-25', 97.5, 82.3)
    # Read the data file containing the hauls
    catch_hauls_df = pd.read_csv('data/catch_data_hauls_merge.csv')
    print(catch_hauls_df.head(10))
    # Add a day column with default set to 1
    catch_hauls_df['day'] = 1
    # Create a 'haul_date' column by using the 'year', 'month', and 'day' columns
    catch_hauls_df['haul_date'] = pd.to_datetime(catch_hauls_df[['year', 'month', 'day']])
    print('How does the haul date column look')
    # Print out the relevant columns
    print(catch_hauls_df[['haul_date', 'year', 'month', 'day']].head(10))
    # Filter the data from or after 1980-01-01
    mask_post_1980 = catch_hauls_df['haul_date'] >= '1980-01-01'
    catch_hauls_df = catch_hauls_df[mask_post_1980]
    print("Print out the final dataframe")
    print(catch_hauls_df)
    # Sort the dataframe by 'haul_date'
    catch_hauls_df = catch_hauls_df.sort_values(by='haul_date')
    print(catch_hauls_df)
    # OK. So this works
    # Now on to the fun stuff
    catch_hauls_df.reset_index(inplace=True)
    print(catch_hauls_df)
    # Let's just get the seasonal range for a certain date
    sample_haul_date = catch_hauls_df.loc[0, 'haul_date']
    # print(sample_haul_date)
    sample_start_date = sample_haul_date - relativedelta(months=1)
    sample_end_date = sample_haul_date + relativedelta(months=2)
    # print(sample_haul_date - relativedelta(months=1))
    # print(sample_haul_date + relativedelta(months=2))
    # Testing if the file index is working
    # print(daily_index.head(10))
    # print(daily_index['2004-01-01']['file_path'])
    print(daily_index.loc[sample_start_date: sample_end_date, 'file_path'])
    print(daily_index.loc[sample_start_date: sample_end_date, 'file_path'].tolist())
    # create_monthly_mean()
    # First a list of unique dates in the 'haul_date' column
    print(type(catch_hauls_df['haul_date'].unique()[0]))
    print(len(catch_hauls_df['haul_date'].unique()))
    # OK. Let's take the 10th unique value and stick it in there
    test_date_1 = catch_hauls_df['haul_date'].unique()[10]
    create_monthly_mean(test_date_1)

