from flask import Flask, request, redirect, url_for, render_template, Response
import json
import os
from flask_cors import CORS
from data.Indicators import Indicators
from src.engine.Decide import Decide
from bs4 import BeautifulSoup
import pandas as pd
from data import tickers_list as t
from src import filter as f
import script as s
import traceback
from datetime import datetime
import csv
import re
from requests import get
import numpy as np

app = Flask(__name__)
CORS(app)

#Resources:

#Insider buyers:
#       http://openinsider.com/search?q=<TICKER>
#		https://whalewisdom.com/stock/<TICKER>

#General info:
#		https://stockcharts.com/freecharts/symbolsummary.html?sym=<TICKER>
#		https://seekingalpha.com/symbol/<TICKER>

#Corporate debt:
#		https://finra-markets.morningstar.com/BondCenter/



#Financials			XLK
#Technology			XLF
#Health Care			XLV
#Consumer Discretionary		XLY
#Industrials			XLI
#Energy				XLE
#Consumer Staples		XLP
#Communications			XLC
#Utilities			XLU
#Materials			XLB
#Real Estate			XLRE
#Transportation			XTN
#Commodity			GLD

#Ways to value a company:
#   > Price to earnings multiple (profitable companies)
#   > Discounted free cash flow
#   > Enterprise value / EBITDA or Revenue (For younger non profitable companies)
#   > Sum of the parts

# PEG ratio
# Key statistics: https://finance.yahoo.com/quote/<TICKER>/key-statistics/

#####################################################################################################################
############################################## WEB DATA FETCH SERVICE ###############################################
#####################################################################################################################
@app.route('/')
def quide():
    return render_template('template.html')

@app.route('/indicators/<type>')
def indicators_data(type):
    data = []
    indicators = Indicators(type)
    soup = BeautifulSoup(str(indicators.getData()[0]), 'html.parser')
    rows = soup.find('tbody').find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip().replace('%', '') for ele in cols]
        data.append([ele for ele in cols if ele])
    normalize = {}
    for x in data:
        normalize[x[0]] = x[1]
    return str(normalize).replace("'", "\"")

@app.route('/data/<filter>/<tickers>')
def quote(filter, tickers):
    ret = s.main(filter, tickers)
    ret_dict = {}
    dates = []
    ret_dict_sync = {}
    ret_dict_sync_tm = {}
    if isinstance(ret, pd.DataFrame):
        ret_dict = ret.to_dict()
        if filter == 'quote':
            for x in ret_dict.keys():
                ret_dict_sync[str(x)] = ret_dict[x][0]
            ret_dict_sync_tm[str(datetime.today().strftime('%m/%d/%Y'))] = ret_dict_sync
        elif filter == 'inside':
            ret_dict = ret.to_dict()
            for x in ret_dict['FILE DATE']:
                dates.append(ret_dict['FILE DATE'][x])
            ret_dict.pop('FILE DATE')
            dur = []
            for y in ret_dict.keys():
                dur.append(y)
                ret_dict_sync['Date'] = dur
            count = 0
            name = []
            title = []
            date = []
            trans = []
            share = []
            price = []
            amt = []
            for x in dates:
                name.append(ret_dict['INSIDER NAME'][count])
                title.append(ret_dict['TITLE'][count])
                date.append(ret_dict['DATE'][count])
                trans.append(ret_dict['TRANSATION'][count])
                share.append(ret_dict['SHARE'][count])
                price.append(ret_dict['PRICE'][count])
                amt.append(ret_dict['AMOUNT'][count])
                count = count + 1
            final = []
            count_ = 0
            for y in dates:
                final.append(name[count_])
                final.append(title[count_])
                final.append(date[count_])
                final.append(trans[count_])
                final.append(share[count_])
                final.append(price[count_])
                final.append(amt[count_])
                ret_dict_sync[y] = final
                final = []
                count_ = count_ + 1
            ret_dict_sync_tm = ret_dict_sync
        else:
            for x in ret_dict['Duration'].keys():
                for y in ret_dict.keys():
                    ret_dict_sync[str(y)] = ret_dict[str(y)][x]
                ret_dict_sync_tm[str(ret_dict['Duration'][x])] = ret_dict_sync
                ret_dict_sync = {}
        return str(ret_dict_sync_tm).replace("'", "\"")
    else:
        return str("{'res': 'ERROR: Unable to sync data for: " + filter + " > " + tickers + "'}").replace("'", "\"")

