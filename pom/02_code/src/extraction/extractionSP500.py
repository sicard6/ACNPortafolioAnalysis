import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from datetime import date, timedelta

def get_time_delta(date: date , days: int, format: str = '%Y-%m-%d'):
    """this function returns a date that is days before the date passed as argument and its original day

    Args:
        date (date): date to be used as reference
        days (int): number of days for the time delta

    Returns:
        [str,str]: end date and start date in the format specified
    """
    return (date - timedelta(days=days)).strftime(format), date.strftime(format)

def format_data_to_save(data: pd.DataFrame):
    """this function formats the data to be saved in the database

    Args:
        data (pd.DataFrame): data to be formatted

    Returns:
        pd.DataFrame: data formatted to be saved
    """
    data["Date"] = data.index
    data = data[["Date", "Adj Close"]]
    data.reset_index(drop=True, inplace=True)
    data["Date"] = data["Date"].dt.date
    data["Date"] = pd.to_datetime(data["Date"])
    fecha_minima=min(data["Date"])
    data=data.set_index(data["Date"])
    del data["Date"]
    data = data.reorder_levels([0,1], axis=1)
    data.columns = data.columns.droplevel()
    return data
    
# load data from SP500

start_date,end_date = get_time_delta(date.today(), 730)

sp500 = pd.read_csv(f'../../../01_data/info/infoSP500.csv')
symbols = sp500["Symbol"].tolist()
data = yf.download(symbols, 
                      start=start_date, 
                      end=end_date, 
                      progress=True)

data = format_data_to_save(data)


data.to_csv('../../../01_data/raw/SP500_History.csv')