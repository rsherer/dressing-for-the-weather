import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta

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