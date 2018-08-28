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
    raw_data = pd.read_csv(filename)
    mask = raw_data['valid'].apply(lambda x: x[-5:] == '10:53')
    df = raw_data[mask]
    df.columns = [x.strip().replace(' ', '_').lower() for x in df.columns]
    df.rename(columns={'valid':'date'}, inplace=True)
    temp = df['tmpf'].apply(float)
    date = pd.to_datetime(df['date']).dt.date
    df = pd.concat([date, temp], axis=1)
    return df