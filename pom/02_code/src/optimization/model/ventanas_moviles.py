# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


data = pd.read_csv("pom\\01_data\\pct_change\\S&P500-Curated-Data_MS_pct_change.csv", encoding="utf-8",sep=",",index_col="Date")
num_columns=len(data.columns)
result=[[] for i in range(num_columns)]
initial_window_length = 12
window_shift = 1 

for window_start in range(0, len(data), window_shift):
    window_end = window_start + initial_window_length
    if window_end > len(data):
        break
    window = data.iloc[window_start:window_end]
    for col in range(num_columns):
        mean = np.mean(window.iloc[:, col])
        result[col].append(mean)

for col in range(num_columns):
    print(f"Medias móviles para la columna {data.columns[col]}:")
    for i in range(len(result[col])):
        print(f"Longitud de ventana {initial_window_length - i * window_shift}: {result[col][i]}")

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
    