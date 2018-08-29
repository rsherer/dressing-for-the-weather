import pandas as pd
import numpy as np
import datetime

def get_date_and_weather_from_metar(filename):
    '''
    Function to use METAR csv and convert it to a df with a day and temperature column. 
    The daily temperature is taken at 10:53a, so that it can be used for 11a, when the lunch rush starts.
    
    Input: pandas dataframe
    
    Output: pandas dataframe
    '''
    # download raw data
    raw_data = pd.read_csv(filename)
    
    # get temperature at 10:53a, as this is right before lunch rush
    mask = raw_data['valid'].apply(lambda x: x[-5:] == '10:53')
    df = raw_data[mask]
    
    # remove spaces from column names, and rename date and temperature columns
    df.rename(columns=lambda x: x.replace(' ', '').lower(), inplace=True)
    df.rename(columns={'valid':'date', 'tmpf':'temp'}, inplace=True)
    
    # create series for the features to be included in modeling
    # cast temp column to floats
    temp = df['temp'].apply(float)
    
    # cast date column to datetime series
    date = pd.to_datetime(df['date']).dt.date

    # cast values in p01i to float
    raw_prec = df['p01i'].apply(float)
    prec = raw_prec.apply(lambda x: True if (x > 0.03) else False)

    # convert the sky cover entries into sunny or not sunny
    sky_coverage = ['skyc1', 'skyc2', 'skyc3', 'skyc4']
    sky_agg = df[sky_coverage].values.tolist()
    sky_reduce = [['cloudy' if (('BKN' in element) or ('OVC' in element)) else 'clear'
                    for element in row] for row in sky_agg]
    sunny = pd.Series([False if 'cloudy' in row else True for row in sky_reduce])
    sunny.index = date.index

    # concatenate the series, name the columns
    cleaned_df = pd.concat([date, temp, prec, sunny], axis=1)
    cleaned_df.columns = ['date', 'temp', 'prec', 'sunny']

    # make the date time series column the index for join with sales data
    cleaned_df = cleaned_df.set_index(pd.DatetimeIndex(cleaned_df['date']))
    return cleaned_df[['temp', 'prec', 'sunny']]