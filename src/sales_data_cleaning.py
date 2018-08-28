import pandas as pd
import numpy as np
import datetime

def clean_up_dataframe(df):
    '''
    Function to clean up dataframe from csv
    
    Input: pandas dataframe
    
    Output: pandas dataframe
    '''
    df.rename(columns=lambda x: x.replace(' ', '_').lower(), inplace=True)
    df['dob'] = pd.to_datetime(df['dob']).dt.date
    df.rename(columns={'dob':'date'}, inplace=True)
    df['ordermodename'] = df['ordermodename'].replace({'In Store': 'instore',
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
                                                             'Commissary': 'omit_category'})
    df = df.set_index(pd.DatetimeIndex(df['date']))
    return df[['locationid', 'locationname','day_of_week', 'ordermodename','net_sales']]


def store_filter(df, store=1):
    '''
    Function to pull sales data for a specific store
    
    Input Parameters
    ----------------
    df: pandas dataframe
        pandas dataframe converted from csv with Sales, Guests, Checks, Entrees by day
    
    store: int, default to Marion store, id 1
        Specific store name from following list of choices: 

        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 111] 
        
        which corresponds to:
        
        ['WA-001 3rd and Marion', 'WA-002 6th and Olive',
       'WA-003 U-Village', 'WA-004 Lenora-6th', 'WA-005 Thomas-Boren',
       'WA-006 Fremont', 'WA-007 - Bellevue City Center',
       'WA 008 - One Union', 'WA-009 Pioneer Square', 'WA-10 INTNL',
       'WA-Commissary']
    
    Output: pandas dataframe of sales data from just a specific store
    '''
    mask = df['locationid'].apply(lambda x: x == store)
    return df[mask]


def get_instore_sales_data(df, sales_type=['(UnSpecified)', 'In Store']):
    '''
    Function to find in store sales data for a certain type of sales visit
    
    Input Parameters
    ----------------
    df: pandas dataframe
        pandas dateframe converted from csv with Sales, Guests, Checks, Entrees by day
    
    sales_type: list of str
        must be a list of string(s), to show the type of sale from the store from the following list of choices:
        ['(UnSpecified)', 'Online', 'Online Pick Up', 'Postmates',
       'Uber Eats', 'UberEats', 'Catering', 'Caviar', 'Future',
       'Phone In', 'In Store', 'Phone Order', 'Take Out', 'Doordash']
       
    Output: pandas dataframe with type of sales data
    '''
    return df.loc[df['ordermodename'].isin(sales_type)]


def date_to_nth_day(date):
    '''
    Function to convert a datetime day to a number
    
    Input: datetime date
    
    Output: int
    '''
    date = pd.to_datetime(date)
    new_year_day = pd.Timestamp(year=date.year, month=1, day=1)
    return (date - new_year_day).days + 1