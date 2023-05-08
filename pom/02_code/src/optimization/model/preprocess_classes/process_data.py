import sys, re
import pandas as pd
#PREGUNTA: podría alguna vez leerse ambos data sets al mismo tiempo?, Usuario elige - complejizar el codigo 

class ProcessData():
        def __init__(self, parameters):
            self.parameters = parameters

        def read_local_data(self):
            print('    reading data from one drive...')
            if self.parameters['crypto']:
                 data = pd.read_csv(self.parameters['dir_crypto'])
            else: 
                 data = pd.read_csv(self.parameters['dir_sp500'])
            return data
        
        @staticmethod
        def get_returns(data):
            """Calculates the returns of a DataFrame where the columns are the assets.

            Args:
                df (pandas.DataFrame): The DataFrame containing the assets data.

            Returns:
                pandas.DataFrame: A DataFrame containing the returns of the assets, with the date column preserved.
            """
            date = data.iloc[:, 0]
            date = date.drop(index=0)
            returns = data.iloc[:, 1:].pct_change()
            returns = returns.drop(index=0)
            returns = returns.set_index(date)
            return returns
        
        @staticmethod            
        def expected_returns(data):
            """Calculates the expected returns for each asset in a DataFrame.

            Args:
                df (pandas.DataFrame): The DataFrame containing the asset data.

            Returns:
                pandas.Series: A Series containing the expected returns for each asset.
            """
            mean_returns = data.mean()
            return mean_returns

        def process_data(self, data):
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
            for key, value in atri_data.items():
                 setattr(self, key, value)
                     


        
        