@app.route('/csv/<type>')
def csvData(type):
    filename = './data/tickers/' + type + '.csv'
    return pd.read_csv(filename).head(10000).to_csv()

@app.route('/data/metadata/stocks/<country>/<parent>/<category>')
def stocksBySector(country, parent, category):
    metadata = []
    metadata_agg = ""
    category = str(category).replace("+", " ")
    get_parent = ""
    if str(parent) == "Customs":
        if os.path.isfile('./data/tickers/Stocks.csv'):
            metadata = t.ticker_details("Stocks")
        tickers = []
        data = []
        with open('./data/sectors/Customs/'+str(category)+'.csv', newline='') as f:
            reader = csv.reader(f)
            tickers = list(reader)[0]
        for ticks in tickers:
            is_country = metadata['Country'] == str(country)
            is_category = metadata['Ticker'] == str(ticks)
            metadata_country = metadata[is_country]
            metadata_category = metadata_country[is_category]
            data.append(metadata_category.to_json(orient='records', lines=True))
        return str(data).replace("'", "").replace("\\\\", "")
    else:
        if os.path.isfile('./data/tickers/Categories.csv'):
            get_parent = pd.read_csv('./data/tickers/Categories.csv')
        isParent = get_parent['ParentSector'] == str(parent)
        parentSect = get_parent[isParent]
        categories = parentSect['Subsector']
        if category == 'All':
            if os.path.isfile('./data/tickers/Stocks.csv'):
                metadata = t.ticker_details("Stocks")
            for x in categories:
                is_country = metadata['Country'] == str(country)
                is_category = metadata['Category'] == str(x)
                metadata_country = metadata[is_country]
                metadata_category = metadata_country[is_category]
                metadata_agg = metadata_agg + str(metadata_category.to_json(orient='records', lines=True).replace('}', '},')).replace("'", "\"")
            return "["+metadata_agg[:-1].replace("'", "\"")+"]"
        else:
            if os.path.isfile('./data/tickers/Stocks.csv'):
                metadata = t.ticker_details("Stocks")
            is_country = metadata['Country'] == str(country)
            is_category = metadata['Category'] == str(category)
            metadata_country = metadata[is_country]
            metadata_category = metadata_country[is_category]
            return "["+str(metadata_category.to_json(orient='records', lines=True).replace('}', '},'))[:-1].replace("'", "\"")+"]"

@app.route('/data/cik/<ticker>')
def get_cik_ticker(ticker):
    return str(getCIK(ticker)).replace("'", "\"")

#####################################################################################################################
############################################# LOCAL DATA FETCH SERVICE ##############################################
#####################################################################################################################
@app.route('/data/get/<parent>/<subsector>/<ticker>/<type>')
def data_get(parent, subsector, ticker, type):
    filename = './data/sectors/' + str(parent).replace(" ", "_") + "/" + subsector + '.json'
    getData = {}
    data = []
    try:
        with open(filename, 'r') as data_file:
            data = json.loads(data_file.read())
            count = 0
            isFound = False
            for x in data:
                tick_jsons = dict(x)
                if list(tick_jsons.keys())[0].lower() == str(ticker).lower():
                    getData = data[count][str(ticker)][str(type)]
                    isFound = True
                    break
                count = count + 1
            if isFound == False:
                return str("{'res': 'ERROR: Data not yet synced for: " + parent + " > " + subsector + " > " + ticker + " > " + type + "'}")
        return str(getData).replace("'", "\"")
    except:
        traceback.print_exc()
        return str("{'res' :'ERROR: Data get failed for: " + parent + " > " + subsector + " > " + ticker + " > " + type + "'}").replace("'", "\"")

@app.route('/data/getSectors')
def getSectors():
    sectors = {}
    parent = []
    count = 0
    for path, dirnames, filenames in os.walk('./data/sectors'):
        if count == 0:
            parent = [str(x).replace("_", " ") for x in list(dirnames)]
        else:
            files = list(filenames)
            files = [str(f).split(".")[0] for f in files]
            sectors[parent[count - 1]] = files
        count = count + 1
    return str(sectors).replace("'", "\"")

