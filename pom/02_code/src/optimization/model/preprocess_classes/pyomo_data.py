import pandas as pd
import numpy as np
#PREGUNTAR es posible que alguno tenga mas de dos dimenciones en el futuro? es necesario guardar la fecha
class PyomoData:
    def __init__(self, data):
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

    