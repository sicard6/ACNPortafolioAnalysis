# -*- coding: utf-8 -*-
"""
s3_manager.py
====================================
This module contains a class to manage s3 connections and pull-push data

@author:
     - g.munera.gonzalez
"""

import re, os, boto3
import pandas as pd

class S3Manager:
    '''Class defined to manage s3 bicket connections letting user pull-push data

    Attributes
    ----------
    user : str
        aws user to enable connection to the s3 bucket
    secret : str
        aws password to enable connection to the s3 bucket
    bucket : str
        bucket-repository wich contain data to push-pull
    client : botocore.client.S3
        boto3 client connection
    resource : s3.ServiceResource
        boto3 resource object

    Parameters
    ----------
    bucket : str, optional default None
        Buket name to consume the data
    '''

    def __init__(self, bucket=None):
        self.bucket = bucket if bucket!=None else os.environ['S3_BUCKET']
        self.connect()
    
    def connect(self):
        '''Create connection and boto3 objects
        '''
        # Creating the low level functional client
        self.client = boto3.client('s3', region_name = 'us-east-1')
            
        # Creating the high level object oriented interface
        self.resource = boto3.resource('s3', region_name = 'us-east-1')

    def get_preffix_list(self, prefix):
        bucket_ = self.client.list_objects(Bucket=self.bucket, Prefix=prefix)
        files, dates = [], []
        for obj in bucket_['Contents']:
            if re.sub(r'\W', '', obj['Key'])!=re.sub(r'\W', '', prefix):
                files.append(obj['Key'])
                dates.append(obj['LastModified'])
        files = pd.DataFrame({'FILE': files, 'DATE': dates})
        return files

    def get_recent_file(self, prefix, ascending=False):
        '''Method defined to get the most recent file on s3 prefix

        Parameters
        ----------
        prefix : str
            S3 bucket prefix to find the most recent file

        Returns
        -------
        recent_file : str
            S3 path with the most recent file in the sufix (example: sufix/recent_file)
        '''
        files = self.get_preffix_list(prefix)
        if len(files):
            recent_file = files.sort_values('DATE', ascending=ascending).FILE.iloc[0]
            return recent_file
        else:
            return None
    
    def get_s3data(self, file, sheet_name=None, pandas=True):
        '''Pull data from s3 bucket

        Parameters
        ----------
        file : str
            file path in the s3 bucket
        sheet_name : str, optional
            In case file is an excel file, let user specify sheet name
        pandas: boolean
            Define if return a pandas.DataFrame 

        Returns
        -------
        data : pandas.DataFrame or byte object
            Object with s3 file data
        '''
        obj = self.client.get_object(
            Bucket=self.bucket,
            Key=file
        )
        if re.match('xl.+', file.split('.')[1]) and sheet_name!=None and pandas:
            data = pd.read_excel(obj['Body'].read(), sheet_name=sheet_name, engine='openpyxl')
        elif re.match('xl.+', file.split('.')[1]) and pandas:
            data = pd.read_excel(obj['Body'].read(), engine='openpyxl')
        elif file.split('.')[1]=='csv' and pandas:
            data = pd.read_csv(obj['Body'])
        elif file.split('.')[1]=='json' and pandas:
            data = pd.read_json(obj['Body'])
        else:
            return obj['Body']
        return data

    def save_s3results(self, folder, suffix):
        '''Save model results in s3 bucket

        Parameters
        ----------
        folder : str
            Folder where lies the files to upload
        suffix : str
            S3 bucket suffix
        '''
        for f in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, f)):
                self.client.upload_file(os.path.join(folder, f), self.bucket, f'{suffix}/{f}')