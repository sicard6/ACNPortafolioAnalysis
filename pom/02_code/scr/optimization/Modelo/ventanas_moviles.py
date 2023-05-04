import numpy as np

data = [...]
initial_window_length = 1000
window_shift = 100 

window_lengths = []
window_means = []

window_length = initial_window_length
while window_length > 0:
    strides = (data.itemsize,) * 2
    shape = ((len(data) - window_length) // window_shift + 1, window_length)
    windows = np.lib.stride_tricks.as_strided(np.array(data), shape=shape, strides=strides)
    window_lengths.append(window_length)
    window_means.append(windows.mean(axis=1))
    window_length -= window_shift

for i in range(len(window_lengths)):
    print(f"Ventana de longitud {window_lengths[i]}: {window_means[i]}")