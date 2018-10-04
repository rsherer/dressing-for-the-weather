import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import date, datetime, timedelta
from dateutil.parser import parse

def get_raw_forecasts(day):
    '''
    Get raw text from weather.com's 10 day forecast, for the day passed into the function.
    Day = 1 will be today.
    
    Input: int
    Day between 1 and 15, representing the day of the desired forecast.
    
    Output: list of strings
    Raw text for the day chosen, in the following order:
        [daymonth date, weather forecast, hi/lo temp, % chance precipitation, 
         wind speed and direction, humidity]
    '''
    if day > 15:
        raise ValueError('the variable day must be an integer between 1 and 15')
    page_link = 'https://weather.com/weather/tenday/l/USWA0396:1:US'
    page_response = requests.get(page_link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    
    web_predictions = []
    for i in range(0,105):
        predictions = page_content.find_all('td')[i].text
        web_predictions.append(predictions)
    return web_predictions[(day*7 - 6):(day*7)]


def get_day_of_week(string):
    '''
    Convert a string scraped from weather.com and convert it into a day of
    week.

    Input: string

    Output: string
    '''
    day_of_week = string[0][:3]
    return day_of_week


def get_date(string):
    '''
    Convert a string scraped from weather.com and convert it into a datetime date.

    Input: string

    Output: datetime date
    '''
    if string[3:4] != '\n':
        date = string[3:]
    else:
        date = string[4:]
    return parse(date)


def get_hi_temperature(string):
    '''
    Take the hi/lo string from weather.com and convert to an integer of the
    hi temperature.

    Input: string

    Output: int
    '''
    numbers = str([num for num in range(0,10)])
    temp = ''
    for char in string:
        if char in numbers:
            temp += char
        else:
            break
    return int(temp)


def get_low_temperature(string):
    '''
    Take the hi/lo string from weather.com and convert to an integer of the
    low temperature.

    Input: string

    Output: int
    '''
    
    numbers = [str(num) for num in range(0,10)]
    temp = ''
    for char in reversed(string[:-1]):
        if char in numbers:
            temp = char + temp
        elif char == '-':
            raise ValueError('Negative temperatures - too cold!')
        else:
            break
    return int(temp)


def precipitation(string):
    '''
    Convert string scraped from weather.com to True or False if precipitation that day

    Input: string

    Output: boolean
    '''
    prec = int(string[:-1])
    if prec >= 40:
        return True
    else:
        return False


def sunny(string):
    '''
    Convert string scraped from weather.com to True or False depending on sunny or not.
    Sunny is considered if the forecast is Sunny, mostly Sunny, or Partly Cloudy
    
    Input: string
    
    Output: boolean
    '''
    sunny_lst = ['Sunny'.lower(), 'Mostly Sunny'.lower(), 'Partly Cloudy'.lower()]
    if string.lower() in sunny_lst:
        return True
    else:
        return False


def check_day_of_week(day, dow='Fri'):
    '''
    Function to get a 1 for a matching day of week, and zero otherwise.
    
    Inputs: str, str
    
    Output: int
    '''
    if day == dow:
        return 1
    else:
        return 0
        
        
def make_weather_dressing_prediction_components(day_scrape: list):
    '''
    Aggregate all forecast components necessary for the array that is used for the predict
    function in the WeatherDressing. The list of strings that is scraped from 
    get_raw_forecasts() is the list of strings that should be used for day_scrape.
    
    Input: list
    
    Output: list
    '''
    pred = [get_hi_temperature(day_scrape[2]),
           precipitation(day_scrape[3]),
           sunny(day_scrape[1]),
           assign_sine_vector(get_date(day_scrape[0])),
           assign_cosine_vector(get_date(day_scrape[0])),
           check_day_of_week(get_day_of_week(day_scrape), 'Fri'),
           check_day_of_week(get_day_of_week(day_scrape), 'Mon'),
           check_day_of_week(get_day_of_week(day_scrape), 'Thu'),
           check_day_of_week(get_day_of_week(day_scrape), 'Tue'),
           check_day_of_week(get_day_of_week(day_scrape), 'Sat'),
           check_day_of_week(get_day_of_week(day_scrape), 'Sun'),
           check_day_of_week(get_day_of_week(day_scrape), 'Wed')]
    return pred