import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
from datetime import datetime, timedelta
import json

# Suprimir advertencias de solicitudes no seguras
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Cargar el archivo JSON de la ruta especificada
with open('pom/01_data/parameters.json') as f:
    config = json.load(f)

print(type(config))

def get_time_delta(date: datetime, days: int, format: str = '%Y-%m-%d'):
    """Esta función devuelve una fecha que está 'days' días antes de la fecha pasada como argumento y su fecha original.

    Args:
        date (datetime): fecha para ser utilizada como referencia
        days (int): número de días para el intervalo de tiempo

    Returns:
        (str, str): fecha final y fecha de inicio en el formato especificado
    """
    return (date - timedelta(days=days)).strftime(format), date.strftime(format)

def get_stock_data(symbol, start_date, end_date, config):
    """Obtiene los datos históricos de las acciones para un símbolo de empresa dado en un rango de fechas específico.

    Args:
        symbol (str): Símbolo de la empresa
        start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'
        end_date (str): Fecha de finalización en formato 'YYYY-MM-DD'
        config (dict): Diccionario con la configuración de la aplicación

    Returns:
        pd.DataFrame: DataFrame con los datos históricos de las acciones
    """

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

# Define las fechas de inicio y finalización usando la función get_time_delta
today = datetime.now()
start_date, end_date = get_time_delta(today, 5 * 365)

# Obtiene los datos históricos de las acciones para cada símbolo y guarda los DataFrames en un diccionario
stock_data = {}
for symbol in symbols:
    stock_data[symbol] = get_stock_data(symbol, start_date, end_date, config)  # Cambiar config['api_key'] por config

