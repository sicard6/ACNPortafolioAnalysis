import requests
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
from datetime import datetime, timedelta
import json

# Cargar el archivo JSON de la ruta especificada
with open('pom/01_data/parameters.json') as f:
    config = json.load(f)

########################################################################################
############################# Codigo para Google Colab #################################

import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from datetime import date, timedelta
from IPython.display import clear_output

def format_data_to_save(data: pd.DataFrame):
    """
    Esta función formatea los datos para ser guardados en la base de datos.

    Args:
        data (pd.DataFrame): datos a ser formateados

    Returns:
        pd.DataFrame: datos formateados para ser guardados
    """
    data["Date"] = data.index
    data = data[["Date", "Close"]]
    data.reset_index(drop=True, inplace=True)
    data["Date"] = data["Date"].dt.date
    data["Date"] = pd.to_datetime(data["Date"])
    fecha_minima = min(data["Date"])
    data = data.set_index(data["Date"])
    del data["Date"]
    data = data.reorder_levels([0, 1], axis=1)
    data.columns = data.columns.droplevel()
    return data

def get_time_delta(date: date, days: int, format: str = '%Y-%m-%d'):
    """
    Esta función devuelve una fecha que es 'days' días antes de la fecha pasada como argumento y su día original.

    Args:
        date (date): fecha a ser utilizada como referencia
        days (int): número de días para el intervalo de tiempo

    Returns:
        [str, str]: fecha final y fecha inicial en el formato especificado
    """
    return (date - timedelta(days=days)).strftime(format), date.strftime(format)

def extract_sp500_data(num_symbols=None,history_of_years = 5):
    """
    Esta función extrae datos del S&P 500, procesa los datos y guarda los resultados en archivos CSV.
    
    Args:
        num_symbols (int, optional): número de símbolos de la lista S&P 500 a utilizar. Por defecto es None,
        por lo que trae todos los elementos posibles de la lista.
    """
    # Leer lista de las empresas del SP500
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    sp500_info = table[0]

    # Convertirlo CSV's
    sp500_info.to_csv('S&P500-Info.csv')
    sp500_info.to_csv("S&P500-Symbols.csv", columns=['Symbol'])
    sp500_info.to_csv("S&P500-Sector.csv", columns=['GICS Sector'])

    # Variable de los símbolos de las empresas (Tickers)
    symbols = sp500_info["Symbol"].tolist()

    # Eliminar "BF.B" y "BRK.B" de la lista de símbolos
    symbols.remove("BF.B")
    symbols.remove("BRK.B")
    
    if num_symbols is not None:
        symbols = symbols[:num_symbols]

    # Historial de años a investigar
    start_date, end_date = get_time_delta(date.today(), 365 * history_of_years)

    # Dataframe con Data 100% Cruda y que se guarda en un CSV
    df_raw_data = yf.download(symbols,
                              start=start_date,
                              end=end_date,
                              progress=False)

    # Guardar la Raw Data en CSV
    df_raw_data.to_csv('S&P500-Raw-Data.csv')

    # Procesar y guardar datos
    df_curated_data = format_data_to_save(df_raw_data)
    df_curated_data.to_csv('S&P500-Curated-Data.csv')

    df_curated_data_YS = df_curated_data.resample("YS").last()
    df_curated_data_YS.to_csv('S&P500-Curated-Data_YS.csv')
    df_curated_data_QS = df_curated_data.resample("QS").last()
    df_curated_data_QS.to_csv('S&P500-Curated-Data_QS.csv')
    df_curated_data_MS = df_curated_data.resample("MS").last()
    df_curated_data_MS.to_csv('S&P500-Curated-Data_MS.csv')

def extract_crypto_data(crypto_symbols, history_of_years=5):
    """
    Esta función extrae datos de criptomonedas, procesa los datos y guarda los resultados en archivos CSV.
    
    Args:
        crypto_symbols (str): Símbolos de criptomonedas separados por espacios.
        history_of_years (int, optional): Número de años de datos históricos a obtener. Por defecto es 5.
    """
    # Convertir la cadena de símbolos en una lista
    symbols = crypto_symbols.split()

    # Definir fechas de inicio y fin
    start_date, end_date = get_time_delta(date.today(), 365 * history_of_years)

    # Descargar datos crudos
    df_raw_data = yf.download(symbols,
                              start=start_date,
                              end=end_date,
                              progress=False)

    # Guardar la Raw Data en CSV
    df_raw_data.to_csv('Crypto-Raw-Data.csv')

    # Procesar y guardar datos
    df_curated_data = format_data_to_save(df_raw_data)
    df_curated_data.to_csv('Crypto-Curated-Data.csv')

    df_curated_data_YS = df_curated_data.resample("YS").last()
    df_curated_data_YS.to_csv('Crypto-Curated-Data_YS.csv')
    df_curated_data_QS = df_curated_data.resample("QS").last()
    df_curated_data_QS.to_csv('Crypto-Curated-Data_QS.csv')
    df_curated_data_MS = df_curated_data.resample("MS").last()
    df_curated_data_MS.to_csv('Crypto-Curated-Data_MS.csv')


## Funciones descargando informacion
extract_sp500_data()

Crypto_Symbols = "BTC-USD ETH-USD XRP-USD BNB-USD LTC-USD"
extract_crypto_data(Crypto_Symbols)


########################################################################################
############################# Codigo para Financial Modeling Prep #################################

"""
# Suprimir advertencias de solicitudes no seguras
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_time_delta(date: datetime, days: int, format: str = '%Y-%m-%d'):
    """ """Esta función devuelve una fecha que está 'days' días antes de la fecha pasada como argumento y su fecha original.

    Args:
        date (datetime): fecha para ser utilizada como referencia
        days (int): número de días para el intervalo de tiempo

    Returns:
        (str, str): fecha final y fecha de inicio en el formato especificado
    """"""
    return (date - timedelta(days=days)).strftime(format), date.strftime(format)

def get_stock_data(symbol, start_date, end_date, config):
    """ """Obtiene los datos históricos de las acciones para un símbolo de empresa dado en un rango de fechas específico.

    Args:
        symbol (str): Símbolo de la empresa
        start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'
        end_date (str): Fecha de finalización en formato 'YYYY-MM-DD'
        config (dict): Diccionario con la configuración de la aplicación

    Returns:
        pd.DataFrame: DataFrame con los datos históricos de las acciones
    """ """

    api_key = config.get('api_key')
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={api_key}&from={start_date}&to={end_date}'
    
    response = requests.get(url, verify=False)  # Agregar el argumento verify=False aquí
    
    if response.status_code == 200:
        json_data = response.json()
        historical_data = json_data['historical']
        df = pd.DataFrame(historical_data)
        return df
    else:
        print(f"Error al obtener datos para {symbol}: {response.status_code}")
        return None

# Cargar los datos del archivo CSV de la ruta especificada
sp500 = pd.read_csv('pom/' + config['Location_SP500_list'])

# Extraer los símbolos de SP500 del DataFrame cargado
symbols = sp500['Symbol'].tolist()
#Solo como prueba, ultimos 5 valores
symbols = symbols[:5]

# Define las fechas de inicio y finalización usando la función get_time_delta
today = datetime.now() - timedelta(days=1)  # Resta un día a la fecha actual
start_date, end_date = get_time_delta(today, 5 * 365)


# Obtiene los datos históricos de las acciones para cada símbolo y guarda los DataFrames en un diccionario
stock_data = {}
for symbol in symbols:
    stock_data[symbol] = get_stock_data(symbol, start_date, end_date, config)  # Cambiar config['api_key'] por config



"""