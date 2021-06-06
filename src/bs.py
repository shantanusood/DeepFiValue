from bs4 import BeautifulSoup
from obj import yahoo_obj_funcs as y
import pandas as p
import json
import traceback as t

def getBalanceSheet(html, curData):
    soup = BeautifulSoup(html, 'html.parser')
    df = p.DataFrame(y.getTableData(soup, "bs"))
    curData_j = ""
    try:
        curData_j = json.loads(curData)
        curHeaders = list(dict(curData_j[str(next(iter(dict(curData_j))))]).keys())
        preHeaders = list(df.columns.values)
        not_in_cur = []
        not_in_pre = []

        for x in preHeaders:
            if x not in curHeaders:
                not_in_cur.append(x)

        for x in curHeaders:
            if x not in preHeaders:
                not_in_pre.append(x)

        curData_j = dict(curData_j)
        for x in not_in_cur:
            for z in curData_j.keys():
                curData_j[z][str(x)] = "-"

        for x in not_in_pre:
            df[x] = '-'
        curData_j = json.dumps(curData_j)
    except:
        pass

    lst = [df, str(curData_j)]
    return lst


