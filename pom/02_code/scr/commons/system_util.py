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
import pandas as pd
from src.commons.s3_manager import S3Manager


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
    def __init__(self, s3_data, param_file=None, date=None):
        #reading and storing class inputs
        self.path, self.s3_data = sys.path[0], s3_data
        self.param_file = param_file if param_file!=None else 'parameters.json'
        #getting parameters from json
        self.date = date.strftime("%Y%m%d-%H%M%S") if date!=None else None

    def read_parameters(self):
        '''Method defined to read front parameters 
        '''
        if re.match('linux.*', sys.platform) or self.s3_data:
            test = S3Manager()
            param_file = os.path.join(os.environ['PARAMETERS_PATH'], os.environ['PARAMETERS_JSON'])
            self.param_file = os.path.basename(param_file)
            print(f'    reading parameters file {param_file}...')
            json_ = test.get_s3data(param_file, pandas=False)
            json_ = json_.read()
            self.params = json.loads(''.join(json_.decode('utf-8')).replace("'", '"'))
            self.s3path_in = f"{self.params['input_path']}{self.params['asset'].lower()}/"
            self.s3path_out = self.params['output_path'].format(self.params['asset'].lower())
            self.s3path_appsync = self.params['appsync_path'].format(self.params['asset'].lower())
            self.s3path_param = f"{self.params['parametrics_path']}{self.params['asset'].lower()}/"
        else:
            print(f'    reading parameters file {self.param_file}...')
            with open(os.path.join(os.path.dirname(self.path), '01_data', self.param_file), 'r') as f:
                json_ = f.readlines()
            self.params = json.loads(''.join(json_).replace("'", '"'))
        print(f'    processing for {self.params["asset"]} asset...')
        self.v_data = self.params['run_name']
        self.path_in = os.path.join(os.path.dirname(self.path), self.params['local_input'])
        #defining output folder
        if re.match('linux.*', sys.platform) or self.s3_data:
            self.path_out = os.path.join(os.path.dirname(self.path), self.params['local_output'], self.v_data)
        else:
            user = ''.join(re.split(r'\W', os.getlogin())[0:2])
            simulation = self.date+'_'+self.v_data+'_'+user if self.date!=None else self.v_data
            self.path_out = os.path.join(os.path.dirname(self.path), self.params['local_output'], simulation)

    def generate_parameters(self, model):
        '''This model generate parameters attribute to distribute across all scripts
        Parameters
        ----------
        model : str
            String defining model output. Can be:
            cpf: For Ocelote cpf model
            injection: For Ocelote injection 
            extraction: For Ocelote extraction
            downstream: For downstream models
        '''
        print('    reading parameters...')
        self.parameters = {}
        if re.match('linux.*', sys.platform) or self.s3_data:
            self.parameters["data_file_dir"] = f'{self.s3path_in}{self.params[model+"_config"]}'
            self.parameters["pump_energy_model_dir"] = f'{self.s3path_in}{self.params[model+"_pump_models"]}'
            self.parameters["appsync_asset_dir"] = f'{self.s3path_param}{self.params["appsync_asset"]}'
            self.parameters["appsync_kpi_dir"] = f'{self.s3path_param}{self.params["appsync_kpi"]}'
            self.parameters["appsync_tool_level_dir"] = f'{self.s3path_param}{self.params["appsync_tool_level"]}'
            self.parameters["appsync_unit_dir"] = f'{self.s3path_param}{self.params["appsync_unit"]}'
            self.parameters['s3_output_model'] = f'{self.s3path_out}{self.v_data}'
            self.parameters["flow_file"] = f'{self.s3path_in}{self.params[model+"_flow_file"]}'
            self.parameters['s3_output_appsync'] = f'{self.s3path_appsync}{self.v_data}.csv'
            if model=='injection':
                self.parameters["well_pressure_drop_dir"] = f'{self.s3path_in}{self.params["injection_well_pressure_drop"]}'
                self.parameters["pump_variables_constraint_dir"] = f'{self.s3path_in}{self.params["injection_pump_contraints"]}'
                self.parameters["pump_rpm_relationship_dir"] = f'{self.s3path_in}{self.params["injection_pump_rpm_relation"]}'
        else:
            self.parameters["data_file_dir"] = os.path.join(self.path_in, self.params[model+"_config"])
            self.parameters["pump_energy_model_dir"] = os.path.join(self.path_in, self.params[model+"_pump_models"])
            self.parameters["flow_file"] = os.path.join(self.path_in, self.params[model+"_flow_file"])
            self.parameters["appsync_asset_dir"] = os.path.join(self.path_in, self.params["appsync_asset"])
            self.parameters["appsync_kpi_dir"] = os.path.join(self.path_in, self.params["appsync_kpi"])
            self.parameters["appsync_tool_level_dir"] = os.path.join(self.path_in, self.params["appsync_tool_level"])
            self.parameters["appsync_unit_dir"] = os.path.join(self.path_in, self.params["appsync_unit"])
            if model=='injection':
                self.parameters["well_pressure_drop_dir"] = os.path.join(self.path_in, self.params["injection_well_pressure_drop"])
                self.parameters["pump_variables_constraint_dir"] = os.path.join(self.path_in, self.params["injection_pump_contraints"])
                self.parameters["pump_rpm_relationship_dir"] = os.path.join(self.path_in, self.params["injection_pump_rpm_relation"])

        self.parameters["output_model_dir"] = os.path.join(self.path_out, f"model_results_{model}_summary.csv")
        self.parameters["output_nodes_dir"] = os.path.join(self.path_out, f"model_results_{model}_nodes.csv")
        self.parameters["output_arcs_dir"] = os.path.join(self.path_out, f"model_results_{model}_edges.csv")
        self.parameters["output_json_dir"] = os.path.join(self.path_out, self.param_file)
        self.parameters["output_recommendations_dir"] = os.path.join(self.path_out, f'recommendations_{model}.json')
        self.parameters["validation_nodes_dir"] = os.path.join(self.path_out, f"model_validation_{model}_nodes.csv")
        self.parameters["validation_arcs_dir"] = os.path.join(self.path_out, f"model_validation_{model}_edges.csv")
        self.parameters["solver_log"] = os.path.join(self.path_out, f"solve_{model}.log")

        #reding numeric parameters
        self.parameters["energy_cost"] = self.params['energy_cost']
        self.parameters["energy_co2"] = self.params['energy_co2']
        self.parameters["time_periods"] = self.params['time_periods']
        self.parameters["percentage_hierarchical_optimization"] = self.params['percentage_hierarchical_optimization']
        self.parameters["iterations"] = self.params["iterations"]
        self.parameters["delta"] = self.params["delta"]
        #reading other cross features
        self.parameters["json_file"] = self.params
        self.parameters["object_funct"] = self.params[f"{model}_object_funct"]
        self.parameters["water"] = self.params["water"]
        self.parameters["injection"] = self.params["injection"]
        self.parameters["pump_safety_factor_pressure"]=self.params["pump_safety_factor_pressure"]
        self.parameters["pump_safety_factor_flow"]=self.params["pump_safety_factor_flow"]
        self.parameters["barrel_to_liters"] = 158.987304
        self.parameters["day_to_sec"] = 86400
        self.parameters["watt_to_kwh"] = 1
        

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

