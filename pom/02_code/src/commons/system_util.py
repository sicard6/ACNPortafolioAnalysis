# -*- coding: utf-8 -*-
"""
system_util.py
====================================
This module contains a class to verify folder system integrity and create the folders
in case to be necessary. This also manage model parameters placing it into "parameters" dict.
Finally, there is a useful function named "get_string_time" to convert time delta and get 
time in HH:MM:SS format.

@author:
     - g.munera.gonzalez
     - c.maldonado
"""
import sys, os, json, re, datetime



class SystemUtilities:
    """This module contains a class to verify folder system integrity and create the folders
    in case to be necessary.

    In case you need to add another directory to be check modify method check_itall

    Attributes
    ----------
    v_data : str
        Simulation running name
    path : str
        sys.path[0], the __main__.py base path of the development
    path_in : str
        Path where input data is located
    path_out : str
        Path where output data will be located. It includes v_data folder
    parameters : dict
        Dictionary with front parameters

    Parameters
    ----------
    s3_data : Boolean
        Define if read from S3 or not
    param_file : str-Nonetype, default None
        Parameter json name to configure run
    date : datetime.datetime, default None
        Date to add in the output folder
    """
    def __init__(self, param_file=None, date=None):
        #reading and storing class inputs
        self.path = sys.path[0]
        self.param_file = param_file if param_file!=None else 'parameters.json'
        #getting parameters from json
        self.date = date.strftime("%Y%m%d-%H%M%S") if date!=None else None

    def read_parameters(self):
        '''Method defined to read front parameters 
        '''
        print(f'    reading parameters file {self.param_file}...')
        with open(os.path.join(os.path.dirname(self.path), '01_data', self.param_file), 'r') as f:
            json_ = f.readlines()
        self.params = json.loads(''.join(json_).replace("'", '"'))
        print('    processing ...')
        self.v_data = self.params['run_name']
        self.path_in = os.path.join(os.path.dirname(self.path), self.params['local_input'])
        #defining output folder
        user = ''.join(re.split(r'\W', os.getlogin())[0:2])
        simulation = self.date+'_'+self.v_data+'_'+user if self.date!=None else self.v_data
        self.path_out = os.path.join(os.path.dirname(self.path), self.params['local_output'], simulation)
        self.path_out_curated = os.path.join(os.path.dirname(self.path), self.params['local_output_curated'], simulation)
    #PREGUNTAR SOBRE BACKUP DE RETURNS
    def generate_parameters(self):
        print('    reading parameters...')
        self.parameters = {}
        self.parameters["output_dir_returns"] = os.path.join(self.path_out_curated, "returns.csv")
        self.parameters["output_dir_mean"] = os.path.join(self.path_out_curated, "mean.csv")
        self.parameters["json_file"] = self.params
        self.parameters["coefficient"] = self.params["coefficient"]
        self.parameters["crypto"] = self.params["crypto"]
        self.parameters["sp500"] = self.params["sp500"]
        self.parameters["periodicity"] = self.params["periodicity"]
        self.parameters["output_json_dir"] = os.path.join(self.path_out, self.param_file)
        self.parameters["dir_crypto"] = os.path.join(self.path_in, "Crypto_History.csv")
        self.parameters["dir_sp500"] = os.path.join(self.path_in, "SP500_History.csv")
    

    def check_directories(self):
        '''This method check completitud in file folders. In case one of the directories list paths
        doesn't exists the method make that directory
        '''
        print('    checking directories...')
        directories = [
            os.path.join(self.path_in),
            os.path.dirname(self.path_out),
            self.path_out,
        ]
        for directory in directories:
            if not os.path.exists(directory):
                os.mkdir(directory)





