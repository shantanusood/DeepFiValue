from bs4 import BeautifulSoup
import pandas as p
from obj import yahoo_obj_funcs as y
import json

def getCashFlow(html, curData):
    soup = BeautifulSoup(html, 'html.parser')
    df = p.DataFrame(y.getTableData(soup, "cf"))
    curData_j = ""
    try:
        curData_j = json.loads(curData)
        curHeaders = list(dict(curData_j['TTM']).keys())
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

