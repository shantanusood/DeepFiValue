from src.engine.types import Helpers
import random
import traceback
import os
import pandas as pd

class Basics:
    parent = ""
    subsector = ""
    data = []

    def __init__(self, parent, subsector, data):
        self.parent = parent
        self.subsector = subsector
        self.data = data

    def final(self):
        self.mc()
        self.div()
        self.beta()
        self.price()
        self.pt()
        self.up()
        self.pMargin()
        return str(self.data).replace("'", "\"")

    def mc(self):
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "quote")
                if "ERROR" in p_e:
                    self.data[count]['basics'] = {'mc': '-999'}
                else:
                    if p_e[str(list(p_e.keys())[0])]['Market Cap'] == 'N/A':
                        self.data[count]['basics'] = {'mc': '-999'}
                    else:
                        m_cap = str(p_e[str(list(p_e.keys())[0])]['Market Cap'])
                        if "B" in m_cap:
                            m_cap = float(m_cap.replace("B", ""))
                        elif "M" in m_cap:
                            m_cap = round(float(m_cap.replace("M", ""))/1000, 2)
                        elif "T" in m_cap:
                            m_cap = round(float(m_cap.replace("T", ""))*1000, 2)
                        else:
                            m_cap = round(float(m_cap.replace(",", ""))/1000000, 2)
                        self.data[count]['basics'] = {'mc': str(m_cap)}
            except:
                self.data[count]['basics'] = {'mc': '-999'}
                pass
            count = count + 1

    def div(self):
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "quote")
                if "ERROR" in p_e:
                    self.data[count]['basics']['div'] = '-999'
                else:
                    if 'N/A' in p_e[str(list(p_e.keys())[0])]['Forward Dividend & Yield']:
                        self.data[count]['basics']['div'] = '-999'
                    else:
                        div = str(p_e[str(list(p_e.keys())[0])]['Forward Dividend & Yield'])
                        div = div.split("(")[1]
                        div = div.split("%")[0]
                        self.data[count]['basics']['div'] = str(div)
            except:
                self.data[count]['basics']['div'] = '-999'
                pass
            count = count + 1

    def beta(self):
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "quote")
                if "ERROR" in p_e:
                    self.data[count]['basics']['beta'] = '-999'
                else:
                    if 'N/A' in p_e[str(list(p_e.keys())[0])]['Beta (5Y Monthly)']:
                        self.data[count]['basics']['beta'] = '-999'
                    else:
                        beta = str(p_e[str(list(p_e.keys())[0])]['Beta (5Y Monthly)'])
                        self.data[count]['basics']['beta'] = str(beta)
            except:
                self.data[count]['basics']['beta'] = '-999'
                pass
            count = count + 1

    def price(self):
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "quote")
                if "ERROR" in p_e:
                    self.data[count]['basics']['price'] = '-999'
                else:
                    if 'N/A' in p_e[str(list(p_e.keys())[0])]['value']:
                        self.data[count]['basics']['price'] = '-999'
                    else:
                        price = str(p_e[str(list(p_e.keys())[0])]['value'])
                        self.data[count]['basics']['price'] = str(price)
            except:
                self.data[count]['basics']['price'] = '-999'
                pass
            count = count + 1

    def pt(self):
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "quote")
                if "ERROR" in p_e:
                    self.data[count]['basics']['target'] = '-999'
                else:
                    if 'N/A' in p_e[str(list(p_e.keys())[0])]['1y Target Est']:
                        self.data[count]['basics']['target'] = '-999'
                    else:
                        target = str(p_e[str(list(p_e.keys())[0])]['1y Target Est'])
                        self.data[count]['basics']['target'] = str(target)
            except:
                self.data[count]['basics']['target'] = '-999'
                pass
            count = count + 1

    def up(self):
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "quote")
                if "ERROR" in p_e:
                    self.data[count]['basics']['upside'] = '-999'
                else:
                    if 'N/A' in p_e[str(list(p_e.keys())[0])]['1y Target Est']:
                        self.data[count]['basics']['upside'] = '-999'
                    else:
                        target = float(p_e[str(list(p_e.keys())[0])]['1y Target Est'].replace(",", ""))
                        price = float(p_e[str(list(p_e.keys())[0])]['value'].replace(",", ""))
                        upside = round(((target - price)/price)*100, 2)
                        if upside>300:
                            raise Exception("Upaside over 300% - Invalid")
                        else:
                            self.data[count]['basics']['upside'] = str(upside)
            except:
                self.data[count]['basics']['upside'] = '-999'
                pass
            count = count + 1

    def pMargin(self):
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "quote")
                if "ERROR" in p_e:
                    self.data[count]['basics']['pMargin'] = '-999'
                else:
                    if 'N/A' in p_e[str(list(p_e.keys())[0])]['Profit Margin ']:
                        self.data[count]['basics']['pMargin'] = '-999'
                    else:
                        target = float(p_e[str(list(p_e.keys())[0])]['Profit Margin '].replace(",", "").replace("%", ""))
                        if target>100:
                            raise Exception("Profit margin over 100% - Invalid")
                        else:
                            self.data[count]['basics']['pMargin'] = str(target)
            except:
                self.data[count]['basics']['pMargin'] = '-999'
                pass
            count = count + 1