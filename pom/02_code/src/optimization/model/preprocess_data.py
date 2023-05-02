import pandas as pd
import os, sys
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path[0] =os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
#Acá deben ir las funciones donde se filtren los activos no deseados 
from src.optimization.model.preprocess_classes.process_data import ProcessData
from src.optimization.model.preprocess_classes.pyomo_data import PyomoData
from src.commons.system_util import SystemUtilities

def data_to_pyomo(processed_data):
    pyomo_data = PyomoData(processed_data)
    return pyomo_data  

def preprocess_data(parameters):
    processed_data = ProcessData(parameters) 
    data = processed_data.read_local_data()       
    atri_data = processed_data.process_data(data)  
    processed_data.create_attributes(atri_data)
    return processed_data

       
'''
system_util = SystemUtilities()
system_util.read_parameters()
system_util.generate_parameters()
parameters = system_util.parameters
x = preprocess_data(parameters)
prueba = PyomoData(x.returns)
print(prueba.dict)
'''