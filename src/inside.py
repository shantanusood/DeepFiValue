from bs4 import BeautifulSoup
import pandas as p
from obj import yahoo_obj_funcs as y

def getInsider(html):
    soup = BeautifulSoup(html, 'html.parser')
    df = p.DataFrame(y.getTableData_inside(soup, "inside"))
    return df

