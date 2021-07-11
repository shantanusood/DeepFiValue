import os
import pandas as pd
from src.engine.types import Helpers
import traceback
import statistics as st

class DiscountedCashFlow:
    parent = ""
    subsector = ""
    data = []
    type = ""
    def __init__(self, parent, subsector, data):
        self.parent = parent
        self.subsector = subsector
        self.data = data

    def final(self):
        self.curFreeCash()
        self.wacc()
        self.terVal()
        self.curMcap()
        self.proMcap()
        self.upside()
        return str(self.data).replace("'", "\"")

    def curFreeCash(self):
        count = 0
        parent_t = ""
        for tick in self.data:
            try:
                if self.parent == "Customs":
                    if os.path.isfile('./data/tickers/Categories.csv'):
                        get_parent = pd.read_csv('./data/tickers/Categories.csv')
                        isSubsector = get_parent['Subsector'] == tick['Category']
                        parentSect = get_parent[isSubsector]
                        parent_t = str(parentSect['ParentSector'].head(1).item())
                else:
                    parent_t = self.parent
                fin = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "cf")
                rev_lst = []
                dur = []
                type = []
                for x in range(0, len(list(fin.keys()))):
                    rev_lst.append(int(str(fin[str(list(fin.keys())[x])]['Free Cash Flow']).replace(",", "")))
                    dur.append(str(fin[str(list(fin.keys())[x])]['Duration']))
                    type.append("cur")
                pro = self.projected(tick, parent_t, rev_lst)
                pro[0].extend(rev_lst)
                pro[1].extend(dur)
                pro[2].extend(type)
                rev_lst = pro[0]
                dur = pro[1]
                type = pro[2]
                self.data[count]['discountedcashflow'] = {'freecash': list(reversed(rev_lst)), 'duration': list(reversed(dur)), 'type': list(reversed(type)), 'growth': list(reversed(pro[3])), 'comTy': self.type}
            except:
                self.data[count]['discountedcashflow'] = {'freecash':  [], 'duration': [], 'type': [], 'growth': [], 'comTy': "NONE"}
                pass
            count = count + 1

    def wacc(self):
        count = 0
        for tick in self.data:
            self.data[count]['discountedcashflow']['wacc'] = '8.4'
            count = count + 1

    def terVal(self):
        count = 0
        for tick in self.data:
            cashpro = self.data[count]['discountedcashflow']['freecash']
            try:
                self.data[count]['discountedcashflow']['terVal'] = str(round((cashpro[len(cashpro)-1] * (1.025))/(float(self.data[count]['discountedcashflow']['wacc'])/100 - 0.025)))
            except:
                self.data[count]['discountedcashflow']['terVal'] = '-999'
            count = count + 1

    def curMcap(self):
        count = 0
        parent_t = ""
        for tick in self.data:
            try:
                if self.parent == "Customs":
                    if os.path.isfile('./data/tickers/Categories.csv'):
                        get_parent = pd.read_csv('./data/tickers/Categories.csv')
                        isSubsector = get_parent['Subsector'] == tick['Category']
                        parentSect = get_parent[isSubsector]
                        parent_t = str(parentSect['ParentSector'].head(1).item())
                else:
                    parent_t = self.parent
                p_e = Helpers.get_by_type(parent_t, tick['Category'], tick['Ticker'], "quote")
                if "ERROR" in p_e:
                    self.data[count]['discountedcashflow']['curMcap'] = '-999'
                else:
                    if p_e[str(list(p_e.keys())[0])]['Market Cap'] == 'N/A':
                        self.data[count]['discountedcashflow']['curMcap'] = '-999'
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
                        self.data[count]['discountedcashflow']['curMcap'] = str(m_cap)
            except:
                self.data[count]['discountedcashflow']['curMcap'] = '-999'
                pass
            count = count + 1

    def proMcap(self):
        count = 0
        factor = 1 + float(self.data[count]['discountedcashflow']['wacc'])/100
        for tick in self.data:
            try:
                vals = []
                vals = vals + self.data[count]['discountedcashflow']['freecash'][-5:]
                vals.append(int(self.data[count]['discountedcashflow']['terVal']))
                vals[0] = round(vals[0]/factor)
                vals[1] = round(vals[1]/(factor**2))
                vals[2] = round(vals[2]/(factor**3))
                vals[3] = round(vals[3]/(factor**4))
                vals[4] = round(vals[4]/(factor**5))
                vals[5] = round(vals[5]/(factor**5))
                sm = 0
                if "G" in self.data[count]['discountedcashflow']['comTy']:
                    sm = sum(vals)*1.25
                else:
                    sm = sum(vals)
                self.data[count]['discountedcashflow']['proMcap'] = str(round(sm/1000000, 2))
            except:
                self.data[count]['discountedcashflow']['proMcap'] = '-999'
            count = count + 1

    def upside(self):
        count = 0
        for tick in self.data:
            try:
                cur = float(self.data[count]['discountedcashflow']['curMcap'])
                pro = float(self.data[count]['discountedcashflow']['proMcap'])
                self.data[count]['discountedcashflow']['upside'] = str(round(((pro - cur)/cur)*100, 2))
                pass
            except:
                self.data[count]['discountedcashflow']['upside'] = '-999'
            count = count + 1

    def projected(self, tick, parent, rev_lst):
        prev = 0
        count = 0
        sum = 0
        type = self.companyType(tick, parent)
        growth = []
        if type == "SLP":
            try:
                for x in range(0, len(rev_lst)):
                    if (x+1) != len(rev_lst):
                        prev = rev_lst[x+1]
                    else:
                        break
                    sum = sum + ((rev_lst[x] - prev)/prev)
                    count = count + 1
                    if count == 4:
                        break
                sum = sum/(count*2)
                if sum*100 > 10.0:
                    sum = 0.1
                elif sum < 0:
                    sum = 0.02

                fcf = (rev_lst[0] + rev_lst[1] + rev_lst[2] + rev_lst[3])/4

                ret = [int(fcf*(1 + sum)**5), int(fcf*(1 + sum)**4), int(fcf*(1 + sum)**3), int(fcf*(1 + sum)**2), int(fcf*(1 + sum))]
                ret = ret + rev_lst
                for x in range(0, len(ret)):
                    if (x+1) != len(ret):
                        prev = ret[x+1]
                    else:
                        break
                    growth.append(round(float((ret[x] - prev)/prev)*100, 2))
                growth.append(0)
                return [[int(fcf*(1 + sum)**5), int(fcf*(1 + sum)**4), int(fcf*(1 + sum)**3), int(fcf*(1 + sum)**2), int(fcf*(1 + sum))], ['12/31/2025', '12/31/2024', '12/31/2023', '12/31/2022', '12/31/2021'], ['pro', 'pro', 'pro', 'pro', 'pro'], growth]
            except:
                pass
        elif type == "SLN":

            return [[0, 0, 0, 0, 0], ['12/31/2025', '12/31/2024', '12/31/2023', '12/31/2022', '12/31/2021'], ['pro', 'pro', 'pro', 'pro', 'pro'], growth]
        elif "SH" in type:
            quote = Helpers.get_by_type(parent, tick['Category'], tick['Ticker'], "quote")
            fin = Helpers.get_by_type(parent, tick['Category'], tick['Ticker'], "fin")
            bs = Helpers.get_by_type(parent, tick['Category'], tick['Ticker'], "bs")

            div = 0
            ni = 0
            count = 0
            shares = 0
            try:
                for x in quote:
                    div = float(str(quote[x]['Forward Dividend & Yield']).split(" ")[0])
                    break
                for x in bs:
                    shares = int(str(bs[x]['Ordinary Shares Number']).replace(",", ""))
                    break
                for x in fin:
                    ni = ni + int(str(fin[x]['Net Income Common Stockholders']).replace(",", ""))
                    count = count + 1
                    if count == 2:
                        break
                ni = ni / 3
                if ni < 0:
                    cnt = 0
                    ni = 0
                    for x in rev_lst:
                        ni = ni + x
                        cnt = cnt + 1
                        if cnt == 2:
                            break
                ni = ni / 3
                div = div * shares
                fcf = 0
                if round(div / ni, 2) * 100 > 100:
                    fcf = div
                else:
                    fcf = div + ni * (1 - round(div / ni, 2))
                if "N" in type:
                    sum = 0.02
                elif "P" in type:
                    sum = 0.05

                ret = [int(fcf * (1 + sum) ** 5), int(fcf * (1 + sum) ** 4), int(fcf * (1 + sum) ** 3),
                       int(fcf * (1 + sum) ** 2), int(fcf * (1 + sum))]
                ret = ret + rev_lst
                for x in range(0, len(ret)):
                    if (x + 1) != len(ret):
                        prev = ret[x + 1]
                    else:
                        break
                    growth.append(round(float((ret[x] - prev) / prev) * 100, 2))
                growth.append(0)
                return [[int(fcf * (1 + sum) ** 5), int(fcf * (1 + sum) ** 4), int(fcf * (1 + sum) ** 3),
                         int(fcf * (1 + sum) ** 2), int(fcf * (1 + sum))],
                        ['12/31/2025', '12/31/2024', '12/31/2023', '12/31/2022', '12/31/2021'],
                        ['pro', 'pro', 'pro', 'pro', 'pro'], growth]
            except:
                return [[0, 0, 0, 0, 0], ['12/31/2025', '12/31/2024', '12/31/2023', '12/31/2022', '12/31/2021'],
                        ['pro', 'pro', 'pro', 'pro', 'pro'], growth]

        elif type == "G0P":
            try:
                for x in range(0, len(rev_lst)):
                    if (x + 1) != len(rev_lst):
                        prev = rev_lst[x + 1]
                    else:
                        break
                    sum = sum + ((rev_lst[x] - prev) / prev)
                    count = count + 1
                    if count == 4:
                        break
                sum = sum / count
                if sum * 100 > 20.0:
                    sum = 0.20
                elif sum < 0:
                    sum = 0.08

                fcf = (rev_lst[0] + rev_lst[1] + rev_lst[2] + rev_lst[3]) / 4

                ret = [int(fcf * (1 + sum) ** 5), int(fcf * (1 + sum) ** 4), int(fcf * (1 + sum) ** 3),
                       int(fcf * (1 + sum) ** 2), int(fcf * (1 + sum))]
                ret = ret + rev_lst
                for x in range(0, len(ret)):
                    if (x + 1) != len(ret):
                        prev = ret[x + 1]
                    else:
                        break
                    growth.append(round(float((ret[x] - prev) / prev) * 100, 2))
                growth.append(0)
                return [[int(fcf * (1 + sum) ** 5), int(fcf * (1 + sum) ** 4), int(fcf * (1 + sum) ** 3),
                         int(fcf * (1 + sum) ** 2), int(fcf * (1 + sum))],
                        ['12/31/2025', '12/31/2024', '12/31/2023', '12/31/2022', '12/31/2021'],
                        ['pro', 'pro', 'pro', 'pro', 'pro'], growth]
            except:
                pass
        elif type == "G0N":
            return [[0, 0, 0, 0, 0], ['12/31/2025', '12/31/2024', '12/31/2023', '12/31/2022', '12/31/2021'], ['pro', 'pro', 'pro', 'pro', 'pro'], growth]
        elif type == "NONE":
            return [[0, 0, 0, 0, 0], ['12/31/2025', '12/31/2024', '12/31/2023', '12/31/2022', '12/31/2021'], ['pro', 'pro', 'pro', 'pro', 'pro'], growth]
        else:
            return [[], [], [], []]

    def companyType(self, tick, parent):
        self.type = ""
        quote = Helpers.get_by_type(parent, tick['Category'], tick['Ticker'], "quote")
        fin = Helpers.get_by_type(parent, tick['Category'], tick['Ticker'], "fin")
        bs = Helpers.get_by_type(parent, tick['Category'], tick['Ticker'], "bs")
        cf = Helpers.get_by_type(parent, tick['Category'], tick['Ticker'], "cf")

        rev_lst = []
        try:
            for x in range(1, len(list(fin.keys()))):
                try:
                    rev_lst.append(int(str(fin[str(list(fin.keys())[x])]['Total Revenue']).replace(",", "")))
                except:
                    rev_lst.append(0)
            changes = []
            count = 0
            for x in range(0, len(rev_lst)):
                try:
                    changes.append(round((rev_lst[x] - rev_lst[x + 1])*100/rev_lst[x + 1], 2))
                except:
                    changes.append(0)
                count = count + 1
                if count==4:
                    break

            changes.sort(reverse=True)
            if len(changes) == 4:
                changes = changes[:3]
            else:
                changes = changes[:2]

            if st.mean(changes) > 20:
                self.type = self.type + "G0"
            else:
                self.type = self.type + "S"

            div = 0
            ni = 0
            count = 0
            shares = 0
            for x in quote:
                div_val = str(quote[x]['Forward Dividend & Yield']).split(" ")
                if "N/A" in div_val:
                    div = 0
                else:
                    div = float(str(quote[x]['Forward Dividend & Yield']).split(" ")[0])
                break
            for x in bs:
                shares = int(str(bs[x]['Ordinary Shares Number']).replace(",", ""))
                break
            for x in fin:
                ni = ni + int(str(fin[x]['Net Income Common Stockholders']).replace(",", ""))
                count = count + 1
                if count == 1:
                    break
            ni = ni / 2
            div = div * shares
            if round(div / ni, 2)*100 > 100 and "G" not in self.type:
                self.type = self.type + "H"
            elif round(div / ni, 2)*100 <= 100 and "G" not in self.type:
                self.type = self.type + "L"

            neg_caf = 0
            neg_caf_val = 0
            neg_caf_cnt = 0
            for x in cf:
                neg_caf_val = neg_caf_val + int(str(cf[x]['Free Cash Flow']).replace(",", ""))
                if int(str(cf[x]['Free Cash Flow']).replace(",", "")) < 0:
                    neg_caf = neg_caf + 1
                neg_caf_cnt = neg_caf_cnt + 1
                if neg_caf_cnt == 4:
                    break

            if neg_caf >= 2 or neg_caf_val < 0:
                self.type = self.type + "N"
            else:
                self.type = self.type + "P"
            if len(self.type) < 3:
                self.type = "NONE"
                return self.type
            return self.type
        except:
            print(tick['Ticker'])
            traceback.print_exc()
            self.type = "NONE"
            return self.type
#We need 3 things for doing this calculations:
#   1. Free cash flow projections
#   2. WACC (weighted average cost of capital) & Perpectual growth rate of free cash flow (2.5%)
#   3. Terminal value