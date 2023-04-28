import pandas as pd
import datetime
#PREGUNTAR es posible que alguno tenga mas de dos dimisenciones en el futuro?
class PyomoData:
    def __init__(self, data):
        self.data = data
        if isinstance(self.data, pd.DataFrame):
            dates = self.data.index.tolist()
            self.time_set =[datetime.datetime.strptime(dates, '%Y-%m-%d').date() for dates in dates]
            self.assets_set = list(self.data.columns)
            self.dict = {}
            for col in self.data.columns:
                for index, value in self.data[col].items():
                    self.dict[(index, col)] = value
        elif isinstance(self.data, pd.Series):
            self.dict = self.data.to_dict()

    