import os
import pandas as pd
from src.engine.types import Helpers

class IncomeChanges:
    parent = ""
    subsector = ""
    data = []

    def __init__(self, parent, subsector, data):
        self.parent = parent
        self.subsector = subsector
        self.data = data

    def final(self):
        self.rev_growth()
        self.cost_rev()
        self.prof_mar()
        self.oper_mar()
        return str(self.data).replace("'", "\"")

    def rev_growth(self):
        count = 0
        parent_t = ""
        for tick in self.data:
            if self.parent == "Customs":
                if os.path.isfile('./data/tickers/Categories.csv'):
                    get_parent = pd.read_csv('./data/tickers/Categories.csv')
                    isSubsector = get_parent['Subsector'] == tick['Category']
                    parentSect = get_parent[isSubsector]
                    parent_t = str(parentSect['ParentSector'].head(1).item())
            else:
                parent_t = self.parent
            try:
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "fin")
                if len(list(fin.keys())) == 4:
                    rev_lst = []
                    for x in range(1, len(list(fin.keys()))):
                        rev_lst.append(int(str(fin[str(list(fin.keys())[x])]['Total Revenue']).replace(",", "")))
                    self.data[count]['incomechanges'] = {'g-1': str(round(((rev_lst[0] - rev_lst[1]) / abs(rev_lst[1]))*100)), 'g-2': str(round(((rev_lst[1] - rev_lst[2])/abs(rev_lst[2]))*100))}
                else:
                    self.data[count]['incomechanges'] = {'g-1': '-999', 'g-2': '-999'}
                    pass
            except:
                self.data[count]['incomechanges'] = {'g-1': '-999', 'g-2': '-999'}
                pass
            count = count + 1

    def cost_rev(self):
        count = 0
        parent_t = ""
        for tick in self.data:
            if self.parent == "Customs":
                if os.path.isfile('./data/tickers/Categories.csv'):
                    get_parent = pd.read_csv('./data/tickers/Categories.csv')
                    isSubsector = get_parent['Subsector'] == tick['Category']
                    parentSect = get_parent[isSubsector]
                    parent_t = str(parentSect['ParentSector'].head(1).item())
            else:
                parent_t = self.parent
            try:
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "fin")
                if 'TTM' in list(fin.keys()):
                    cost = int(str(fin['TTM']['Cost of Revenue']).replace(",", ""))
                    rev = int(str(fin['TTM']['Total Revenue']).replace(",", ""))
                    self.data[count]['incomechanges']['cOfRev'] = str(round((cost/rev)*100))
                else:
                    self.data[count]['incomechanges']['cOfRev'] = '-999'
                    pass
            except:
                self.data[count]['incomechanges']['cOfRev'] = '-999'
                pass
            count = count + 1

    def prof_mar(self):
        count = 0
        parent_t = ""
        for tick in self.data:
            if self.parent == "Customs":
                if os.path.isfile('./data/tickers/Categories.csv'):
                    get_parent = pd.read_csv('./data/tickers/Categories.csv')
                    isSubsector = get_parent['Subsector'] == tick['Category']
                    parentSect = get_parent[isSubsector]
                    parent_t = str(parentSect['ParentSector'].head(1).item())
            else:
                parent_t = self.parent
            try:
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "fin")
                if 'TTM' in list(fin.keys()):
                    cost = int(str(fin['TTM']['Gross Profit']).replace(",", ""))
                    rev = int(str(fin['TTM']['Total Revenue']).replace(",", ""))
                    self.data[count]['incomechanges']['profMar'] = str(round((cost / rev) * 100))
                else:
                    self.data[count]['incomechanges']['profMar'] = '-999'
                    pass
            except:
                self.data[count]['incomechanges']['profMar'] = '-999'
                pass
            count = count + 1

    def oper_mar(self):
        count = 0
        parent_t = ""
        for tick in self.data:
            if self.parent == "Customs":
                if os.path.isfile('./data/tickers/Categories.csv'):
                    get_parent = pd.read_csv('./data/tickers/Categories.csv')
                    isSubsector = get_parent['Subsector'] == tick['Category']
                    parentSect = get_parent[isSubsector]
                    parent_t = str(parentSect['ParentSector'].head(1).item())
            else:
                parent_t = self.parent
            try:
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "fin")
                if 'TTM' in list(fin.keys()):
                    cost = int(str(fin['TTM']['Operating Income']).replace(",", ""))
                    rev = int(str(fin['TTM']['Total Revenue']).replace(",", ""))
                    self.data[count]['incomechanges']['opMar'] = str(round((cost / rev) * 100))
                else:
                    self.data[count]['incomechanges']['opMar'] = '-999'
                    pass
            except:
                self.data[count]['incomechanges']['opMar'] = '-999'
                pass
            count = count + 1