def get_string_time(t):
    '''Function defined to get string time from time measured in seconds
    Parameters
    ----------
    t : float
        Time in seconds
    Returns
    ----------
    time: str
        String time
    '''
    m = int(t//60)
    if m>0:
        s = int(round(t)-m*60)
    else:
        s = round(t)
    m = f'0{m}' if m<10 else m
    s = f'0{s}' if s<10 else s
    return f'{m}:{s}'

def get_athenas_error(error_msg, model,id_model):
    '''Function defined with the goal of provide a error handling database to let architecture team know there were troubles in the optimization model execution
    Parameters
    ----------
    error_msg : str
        String explaining the error get from model
    model : str
        Failed model (water or injection)
    id_model : str
        Has of the model running
    '''
    cols = [
        'DATE', 'ORIGIN', 'REGION', 'OPERATIONS', 'ASSET', 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_4', 'LEVEL_5', 'LEVEL_6',
        'ID_MODEL', 'TOOL', 'OBJECT_IN_GRAPH', 'SOURCE_FILE', 'SOURCE', 'TARGET', 'VALUE', 'TYPE_VARIABLE', 'VARIABLE_TAG',
        'SENSOR', 'VARIABLE', 'SERVICE_TYPE', 'UNITS', 'MIN', 'MAX', 'QUALITY_PASS'
    ]
    error = error_msg.replace(f'Model {model.upper()} solving fail with error "', '')[:-2]
    error = error.replace('"', "'").replace('\n', '').replace('\\', '/')
    json_ = '[{}"type": "model_error", "params": {}"value": "{}","source":"ALL_MODEL","target":"ALL_MODEL"{}{}]'.format('{', '{', error, '}', '}')
    ath_db = pd.DataFrame(columns=cols).assign(VARIABLE_TAG=[f'{model.upper()}_ERROR']).assign(QUALITY_PASS=[json_])
    ath_db = ath_db.assign(ID_MODEL=id_model).assign(DATE=1)
    return ath_db