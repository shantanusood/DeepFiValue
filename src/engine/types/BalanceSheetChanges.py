import os
import pandas as pd
from src.engine.types import Helpers

class BalanceSheetChanges:
    parent = ""
    subsector = ""
    data = []

    def __init__(self, parent, subsector, data):
        self.parent = parent
        self.subsector = subsector
        self.data = data

    def final(self):
        self.asset_growth()
        self.shares_growth()
        self.asset_liab()
        self.debt_growth()
        return str(self.data).replace("'", "\"")

    def asset_growth(self):
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
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "bs")
                if len(list(fin.keys())) == 3:
                    rev_lst = []
                    for x in range(0, len(list(fin.keys()))):
                        rev_lst.append(int(str(fin[str(list(fin.keys())[x])]['Total Assets']).replace(",", "")))
                    self.data[count]['balancesheetchanges'] = {'a-1': str(round(((rev_lst[0] - rev_lst[1]) / rev_lst[1])*100)), 'a-2': str(round(((rev_lst[1] - rev_lst[2])/abs(rev_lst[2]))*100))}
                else:
                    self.data[count]['balancesheetchanges'] = {'a-1': '-999', 'a-2': '-999'}
                    pass
            except:
                self.data[count]['balancesheetchanges'] = {'a-1': '-999', 'a-2': '-999'}
                pass
            count = count + 1

    def shares_growth(self):
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
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "bs")
                if len(list(fin.keys())) == 3:
                    rev_lst = []
                    for x in range(0, len(list(fin.keys()))):
                        rev_lst.append(int(str(fin[str(list(fin.keys())[x])]['Ordinary Shares Number']).replace(",", "")))
                    self.data[count]['balancesheetchanges']['sh-1'] = str(round(((rev_lst[0] - rev_lst[1]) / rev_lst[1])*100))
                    self.data[count]['balancesheetchanges']['sh-2'] = str(round(((rev_lst[1] - rev_lst[2])/abs(rev_lst[2]))*100))
                else:
                    self.data[count]['balancesheetchanges']['sh-1'] = '-999'
                    self.data[count]['balancesheetchanges']['sh-2'] = '-999'
                    pass
            except:
                self.data[count]['balancesheetchanges']['sh-1'] = '-999'
                self.data[count]['balancesheetchanges']['sh-2'] = '-999'
                pass
            count = count + 1

    def asset_liab(self):
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
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "bs")
                rev = int(str(fin[str(list(fin.keys())[0])]['Total Assets']).replace(",", ""))
                cost = int(str(fin[str(list(fin.keys())[0])]['Total Liabilities Net Minority Interest']).replace(",", ""))
                self.data[count]['balancesheetchanges']['assToLia'] = str(round((rev / cost), 2))
            except:
                self.data[count]['balancesheetchanges']['assToLia'] = '-999'
                pass
            count = count + 1

    def debt_growth(self):
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
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "bs")
                if len(list(fin.keys())) == 3:
                    rev_lst = []
                    for x in range(0, len(list(fin.keys()))):
                        rev_lst.append(int(str(fin[str(list(fin.keys())[x])]['Total Debt']).replace(",", "")))
                    self.data[count]['balancesheetchanges']['d-1'] = str(round(((rev_lst[0] - rev_lst[1]) / abs(rev_lst[1]))*100))
                    self.data[count]['balancesheetchanges']['d-2'] = str(round(((rev_lst[1] - rev_lst[2])/abs(rev_lst[2]))*100))
                else:
                    self.data[count]['balancesheetchanges']['d-1'] = '-999'
                    self.data[count]['balancesheetchanges']['d-2'] = '-999'
                    pass
            except:
                self.data[count]['balancesheetchanges']['d-1'] = '-999'
                self.data[count]['balancesheetchanges']['d-2'] = '-999'
                pass
            count = count + 1