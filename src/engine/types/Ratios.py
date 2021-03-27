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
        self.pe()
        self.ps()
        self.pb()
        self.pf()
        return str(self.data).replace("'", "\"")

    def pe(self):
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
                    self.data[count]['ratios'] = {'pe': '-999'}
                else:
                    if p_e[str(list(p_e.keys())[0])]['PE Ratio (TTM)'] == 'N/A':
                        self.data[count]['ratios'] = {'pe': '-999'}
                    else:
                        self.data[count]['ratios'] = {'pe': p_e[str(list(p_e.keys())[0])]['PE Ratio (TTM)']}
            except:
                self.data[count]['ratios'] = {'pe': '-999'}
                pass
            count = count + 1

    def ps(self):
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
                quote = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "quote")
                m_cap = str(quote[str(list(quote.keys())[0])]['Market Cap'])
                if "T" in m_cap:
                    m_cap = int(float(m_cap.replace("T", ""))*1000000000000)
                elif "B" in m_cap:
                    m_cap = int(float(m_cap.replace("B", ""))*1000000000)
                elif "M" in m_cap:
                    m_cap = int(float(m_cap.replace("M", ""))*1000000)
                fin = int(str(Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "fin")['TTM']['Total Revenue']).replace(",", ""))*1000
                self.data[count]['ratios']['ps'] = str(round(float(m_cap/fin), 2))
            except:
                self.data[count]['ratios']['ps'] = str("-999")
                pass
            count = count + 1

    def pb(self):
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
                quote = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "quote")
                m_cap = str(quote[str(list(quote.keys())[0])]['Market Cap'])
                if "T" in m_cap:
                    m_cap = int(float(m_cap.replace("T", "")) * 1000000000000)
                elif "B" in m_cap:
                    m_cap = int(float(m_cap.replace("B", "")) * 1000000000)
                elif "M" in m_cap:
                    m_cap = int(float(m_cap.replace("M", "")) * 1000000)
                bs = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "bs")
                bs = bs[str(list(bs.keys())[0])]
                fin = int(str(bs['Total Equity Gross Minority Interest']).replace(",", "")) * 1000
                self.data[count]['ratios']['pb'] = str(round(float(m_cap / fin), 2))
            except:
                self.data[count]['ratios']['pb'] = str("-999")
                pass
            count = count + 1

    def pf(self):
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
                quote = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "quote")
                m_cap = str(quote[str(list(quote.keys())[0])]['Market Cap'])
                if "T" in m_cap:
                    m_cap = int(float(m_cap.replace("T", "")) * 1000000000000)
                elif "B" in m_cap:
                    m_cap = int(float(m_cap.replace("B", "")) * 1000000000)
                elif "M" in m_cap:
                    m_cap = int(float(m_cap.replace("M", "")) * 1000000)
                cf = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "cf")['TTM']
                fin = int(str(cf['Free Cash Flow']).replace(",", "")) * 1000
                self.data[count]['ratios']['pf'] = str(round(float(m_cap / fin), 2))
            except:
                self.data[count]['ratios']['pf'] = str("-999")
                pass
            count = count + 1