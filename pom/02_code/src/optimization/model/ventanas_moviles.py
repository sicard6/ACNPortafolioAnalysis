# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


data = pd.read_csv("pom\\01_data\\pct_change\\S&P500-Curated-Data_MS_pct_change.csv", encoding="utf-8",sep=",",index_col="Date")
num_columns=len(data.columns)
result=[[] for i in range(0,num_columns)]
initial_window_length = 12
min_len=12
window_shift = 1 

for window_start in range(len(data)-1,min_len-2, -window_shift):
    window_end = len(data)-1 - initial_window_length
    if window_end < 0:
        break
    window = data.iloc[window_end:len(data)-1]
    for col in range(num_columns):
        mean = np.mean(window.iloc[:, col])
        result[col].append(mean)
    initial_window_length=initial_window_length+1
marcos_de_tiempo=[]
minimo=1
for col in range(num_columns):
    print(f"Medias móviles para la columna {data.columns[col]}:")
    objetive=data.iloc[-1,col]
    for i in range(len(result[col])):
        print(f"Longitud de ventana {min_len+i}: {result[col][i]}")
        diferencia=abs((result[col][i])-objetive)
        if diferencia < minimo:
            minimo=result[col][i]
            longitud_objetivo=min_len+i 
    marcos_de_tiempo.append(longitud_objetivo)
print(marcos_de_tiempo)
print(len(marcos_de_tiempo))
""""
window_lengths = []
window_means = []

window_length = initial_window_length
for column in list(range(1, (data.shape[1])+1)):
    while window_length > 0:
        strides = (data.iloc[:, column].strides) * 2
        shape = ((len(data) - window_length) // window_shift + 1, window_length)
        windows = pd.DataFrame(np.lib.stride_tricks.as_strided(np.array(data.iloc[:, column])), shape=shape, strides=strides)
        window_lengths.append(window_length)
        window_means.append(windows.mean(axis=1).values)
        window_length -= window_shift

for i in range(len(window_lengths)):
    print(f"Ventana de longitud {window_lengths[i]}: {window_means[i]}")
"""
    