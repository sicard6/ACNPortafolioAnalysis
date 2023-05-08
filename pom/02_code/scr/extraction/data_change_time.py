import os
import json
import pandas as pd

# Cargar el archivo JSON de la ruta especificada
with open('pom/01_data/parameters.json') as f:
    config = json.load(f)

def calculate_and_save_pct_change(input_path, output_path):
    # Lista todos los archivos CSV en la carpeta de entrada
    curated_files = [f for f in os.listdir(input_path) if f.endswith('.csv')]

    # Crea la carpeta de salida si no existe
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Procesa cada archivo CSV
    for file in curated_files:
        input_file_path = os.path.join(input_path, file)
        output_file_path = os.path.join(output_path, file[:-4] + "_pct_change.csv")

        # Lee el archivo CSV y almacena en un DataFrame
        df = pd.read_csv(input_file_path)

        # Selecciona sólo las columnas numéricas, excluyendo la columna 'Date'
        numeric_columns = df.select_dtypes(include=['number']).columns

        # Calcula el cambio porcentual sólo para las columnas numéricas
        df_pct_change = df[numeric_columns].pct_change()

        # Combina la columna 'Date' con los resultados del cambio porcentual
        result = pd.concat([df['Date'], df_pct_change], axis=1)

        # Elimina la primera fila (índice 0)
        result.drop(0, inplace=True)

        # Guarda el DataFrame resultante en un archivo CSV
        result.to_csv(output_file_path, index=False)
        print(f"Archivo {file} procesado y guardado en {output_file_path}")

# Usa las rutas de entrada y salida desde el archivo JSON
input_path = config['input_pct_change']
output_path = config['output_pct_change']

# Llama a la función con las rutas cargadas desde el archivo JSON
calculate_and_save_pct_change(input_path, output_path)
