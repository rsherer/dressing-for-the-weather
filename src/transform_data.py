import numpy as numpy
import pandas as pd
import datetime
import math

def transform(sales_df, weather_df):
    '''
    Combines sales date with weather data to fit models and get forecasts and predictions

    Input: Cleaned sales pandas data frame, cleaned weather pandas data frame

    Output: Pandas data frame
    '''
    # combine the sales and weather dataframes
    combined_df = sales_df.merge(weather_df, left_index=True, right_index=True)
    
    # create the sine and cosine vectors for each day of the year
    sin_vect = pd.Series(combined_df.index).apply(lambda x: assign_sine_vector(x))
    cos_vect = pd.Series(combined_df.index).apply(lambda x: assign_cosine_vector(x))
    sin_vect.index = days.index
    cos_vect.index = days.index

    # add sine vector series to the dataframe
    combo_with_sin_df = pd.concat([combined_df, sin_vect], axis=1)
    combo_with_sin_df.rename(columns={date: sin_vect}, inplace=True)

    # add cosine vector series to the dataframe
    combo_with_cos_df = pd.concat([combo_with_sin_df, cos_vect], axis=1)
    combo_with_cos_df.rename(columns={date: cos_vect}, inplace=True)

    # create dummies out of the days of the week, and add dummies to the dataframe
    day_of_week = combined_df['day_of_week']
    days = pd.get_dummies(day_of_week)
    combo_dummy_days_df = pd.concat([combo_data, days], axis=1)
    combo_dummy_days_df = combo_dummy_days_df.drop(columns=['day_of_week'], axis=1)

    # need to add columns for rolling means for trailing 1, 2, 3, and 4 week equivalents


def date_to_nth_day(date):
    '''
    Function to convert a datetime day to a number
    
    Input: datetime date
    
    Output: int
    '''
    date = pd.to_datetime(date)
    new_year_day = pd.Timestamp(year=date.year, month=1, day=1)
    return (date - new_year_day).days + 1


def assign_sine_vector(day):
    '''
    Function will create a sine vector based on the day of the year (d) such that 
    vector = sin((2 * pi * d) / 365
    
    Input: date
    
    Output: sine vector
    '''
    return math.sin((2 * math.pi * date_to_nth_day(day)) / 365)


def assign_cosine_vector(day):
    '''
    Function will create a cosine vector based on the day of the year (d) such that 
    vector = cos((2 * pi * d) / 365
    
    Input: date
    
    Output: cosine vector
    '''
    return math.cos((2 * math.pi * date_to_nth_day(day)) / 365)