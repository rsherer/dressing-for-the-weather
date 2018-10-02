import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import date, datetime, timedelta
from dateutil.parser import parse

def get_raw_forecasts(day):
    '''
    Get raw text from weather.com's 10 day forecast, for the day passed into the function.
    
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


def get_day_of_week_and_date(string):
    '''
    Convert a string scraped from weather.com and convert it into a day of
    week and datetime date.

    Input: string

    Output: tuple of strings
    '''
    day_of_week = string[:3]
    if string[3:4] != '\n':
        day = string[3:]
    else:
        day = string[4:]
    return day_of_week, date


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
        else:
            break
    if string[0] == '-':
        raise ValueError('Negative temperatures - too cold!')
    return int(temp)