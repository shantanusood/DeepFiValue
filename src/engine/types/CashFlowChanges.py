import os
import pandas as pd
from src.engine.types import Helpers

class CashFlowChanges:
    parent = ""
    subsector = ""
    data = []

    def __init__(self, parent, subsector, data):
        self.parent = parent
        self.subsector = subsector
        self.data = data

    def final(self):
        self.cash_growth()
        self.capex()
        self.iss_debt()
        return str(self.data).replace("'", "\"")

    def cash_growth(self):
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
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "cf")
                if len(list(fin.keys())) == 4:
                    rev_lst = []
                    for x in range(1, len(list(fin.keys()))):
                        rev_lst.append(int(str(fin[str(list(fin.keys())[x])]['Free Cash Flow']).replace(",", "")))
                    self.data[count]['cashflowchanges'] = {
                        'c-1': str(round(((rev_lst[0] - rev_lst[1]) / abs(rev_lst[1])) * 100)),
                        'c-2': str(round(((rev_lst[1] - rev_lst[2]) / abs(rev_lst[2])) * 100))}
                else:
                    self.data[count]['cashflowchanges'] = {'c-1': '-999', 'c-2': '-999'}
                    pass
            except:
                self.data[count]['cashflowchanges'] = {'c-1': '-999', 'c-2': '-999'}
                pass
            count = count + 1

    def capex(self):
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
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "cf")
                if len(list(fin.keys())) == 4:
                    rev_lst = []
                    for x in range(1, len(list(fin.keys()))):
                        rev_lst.append(int(str(fin[str(list(fin.keys())[x])]['Capital Expenditure']).replace(",", "")))
                    self.data[count]['cashflowchanges']['ce-1'] = str(
                        round(((abs(rev_lst[0]) - abs(rev_lst[1])) / abs(rev_lst[1])) * 100))
                    self.data[count]['cashflowchanges']['ce-2'] = str(
                        round(((abs(rev_lst[1]) - abs(rev_lst[2])) / abs(rev_lst[2])) * 100))
                else:
                    self.data[count]['cashflowchanges']['ce-1'] = '-999'
                    self.data[count]['cashflowchanges']['ce-2'] = '-999'
                    pass
            except:
                self.data[count]['cashflowchanges']['ce-1'] = '-999'
                self.data[count]['cashflowchanges']['ce-2'] = '-999'
                pass
            count = count + 1

    def iss_debt(self):
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
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "cf")
                if len(list(fin.keys())) == 4:
                    rev_lst = []
                    for x in range(1, len(list(fin.keys()))):
                        rev_lst.append(int(str(fin[str(list(fin.keys())[x])]['Issuance of Debt']).replace(",", "")))
                    self.data[count]['cashflowchanges']['id-1'] = str(
                        round(((rev_lst[0] - rev_lst[1]) / abs(rev_lst[1])) * 100))
                    self.data[count]['cashflowchanges']['id-2'] = str(
                        round(((rev_lst[1] - rev_lst[2]) / abs(rev_lst[2])) * 100))
                else:
                    self.data[count]['cashflowchanges']['id-1'] = '-999'
                    self.data[count]['cashflowchanges']['id-2'] = '-999'
                    pass
            except:
                self.data[count]['cashflowchanges']['id-1'] = '-999'
                self.data[count]['cashflowchanges']['id-2'] = '-999'
                pass
            count = count + 1