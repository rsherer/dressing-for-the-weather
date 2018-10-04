import pandas as pd
import numpy as np
import datetime
import math


store_dct = {1: 'Marion', 2: 'Olive', 3: 'U-Village', 4: 'Lenora',
             5: 'Thomas-Boren', 6: 'Fremont', 7: 'Bellevue City Center',
             8: 'One Union', 9: 'Pioneer Square', 10: 'INTNL'}

def clean_up_dataframe(df):
    '''
    Function to clean up dataframe from csv

    Input: pandas dataframe

    Output: pandas dataframe
    '''
    df.rename(columns=lambda x: x.replace(' ', '_').lower(), inplace=True)
    df['dob'] = pd.to_datetime(df['dob']).dt.date
    df.rename(columns={'dob': 'date'}, inplace=True)
    df['ordermodename'] = (
        df['ordermodename'].replace({'In Store': 'instore',
                                     '(UnSpecified)': 'instore',
                                     'Online': 'online',
                                     'Online Pick Up': 'online',
                                     'Phone In': 'online',
                                     'Phone Order': 'online',
                                     'Take Out': 'online',
                                     'Future': 'online',
                                     'FlyBuy': 'third_party',
                                     'UberEats': 'third_party',
                                     'Uber Eats': 'third_party',
                                     'Postmates': 'third_party',
                                     'Caviar': 'third_party',
                                     'Doordash': 'third_party',
                                     'Catering': 'catering',
                                     'Wholesale': 'omit_category',
                                     '(DS Adjust)': 'omit_category',
                                     'Commissary': 'omit_category'}))
    df = df.set_index(pd.DatetimeIndex(df['date']))
    return df[['locationid', 'locationname', 'day_of_week', 'ordermodename',
               'net_sales']]


def store_filter(df, store=1):
    '''
    Function to pull sales data for a specific store
    
    Input Parameters
    ----------------
    df: pandas dataframe
        pandas dataframe converted from csv with Sales, Guests, Checks, Entrees by day
    
    store: int  
        Between 1 and 10, corresponding to a specific store as listed below:

        ['WA-001 3rd and Marion',
        'WA-002 6th and Olive',
        'WA-003 U-Village',
        'WA-004 Lenora-6th',
        'WA-005 Thomas-Boren',
        'WA-006 Fremont',
        'WA-007 - Bellevue City Center',
        'WA 008 - One Union',
        'WA-009 Pioneer Square',
        'WA-10 INTNL']
    
    Output: pandas dataframe of sales data from just a specific store
    '''
    mask = df['locationid'].apply(lambda x: x == store)
    return df[mask]


def get_instore_sales_data_by_type(df, sales_type=['instore']):
    '''
    Function to find in store sales data for a certain type of sales visit
    
    Input Parameters
    ----------------
    df: pandas dataframe
        pandas dateframe converted from csv with Sales, Guests, Checks, Entrees by day
    
    sales_type: list of str
        must be a list of string(s), to show the type of sale from the store
        from the following list of choices:
        instore = ['In Store', '(UnSpecified)'] 
        online = ['Online', 'Online Pick Up', 'Phone In', 'Phone Order', 'Take Out', 'Future']
        third_party = ['FlyBuy', 'UberEats', 'Postmates', 'Caviar','Uber Eats', 'Doordash']
        catering = ['Catering']
        omit_category = ['Wholesale', '(DS Adjust)', 'Commissary']
       
    Output: pandas dataframe with type of sales data
    '''
    df = df.loc[df['ordermodename'].isin(sales_type)]
    return df[['date', 'day_of_week','ordermodename', 'net_sales']]


def get_sales_data_by_day(df):
    '''
    Function to find total in store sales data by day.
    
    Input Parameters
    ----------------
    df: pandas dataframe
        pandas dateframe converted from csv with Sales, Guests, Checks, Entrees by day
    
    Output: pandas dataframe with type of sales data
    '''
    sales_df = df.resample('D').sum()
    sales_df = sales_df[['net_sales']]
    sales_df = sales_df.drop(sales_df[sales_df['net_sales'] < 200].index)
    combined_df = sales_df.join(df['day_of_week']).drop_duplicates()
    return combined_df

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