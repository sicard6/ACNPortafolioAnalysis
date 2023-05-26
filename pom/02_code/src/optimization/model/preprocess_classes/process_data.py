import sys, re
import pandas as pd
from datetime import datetime
#PREGUNTA: podría alguna vez leerse ambos data sets al mismo tiempo?, Usuario elige - complejizar el codigo 

class ProcessData():
        def __init__(self, parameters):
            self.parameters = parameters

        def read_local_data(self):
            """
                Reads data from a local file and returns it as a pandas DataFrame.

            Returns:
                pandas.DataFrame: The data read from the file.

            """
            print('    reading data from one drive...')
            if self.parameters['crypto']:
                 data = pd.read_csv(self.parameters['dir_crypto'])
                 data = data.dropna(axis=1)
                 
            else: 
                 data = pd.read_csv(self.parameters['dir_sp500'])
                 data = data.dropna(axis=1)
                 data = data.iloc[:409]
                 data.to_csv('data.csv')
            return data
        
        @staticmethod
        def get_returns(data):
            """Calculates the returns of a DataFrame where the columns are the assets.

            Attributes
            ----------
                df (pandas.DataFrame): The DataFrame containing the assets data.

            arameters
            ----------
                pandas.DataFrame: A DataFrame containing the returns of the assets, with the date column preserved.
            """
            print('    getting returns...')
            date = data.iloc[:, 0]
            date = pd.to_datetime(date.drop(index = 0))
            returns = data.iloc[:, 1:].pct_change()
            returns = returns.drop(index=0)
            returns = returns.set_index(date)
            returns.to_csv('returns.csv')
            return returns
        
        @staticmethod            
        def expected_returns(data):
            """Calculates the expected returns for each asset in a DataFrame.

            Attributes
            ----------
                df (pandas.DataFrame): The DataFrame containing the asset data.

            Parameters
            ----------
                pandas.Series: A Series containing the expected returns for each asset.
            """
            print('    getting returns mean...')
            mean_returns = data.mean()
            return mean_returns

        def process_data(self, data):
            """
                Processes the input data and returns a dictionary with the results.

            Parameters:
                data (pandas.DataFrame): The input data to be processed.

            Returns:
                dict: A dictionary with the following keys:
                    - 'returns': The asset returns.
                    - 'returns_mean': The expected asset returns.
                    - 'coef': The coefficient used in the processing.
            """        
            returns = ProcessData.get_returns(data)
            returns_mean = ProcessData.expected_returns(returns)
            coefficient = self.parameters['coefficient']
            atri_data = {
                'returns': returns,
                'returns_mean': returns_mean,
                'coef': coefficient
             } 
            return atri_data

        def create_attributes(self, atri_data):
            """
                Creates attributes on the instance based on the keys and values in the provided dictionary.

            Parameters:
                 atri_data (dict): A dictionary with the keys and values to be set as attributes.

            """
            print('    creating attributes...')
            for key, value in atri_data.items():
                 setattr(self, key, value)
                     


        
        
