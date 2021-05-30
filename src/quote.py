from bs4 import BeautifulSoup
import pandas as pd
from obj import yahoo_obj as y
from src.helpers import commons as cm
import os
from data import tickers_list as tl
import traceback

def getQuote(input):
    df_list = {}
    if "_" in input:
        count = 0
        details = []
        if os.path.isfile('./data/tickers/'+input[0:int(input.index("_"))] + '.csv'):
            details = tl.ticker_details(input)
        for i in tl.tickers(input):
            resp = cm.getHtml("quote", i)
            try:
                if resp[0] == 200:
                    df = parse(resp[1])
                    pd.set_option('display.max_rows', 5, 'display.max_columns', 100)
                    #print("Quote for: {} ".format(i), end='')
                    if len(details)>count:
                        #print(details[count])
                        df_list[str(details[count])] = df
                    else:
                        df_list[i] = df
                        #print("No Details available")
                    #print(df)
            except:
                print("Exception occured while getting quote for: {0}".format(i))
                traceback.print_exc()
            finally:
                count = count + 1
        return df_list
    else:
        resp = cm.getHtml("quote", input)
        resp_ks = cm.getHtml("ks", input)
        if resp[0] == 200 and resp_ks[0] == 200:
            df = parse(resp[1])
            df2 = parse_ks(resp_ks[1])
            pd.set_option('display.max_rows', 5, 'display.max_columns', 100)
            return pd.concat([df, df2], axis=1, join="inner")
    return df_list

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    dict = {'value':soup.select(y.current_value())[0].text}
    l = soup.select(y.quote_table())
    data = [j.text for j in l]
    for i in range(0, len(data), 2):
        dict[data[i]] = data[i+1:i+2]

    df = pd.DataFrame(dict)
    return df

def parse_ks(html):
    soup = BeautifulSoup(html, 'html.parser')
    prof_d = {}
    manage_d = {}
    income_d = {}
    balance_d = {}
    cash_d = {}
    share_d = {}
    div_d = {}
    profitability = [j.text for j in soup.select(y.ks_stats_tables(3, 2))]
    for i in range(0, len(profitability), 2):
        prof_d[profitability[i]] = profitability[i + 1:i + 2]
    df_prof = pd.DataFrame(prof_d)
    management_ffectiveness = [j.text for j in soup.select(y.ks_stats_tables(3, 3))]
    for i in range(0, len(management_ffectiveness), 2):
        manage_d[management_ffectiveness[i]] = management_ffectiveness[i + 1:i + 2]
    df_manage = pd.DataFrame(manage_d)
    income_statement = [j.text for j in soup.select(y.ks_stats_tables(3, 4))]
    for i in range(0, len(income_statement), 2):
        income_d[income_statement[i]] = income_statement[i + 1:i + 2]
    df_income = pd.DataFrame(income_d)
    balance_sheet = [j.text for j in soup.select(y.ks_stats_tables(3, 5))]
    for i in range(0, len(balance_sheet), 2):
        balance_d[balance_sheet[i]] = balance_sheet[i + 1:i + 2]
    df_balance = pd.DataFrame(balance_d)
    cash_flow = [j.text for j in soup.select(y.ks_stats_tables(3, 6))]
    for i in range(0, len(cash_flow), 2):
        cash_d[cash_flow[i]] = cash_flow[i + 1:i + 2]
    df_cash = pd.DataFrame(cash_d)
    share_stats = [j.text for j in soup.select(y.ks_stats_tables(2, 2))]
    for i in range(0, len(share_stats), 2):
        share_d[share_stats[i]] = share_stats[i + 1:i + 2]
    df_share = pd.DataFrame(share_d)
    div = [j.text for j in soup.select(y.ks_stats_tables(2, 3))]
    for i in range(0, len(div), 2):
        div_d[div[i]] = div[i + 1:i + 2]
    df_div = pd.DataFrame(div_d)
    return pd.concat([df_prof, df_manage, df_income, df_balance, df_cash, df_share, df_div], axis=1, join="inner")
