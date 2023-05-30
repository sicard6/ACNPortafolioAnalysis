# -*- coding: utf-8 -*-
"""
process_results.py
====================================
This module contains a class process model outputs and get athena data base structure

@author:
     - g.munera.gonzalez
     - ivan.caro
     - ivo.pajor
"""

import sys, os, re, datetime
import pandas as pd
from src.commons.system_util import SystemUtilities
from src.commons.s3_manager import S3Manager

class ProcessResults(SystemUtilities, S3Manager):
    '''Class used to process athena database from model outputs
    Attributes
    ----------
    model : str
        Model to process data
    s3_data : Boolean
        Define if read from S3 or not
    data_dict : str
        Dictionary with models data (arcs, nodes and summary)
    tool_params : pandas.DataFrame
        Parametric tool table with nodes equivalences and features
    unit_params : pandas.DataFrame
        Parametric unit table with variable's units
    conf_data : pandas.DataFrame
        Configuration file values to extract nodes capacities
    edges : pandas.DataFrame
        Arcs filtered data
    nodes : pandas.DataFrame
        Arcs filtered data
    athena : pandas.DataFrame
        Structured athena's data base
    pandas_results : List of pandas.DataFrame
        List that contains the results of the model
    Parameters
    ----------
    model : str
        Select model to process data. can be "injection" or "cpd"
    s3_data : Boolean
        Define if read from S3 or not
    param_file : str-Nonetype, dafault None
        Parameter json name to configure run
    date : datetime.datetime, default None
        Date to add in the output folder
    '''
    def __init__(self, model, pandas_results, s3_data=False, param_file=None, date=None):
        self.model, self.now , self.data_dict = model, datetime.datetime.now(), pandas_results
        SystemUtilities.__init__(self, s3_data, param_file=param_file, date=date)
        self.read_parameters()
        self.generate_parameters(model)
        self.get_data()
        print('    processing edges...')
        self.process_edges()
        print('    processing nodes...')
        self.process_nodes()
        print('    putting it together...')
        self.get_athena_db()
        print('    addign kpis to database...')
        self.get_kpi()

    def get_data(self):
        '''Method defined to get data (wherever data lies)
        '''
        if re.match('linux.*', sys.platform) or self.s3_data:
            print('    reading data from s3 bucket...')
            S3Manager.__init__(self)
            self.read_datas3()
        else:
            print('    reading data from one drive...')
            self.read_dataod()

    def read_dataod(self):
        '''Read data from one drive
        '''
        #defining paths
        conf_data = os.path.join(self.path_in, self.parameters['json_file'][self.model+"_config"])
        #reding data
        self.tool_params = pd.read_csv(self.parameters["appsync_tool_level_dir"])
        self.unit_params = pd.read_csv(self.parameters["appsync_unit_dir"])
        self.asset_params = pd.read_csv(self.parameters["appsync_asset_dir"])
        self.kpi_params = pd.read_csv(self.parameters["appsync_kpi_dir"])
        sheet = 'Nodes_inj' if self.model=='injection' else 'Arc_CPF'
        conf_data = pd.read_excel(conf_data, sheet_name=sheet)
        self.conf_data = conf_data.rename({'Node_Start': 'Tool', 'MaxFlow': 'Capacity'}, axis=1)
    
    def read_datas3(self):
        '''Method defined to read data from s3 bucket
        '''
        #defining paths
        conf_data = f'{self.s3path_in}{self.parameters["json_file"][self.model+"_config"]}'
        #reding data
        self.tool_params = self.get_s3data(self.parameters["appsync_tool_level_dir"])
        self.unit_params = self.get_s3data(self.parameters["appsync_unit_dir"])
        self.asset_params = self.get_s3data(self.parameters["appsync_asset_dir"])
        self.kpi_params = self.get_s3data(self.parameters["appsync_kpi_dir"])
        sheet = 'Nodes_inj' if self.model=='injection' else 'Arc_CPF'
        conf_data = self.get_s3data(conf_data, sheet_name=sheet)
        self.conf_data = conf_data.rename({'Node_Start': 'Tool', 'MaxFlow': 'Capacity'}, axis=1)

    def process_edges(self):
        '''Process arcs data to filter useful features
        '''
        edges = self.data_dict['edges']
        edges.columns = edges.columns.str.upper()
        edges = pd.melt(edges, id_vars=['SOURCE', 'TARGET', 'DATE'], var_name='VARIABLE', value_name='VALUE')
        self.edges = edges

    def process_nodes(self):
        '''Process nodes data to filter useful features
        '''    
        nodes = self.data_dict['nodes'].rename({'Node': 'SOURCE'}, axis=1)
        nodes.columns = nodes.columns.str.upper()
        nodes = pd.melt(nodes, id_vars=['SOURCE', 'DATE'], var_name='VARIABLE', value_name='VALUE').assign(TARGET='')
        self.nodes = nodes

    def get_athena_db(self):
        '''Use nodes and arcs to structure athena attribute with the db used in the front
        '''
        athena = pd.concat([self.edges, self.nodes])
        athena = athena.assign(ORIGIN='MODEL').assign(ASSET=self.parameters['json_file']['asset'].upper())
        athena = athena.join(self.asset_params.set_index('ASSET'), on='ASSET')
        athena = athena.assign(ID_MODEL=self.v_data).dropna(subset=['VALUE'])
        athena_ = athena[athena.TARGET=='']
        athena_ = athena_.assign(VARIABLE_TAG=athena_.ORIGIN+'_'+athena_.VARIABLE+'_'+athena_.SOURCE)
        athena = athena[~(athena.TARGET=='')]
        athena = athena.assign(VARIABLE_TAG=athena.ORIGIN+'_'+athena.VARIABLE+'_'+athena.SOURCE+'_'+athena.TARGET)
        athena_ = athena_.assign(OBJECT_IN_GRAPH='NODE')
        athena = pd.concat([athena.assign(OBJECT_IN_GRAPH='ARC'), athena_])
        athena = athena.assign(SERVICE_TYPE='WATER').assign(SOURCE_FILE='')
        #joint with tool parametric table
        athena = athena.join(self.tool_params.set_index('ASSET'), on='SOURCE')
        #joint with unit parametric table
        athena = athena.join(self.unit_params.set_index('VARIABLE'), on='VARIABLE').assign(MIN=0)
        conf_data = self.conf_data[['Tool', 'Capacity']].rename({'Capacity': 'MAX'}, axis=1).set_index('Tool')
        athena = athena.join(conf_data, on='SOURCE')
        athena = athena.assign(SENSOR='').assign(QUALITY_PASS='')
        cols = [
            'DATE', 'ORIGIN', 'REGION', 'OPERATIONS', 'ASSET', 'LEVEL_1', 'LEVEL_2', 'LEVEL_3', 'LEVEL_4',
            'LEVEL_5', 'LEVEL_6', 'ID_MODEL', 'TOOL', 'OBJECT_IN_GRAPH', 'SOURCE_FILE', 'SOURCE', 'TARGET',
            'VALUE', 'TYPE_VARIABLE', 'VARIABLE_TAG', 'SENSOR', 'VARIABLE', 'SERVICE_TYPE', 'UNITS', 'MIN',
            'MAX', 'QUALITY_PASS'
        ]
        self.athena = athena[cols]

    def get_kpi(self):
        kpi = self.data_dict['summary'].assign(ASSET=self.parameters['json_file']['asset'].upper()).assign(MODEL=self.model.upper())
        kpi = pd.melt(kpi, id_vars=['DATE', 'ASSET', 'MODEL'], var_name='MODEL_VAR', value_name='VALUE')
        kpi = kpi.join(self.kpi_params.set_index(['ASSET', 'MODEL', 'MODEL_VAR']), on=['ASSET', 'MODEL', 'MODEL_VAR'], how='inner')
        kpi = kpi.assign(ID_MODEL=self.v_data)
        self.athena = pd.concat([self.athena, kpi.drop(['MODEL', 'MODEL_VAR'], axis=1)])