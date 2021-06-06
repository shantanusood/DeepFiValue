from src.engine.types import Helpers
import random
import traceback
import os
import pandas as pd

class Ratios:
    parent = ""
    subsector = ""
    data = []

    def __init__(self, parent, subsector, data):
        self.parent = parent
        self.subsector = subsector
        self.data = data

    def final(self):
        return str(self.data).replace("'", "\"")

    def lines(self):
        lines_dict = {}
        lines_list = []
        for tick in self.data:
            parent_t = ""
            if self.parent == "Customs":
                if os.path.isfile('./data/tickers/Categories.csv'):
                    get_parent = pd.read_csv('./data/tickers/Categories.csv')
                    isSubsector = get_parent['Subsector'] == tick['Category']
                    parentSect = get_parent[isSubsector]
                    parent_t = str(parentSect['ParentSector'].head(1).item())
            else:
                parent_t = self.parent
            try:
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "ks")
                for x in range(1, len(list(fin.keys()))):
                    vals = set()
                    for y in fin[str(list(fin.keys())[x])]:
                        vals.add(y)
                    lines_dict = {tick['Ticker'] : list(vals)}
                    lines_list.append(lines_dict)
                    break
            except:
                pass
        return str(lines_list).replace("'", "\"")