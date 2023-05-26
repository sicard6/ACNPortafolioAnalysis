import pandas as pd
from calendar import monthrange
import os, sys

#Acá deben ir las funciones donde se filtren los activos no deseados 
from src.optimization.model.preprocess_classes.process_data import ProcessData
from src.optimization.model.preprocess_classes.pyomo_data import PyomoData

def preprocess_data(parameters):
    """
        Preprocesses the input data for Pyomo optimization models.

    Parameters:
        parameters (dict): A dictionary containing the parameters for data preprocessing.

    Returns:
        ProcessData: A ProcessData object containing the preprocessed data.

    """
    processed_data = ProcessData(parameters) 
    data = processed_data.read_local_data()       
    atri_data = processed_data.process_data(data)  
    processed_data.create_attributes(atri_data)
    return processed_data

def data_to_pyomo(processed_data):
    """
        Converts processed data to Pyomo input data.

    Parameters:
        processed_data (pandas.DataFrame or pandas.Series): The processed data to be converted.

    Returns:
        PyomoData: A PyomoData object containing the input data.

    """
    pyomo_data = PyomoData(processed_data)
    return pyomo_data  


def get_next_period(returns, mean):
    """
    Generates the returns for the next period.

    Parameters:
        returns (pandas.DataFrame): A DataFrame containing the returns data.
        mean (pandas.Series): A Series containing the expected returns for each asset.

    Returns:
        pandas.DataFrame: A DataFrame containing the returns for the next period.

    """
    returns = returns.drop(returns.index[0])
    returns = pd.concat([returns, pd.DataFrame([mean], columns=returns.columns)], axis=0)
    return returns

#Pregunta: esta funcion mejor acá o en process_data
def data_periodicity(data, parameters):
    df_periodicity= data.resample(parameters['periodicity']).last()
    return df_periodicity

