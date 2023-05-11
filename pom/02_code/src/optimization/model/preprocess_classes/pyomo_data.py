import pandas as pd
import numpy as np
#PREGUNTAR es posible que alguno tenga mas de dos dimenciones en el futuro? es necesario guardar la fecha
class PyomoData:
    """
        A class that represents input data for Pyomo optimization models.

    Attributes:
        data (pandas.DataFrame or pandas.Series): The input data.
        time_set (list): A list of time periods.
        assets_set (list): A list of assets.
        dict (dict): A dictionary containing the input data, indexed by (time, asset).
    """


    def __init__(self, data):
        """
            Initializes a new instance of the PyomoData class.

        Parameters:
            data (pandas.DataFrame or pandas.Series): The input data to be processed.

        """
        print('    creating pyomo data...')
        self.data = data
        if isinstance(self.data, pd.DataFrame):
            self.data = self.data.set_index(pd.Index(np.arange(1, len(self.data)+1)))
            time = self.data.index.tolist()
            self.time_set = time
            self.assets_set = list(self.data.columns)
            self.dict = {}
            for col in self.data.columns:
                for index, value in self.data[col].items():
                    self.dict[(index, col)] = value
            
        elif isinstance(self.data, pd.Series):
            assets = self.data.index.tolist()
            self.assets_set = assets
            self.dict = self.data.to_dict()

    