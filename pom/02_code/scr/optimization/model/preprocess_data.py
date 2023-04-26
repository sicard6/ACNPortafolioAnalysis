import pandas as pd
import os, sys
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path[0] =os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
#Preguntar como se hace este import bien 
#Acá deben ir las funciones donde se filtren los activos no deseados 
from scr.optimization.model.preprocess_classes.process_data import ProcessData
from scr.commons.system_util import SystemUtilities

def preprocess_data(parameters):
    processed_data = ProcessData(parameters) 
    data = processed_data.read_local_data()       
    atri_data = processed_data.process_data(data)  
    processed_data.create_attributes(atri_data)
    return processed_data         

system_util = SystemUtilities()
system_util.read_parameters()
system_util.generate_parameters()
parameters = system_util.parameters
x = preprocess_data(parameters)
print(x.returns)