@app.route('/data/getSubSectors/<parent>')
def getSubSectors(parent):
    get_parent = ""
    if str(parent) == "Customs":
        for filenames in os.walk('./data/sectors/Customs'):
            for f in filenames:
                if isinstance(f, list):
                    if len(f) > 0:
                        return str([x.split(".")[0] for x in f]).replace("'", "\"")
            break
        return "[]"
    else:
        if os.path.isfile('./data/tickers/Categories.csv'):
            get_parent = pd.read_csv('./data/tickers/Categories.csv')
        is_sub = get_parent['ParentSector'] == str(parent)
        return str(get_parent[is_sub]['Subsector'].to_list()).replace("'", "\"")

#####################################################################################################################
################################################ DATA SYNC SERVICE ##################################################
#####################################################################################################################
@app.route('/data/sync/dump/<parent>/<subsector>/<ticker>/<type>', methods=['GET', 'POST'])
def data_sync_dump(parent, subsector, ticker, type):
    filename = './data/sectors/' + str(parent).replace(" ", "_") + "/" + subsector + '.json'
    addData = request.json
    f = ""
    data = []
    try:
        if os.path.isfile(filename):
            f = open(filename, "r")
        else:
            f = open(filename, "x")
            f.write("[]")
            f.close()
        with open(filename, 'r') as data_file:
            data = json.loads(data_file.read())
            count = 0
            isFound = False
            tick_jsons = {}
            for x in data:
                tick_jsons = dict(x)
                if list(tick_jsons.keys())[0] == str(ticker):
                    data[count][str(ticker)][str(type)] = addData
                    isFound = True
                    break
                count = count + 1
            if isFound == False:
                type_jsons = {str(type): addData}
                tick_jsons = {str(ticker): type_jsons}
                data.append(tick_jsons)
        with open(filename, 'w') as data_file:
            data_file.write(str(data).replace("'", "\""))

        r_row = []
        with open('./data/tickers/Stocks.csv', 'r') as in_file:
            r_row = list(csv.reader(in_file))
        with open('./data/tickers/Stocks.csv', 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            for row in r_row:
                if row[0] == ticker:
                    if type == 'quote':
                        row[5] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'ks':
                        row[6] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'fin':
                        row[7] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'bs':
                        row[8] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'cf':
                        row[9] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'inside':
                        row[10] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'bonds':
                        row[11] = str(datetime.today().strftime('%m/%d/%Y'))
                if row:
                    writer.writerow(row)
        return str(data).replace("'", "\"")
    except:
        traceback.print_exc()
        str("{'res': 'ERROR: Data sync dump failed for: " + parent + " > " + subsector + " > " + type + "'}").replace("'", "\"")

@app.route('/data/sync/update/<parent>/<subsector>/<ticker>/<type>', methods=['GET', 'POST'])
def data_sync_update(parent, subsector, ticker, type):
    filename = './data/sectors/' + str(parent).replace(" ", "_") + "/" + subsector + '.json'
    addData = request.json
    f = ""
    data = []
    try:
        with open(filename, 'r') as data_file:
            data = json.loads(data_file.read())
            count = 0
            tick_jsons = {}
            for x in data:
                tick_jsons = dict(x)
                if list(tick_jsons.keys())[0] == str(ticker):
                    tm_data_incoming = list(addData.keys())
                    for i in tm_data_incoming:
                        if 'quote' in str(type):
                            data[count][str(ticker)][str(type)] = {str(i) : addData[str(i)]}
                        else:
                            data[count][str(ticker)][str(type)][str(i)] = addData[str(i)]
                    break
                count = count + 1
        with open(filename, 'w', encoding="utf-8") as data_file:
            data_file.write(str(data).replace("'", "\""))

        r_row = []
        with open('./data/tickers/Stocks.csv', 'r') as in_file:
            r_row = list(csv.reader(in_file))
        with open('./data/tickers/Stocks.csv', 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            for row in r_row:
                if row[0] == ticker:
                    if type == 'quote':
                        row[5] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'ks':
                        row[6] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'fin':
                        row[7] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'bs':
                        row[8] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'cf':
                        row[9] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'inside':
                        row[10] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'bonds':
                        row[11] = str(datetime.today().strftime('%m/%d/%Y'))
                if row:
                    writer.writerow(row)
        return str(data).replace("'", "\"")
    except:
        traceback.print_exc()
        return str("{'res': 'ERROR: Data sync update failed for: " + parent + " > " + subsector + " > " + type + "'}").replace("'", "\"")

@app.route('/data/sync/sector/<parent>/<subsector>/<type>')
def data_sync_sector(parent, subsector, type):
    metadata = []
    metadata_country = []
    metadata_category = []
    tickers = []
    metadata_agg = ""
    failed = []
    try:
        if os.path.isfile('./data/tickers/Stocks.csv'):
            metadata = t.ticker_details("Stocks")
        else:
            pass
        is_country = metadata['Country'] == "USA"
        metadata_country = metadata[is_country]
        is_category = metadata['Category'] == str(subsector)
        metadata_category = metadata_country[is_category]
        tickers = list(metadata_category['Ticker'])

        for x in tickers:
            try:
                toSync = quote(type, x)
                checkData = data_get(parent, subsector, x, type)
                if "ERROR" in str(checkData):
                    data_sync_dump_in(parent, subsector, x, type, json.loads(toSync))
                else:
                    data_sync_update_in(parent, subsector, x, type, json.loads(toSync))
            except:
                print("**Failed Synced ticker: " + x)
                failed.append(x)
        if len(failed) == 0:
            return str("{'res': 'All tickers synced successfully'}").replace("'", "\"").replace("'", "\"")
        else:
            print(failed)
            str_failed = str(failed).replace("'", "")
            print(str_failed)
            print(str("{'res': 'ERROR: These tickers did not sync: " + str_failed + "'}").replace("'", "\""))
            return str("{'res': 'ERROR: These tickers did not sync: " + str_failed + "'}").replace("'", "\"")
    except:
        return str("{'res': 'Some ERROR occured while syncing'}").replace("'", "\"")

@app.route('/data/sync/indicators/<parent>/<subsector>/<type>', methods=["GET", "POST"])
def data_sync_indicators(parent, subsector, type):
    filename = './data/sectors/Indicators/indicators.json'
    addData = dict(request.json)
    f = ""
    data = []
    try:
        if os.path.isfile(filename):
            f = open(filename, "r")
        else:
            f = open(filename, "x")
            f.write("[]")
            f.close()
        with open(filename, 'r') as data_file:
            data = json.loads(data_file.read())
            count = 0
            isFound = False
            tick_jsons = {}
            for x in data:
                tick_jsons = dict(x)
                if list(tick_jsons.keys())[0] == str(subsector):
                    for k in addData:
                        data[count][str(subsector)][str(type)][k] = addData[k]
                    isFound = True
                    break
                count = count + 1
            if isFound == False:
                type_jsons = {str(type): addData}
                tick_jsons = {str(subsector): type_jsons}
                data.append(tick_jsons)
        with open(filename, 'w') as data_file:
            data_file.write(str(data).replace("'", "\""))

        r_row = []
        with open('./data/tickers/Stocks.csv', 'r') as in_file:
            r_row = list(csv.reader(in_file))
        with open('./data/tickers/Stocks.csv', 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            for row in r_row:
                if row[0] == subsector:
                    if type == 'quote':
                        row[5] = str(datetime.today().strftime('%m/%d/%Y'))
                if row:
                    writer.writerow(row)
        return str(data).replace("'", "\"")
    except:
        traceback.print_exc()
        return str("{'res': 'ERROR: Data sync dump failed for: " + parent + " > " + subsector + " > " + type + "'}").replace("'", "\"")

#####################################################################################################################
################################################# HELPER FUNCTIONS ##################################################
#####################################################################################################################

def getMetadata(input):
    metadata = []
    if "_" in input:
        if os.path.isfile('./data/'+input[0:int(input.index("_"))] + '.csv'):
            metadata = t.ticker_details(input)
    return metadata

def data_sync_dump_in(parent, subsector, ticker, type, data):
    filename = './data/sectors/' + str(parent).replace(" ", "_") + "/" + subsector + '.json'
    addData = data
    f = ""
    data = []
    try:
        if os.path.isfile(filename):
            f = open(filename, "r")
        else:
            f = open(filename, "x")
            f.write("[]")
            f.close()
        with open(filename, 'r') as data_file:
            data = json.loads(data_file.read())
            count = 0
            isFound = False
            tick_jsons = {}
            for x in data:
                tick_jsons = dict(x)
                if list(tick_jsons.keys())[0] == str(ticker):
                    data[count][str(ticker)][str(type)] = addData
                    isFound = True
                    break
                count = count + 1
            if isFound == False:
                type_jsons = {str(type): addData}
                tick_jsons = {str(ticker): type_jsons}
                data.append(tick_jsons)
        with open(filename, 'w') as data_file:
            data_file.write(str(data).encode("ascii", errors="ignore").decode().replace("'", "\""))

        r_row = []
        with open('./data/tickers/Stocks.csv', 'r') as in_file:
            r_row = list(csv.reader(in_file))
        with open('./data/tickers/Stocks.csv', 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            for row in r_row:
                if row[0] == ticker:
                    if type == 'quote':
                        row[5] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'ks':
                        row[6] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'fin':
                        row[7] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'bs':
                        row[8] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'cf':
                        row[9] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'inside':
                        row[10] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'bonds':
                        row[11] = str(datetime.today().strftime('%m/%d/%Y'))
                if row:
                    writer.writerow(row)
        return str(data).replace("'", "\"")
    except:
        traceback.print_exc()
        return str("{'res':'ERROR: Data sync dump failed for: " + parent + " > " + subsector + " > " + ticker + " > " + type + "'}").replace("'", "\"")

def data_sync_update_in(parent, subsector, ticker, type, data):
    filename = './data/sectors/' + str(parent).replace(" ", "_") + "/" + subsector + '.json'
    addData = data
    f = ""
    data = []
    try:
        with open(filename, 'r') as data_file:
            data = json.loads(data_file.read())
            count = 0
            tick_jsons = {}
            for x in data:
                tick_jsons = dict(x)
                if list(tick_jsons.keys())[0] == str(ticker):
                    tm_data_incoming = list(addData.keys())
                    for i in tm_data_incoming:
                        if 'quote' in str(type):
                            data[count][str(ticker)][str(type)] = {str(i): addData[str(i)]}
                        else:
                            data[count][str(ticker)][str(type)][str(i)] = addData[str(i)]
                    break
                count = count + 1
        with open(filename, 'w', encoding="utf-8") as data_file:
            data_file.write(str(data).replace("'", "\""))

        r_row = []
        with open('./data/tickers/Stocks.csv', 'r') as in_file:
            r_row = list(csv.reader(in_file))
        with open('./data/tickers/Stocks.csv', 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            for row in r_row:
                if row[0] == ticker:
                    if type == 'quote':
                        row[5] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'ks':
                        row[6] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'fin':
                        row[7] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'bs':
                        row[8] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'cf':
                        row[9] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'inside':
                        row[10] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'bonds':
                        row[11] = str(datetime.today().strftime('%m/%d/%Y'))
                if row:
                    writer.writerow(row)
        return str(data).replace("'", "\"")
    except:
        traceback.print_exc()
        return str("{'res':'ERROR: Data sync update failed for: " + parent + " > " + subsector + " > " + ticker + " > " + type + "'}").replace("'", "\"")

def getCIK(ticker):
    DEFAULT_TICKERS = []
    DEFAULT_TICKERS.append(ticker)
    URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
    CIK_RE = re.compile(r'.*CIK=(\d{10}).*')
    cik_dict = {}
    for ticker in DEFAULT_TICKERS:
        print(URL.format(ticker))
        results = CIK_RE.findall(get(URL.format(ticker)).content)
        if len(results):
            cik_dict[str(ticker).lower()] = str(results[0])
    print(cik_dict)
    # f = open('cik_dict', 'w')
    # dump(cik_dict, f)
    # f.close()
    return cik_dict

#####################################################################################################################
################################################# DECISION ENGINE ###################################################
#####################################################################################################################
@app.route('/data/analyze/<parent>/<subsector>/<type>', methods=["GET", "POST"])
def data_analysis_engine(parent, subsector, type):
    return Decide(parent, subsector, type, list(request.json)).final()

@app.route('/data/analyze/sectors/<type>', methods=["GET", "POST"])
def data_analysis_sector_avg(type):
    data = list(request.json)
    vals_all = {}
    for d in data:
        ty = dict(d[str(type)])
        for x in ty:
            vals_all[str(x)] = []
    for d in data:
        ty = dict(d[str(type)])
        for x in ty:
            for y in vals_all:
                if str(x) == str(y):
                    if ty[str(y)] != '-999':
                        try:
                            vals_all[y].append(float(ty[str(y)]))
                        except:
                            pass
    ret_final = []
    for x in vals_all:
        ret_final.append([x, str(round(np.mean(vals_all[x]), 2))])
    return str(ret_final).replace("'", "\"")
