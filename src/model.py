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
        self.model = GradientBoostingRegressor(max_depth=3, max_features='log2', min_samples_leaf=4, n_estimators=300)

    def fit_transform(self, X, y):
        '''
        Takes in a dataframe of features and a dataframe of targets and transforms them.
        
        Inputs: 
        _______
        X: dataframe of features\
        
        Output:
        _______
        None
        '''
        self.X = X
        self.y = y
        scaler = StandardScaler()
        self.X_scaled = scaler.fit_transform(self.X)
        self.fit_model = self.model.fit(self.X_scaled, self.y)
        return self.fit_model

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
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        return self.fit_model.predict(X_scaled)

    
    # def scaled(self, X):
    #     scaler = StandardScaler()
    #     return scaler.fit_transform(X)
    