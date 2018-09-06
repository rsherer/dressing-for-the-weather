import numpy as np 
import pandas as pd 
import datetime
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler

class WeatherDressing():
    def __init__(self, **kwargs):
        '''
        Instatiates the WeatherDressing object.
        '''
        self.model = GradientBoostingRegressor(**kwargs)

    def fit_transform(self, X, y):
        '''
        Takes in a dataframe of features and a dataframe of targets and transforms them.
        
        Inputs: 
        _______
        X: dataframe of features
\
        Output:
        _______
        None
        '''
        scaler = StandardScaler()
        self.X = X
        self.y = y
        self.X_scaled = scaler.transform(self.X)
        self.fit_model = self.model.fit(self.X_scaled, self.y)

    def predict(self, X):
        '''
        Takes in array of features and returns predictions.
        
        Inputs:
        ______
        X: array of features

        Outputs:
        ______
        y: array of predictions
        '''
        return self.fit_model.predict(X)
    