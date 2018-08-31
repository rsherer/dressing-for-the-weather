import numpy as numpy
import pandas as pd
import datetime

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