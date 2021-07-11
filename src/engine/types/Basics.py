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
        self.tpe()
        self.fpe()
        self.ps()
        self.pb()
        self.pf()
        self.pMargin()
        self.opMargin()
        self.retOnAsset()
        self.retOnEquity()
        self.evToRev()
        self.evToEbitda()
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
                    self.data[count]['basics']['pMar'] = '-999'
                else:
                    if 'N/A' in p_e[str(list(p_e.keys())[0])]['Profit Margin ']:
                        self.data[count]['basics']['pMar'] = '-999'
                    else:
                        target = float(p_e[str(list(p_e.keys())[0])]['Profit Margin '].replace(",", "").replace("%", ""))
                        if target>100:
                            raise Exception("Profit margin over 100% - Invalid")
                        else:
                            self.data[count]['basics']['pMar'] = str(target)
            except:
                self.data[count]['basics']['pMar'] = '-999'
                pass
            count = count + 1

    def opMargin(self):
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
                    self.data[count]['basics']['opMar'] = '-999'
                else:
                    if 'N/A' in p_e[str(list(p_e.keys())[0])]['Operating Margin (ttm)']:
                        self.data[count]['basics']['opMar'] = '-999'
                    else:
                        target = float(
                            p_e[str(list(p_e.keys())[0])]['Operating Margin (ttm)'].replace(",", "").replace("%", ""))
                        if target > 100:
                            raise Exception("Operating margin over 100% - Invalid")
                        else:
                            self.data[count]['basics']['opMar'] = str(target)
            except:
                self.data[count]['basics']['opMar'] = '-999'
                pass
            count = count + 1

    def retOnAsset(self):
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
                    self.data[count]['basics']['retAs'] = '-999'
                else:
                    if 'N/A' in p_e[str(list(p_e.keys())[0])]['Return on Assets (ttm)']:
                        self.data[count]['basics']['retAs'] = '-999'
                    else:
                        target = float(
                            p_e[str(list(p_e.keys())[0])]['Return on Assets (ttm)'].replace(",", "").replace("%", ""))
                        if target > 100:
                            raise Exception("Return on asset over 100% - Invalid")
                        else:
                            self.data[count]['basics']['retAs'] = str(target)
            except:
                self.data[count]['basics']['retAs'] = '-999'
                pass
            count = count + 1

    def retOnEquity(self):
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
                    self.data[count]['basics']['retEq'] = '-999'
                else:
                    if 'N/A' in p_e[str(list(p_e.keys())[0])]['Return on Equity (ttm)']:
                        self.data[count]['basics']['retEq'] = '-999'
                    else:
                        target = float(
                            p_e[str(list(p_e.keys())[0])]['Return on Equity (ttm)'].replace(",", "").replace("%", ""))
                        if target > 100:
                            raise Exception("Return on asset over 100% - Invalid")
                        else:
                            self.data[count]['basics']['retEq'] = str(target)
            except:
                self.data[count]['basics']['retEq'] = '-999'
                pass
            count = count + 1

    def fpe(self):
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "ks")
                if "ERROR" in p_e:
                    self.data[count]['basics']['fpe'] = '-999'
                else:
                    if p_e['Current']['Forward P/E 1'] == 'N/A':
                        self.data[count]['basics']['fpe'] = '-999'
                    else:
                        self.data[count]['basics']['fpe'] = p_e['Current']['Forward P/E 1']
            except:
                self.data[count]['basics']['fpe'] = '-999'
                pass
            count = count + 1

    def tpe(self):
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "ks")
                if "ERROR" in p_e:
                    self.data[count]['basics']['tpe'] = '-999'
                else:
                    if p_e['Current']['Trailing P/E '] == 'N/A':
                        self.data[count]['basics']['tpe'] = '-999'
                    else:
                        self.data[count]['basics']['tpe'] = p_e['Current']['Trailing P/E ']
            except:
                self.data[count]['basics']['tpe'] = '-999'
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "ks")
                if "ERROR" in p_e:
                    self.data[count]['basics']['ps'] = '-999'
                else:
                    if p_e['Current']['Price/Sales (ttm)'] == 'N/A':
                        self.data[count]['basics']['ps'] = '-999'
                    else:
                        self.data[count]['basics']['ps'] = p_e['Current']['Price/Sales (ttm)']
            except:
                self.data[count]['basics']['ps'] = '-999'
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "ks")
                if "ERROR" in p_e:
                    self.data[count]['basics']['pb'] = '-999'
                else:
                    if p_e['Current']['Price/Book (mrq)'] == 'N/A':
                        self.data[count]['basics']['pb'] = '-999'
                    else:
                        self.data[count]['basics']['pb'] = p_e['Current']['Price/Book (mrq)']
            except:
                self.data[count]['basics']['pb'] = '-999'
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
                self.data[count]['basics']['pf'] = str(round(float(m_cap / fin), 2))
            except:
                self.data[count]['basics']['pf'] = str("-999")
                pass
            count = count + 1

    def evToRev(self):
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "ks")
                if "ERROR" in p_e:
                    self.data[count]['basics']['evRev'] = '-999'
                else:
                    if p_e['Current']['Enterprise Value/Revenue 3'] == 'N/A':
                        self.data[count]['basics']['evRev'] = '-999'
                    else:
                        self.data[count]['basics']['evRev'] = p_e['Current']['Enterprise Value/Revenue 3']
            except:
                self.data[count]['basics']['evRev'] = '-999'
                pass
            count = count + 1

    def evToEbitda(self):
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
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "ks")
                if "ERROR" in p_e:
                    self.data[count]['basics']['evEbit'] = '-999'
                else:
                    if p_e['Current']['Enterprise Value/EBITDA 7'] == 'N/A':
                        self.data[count]['basics']['evEbit'] = '-999'
                    else:
                        self.data[count]['basics']['evEbit'] = p_e['Current']['Enterprise Value/EBITDA 7']
            except:
                self.data[count]['basics']['evEbit'] = '-999'
                pass
            count = count + 1