from flask import Flask, request, redirect, url_for, render_template, Response
import json
import os
from flask_cors import CORS
from data.Indicators import Indicators
from bs4 import BeautifulSoup
import pandas as pd
from data import tickers_list as t
from src import filter as f
import script as s
import traceback
from datetime import datetime
import csv

app = Flask(__name__)
CORS(app)

#####################################################################################################################
############################################## WEB DATA FETCH SERVICE ###############################################
#####################################################################################################################
@app.route('/')
def quide():
    return """
<!DOCTYPE html>
<html lang="en">
<body>
<p>
<h3>Try out below:</h3>
</p>
<ul>
<li><b>Indicators (/indicators/<u>Type</u>):</b>
    <ol>
        <table style="border: 1px solid black">
            <tr><th>Type</th><th>Description</th></tr>
            <tr><td>cci</td> <td>Consumer confidence index</td></tr>
            <tr><td>jobless</td></td><td> US Unemployment rate</td></tr>
            <tr><td>pe</td><td> SP500 price to earnings ratio</td></tr>
            <tr><td>dtrlarindex</td><td> Trade weighted us dollar index broad goods and services</td></tr>
            <tr><td>inflation</td><td> US Inflation rate</td></tr>
            <tr><td>putcall</td><td> Cboe Equity Put/Call Ratio</td></tr>
            <tr><td>manufacturing</td><td> US ISM Manufacturing PMI</td></tr>
        </table>
    </ol>
</li>
</ul>
</body>
</html>
"""

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
    ret_dict_sync = {}
    ret_dict_sync_tm = {}
    if isinstance(ret, pd.DataFrame):
        ret_dict = ret.to_dict()
        if filter == 'quote':
            for x in ret_dict.keys():
                ret_dict_sync[str(x)] = ret_dict[x][0]
            ret_dict_sync_tm[str(datetime.today().strftime('%m/%d/%Y'))] = ret_dict_sync
        else:
            for x in ret_dict['Duration'].keys():
                for y in ret_dict.keys():
                    ret_dict_sync[str(y)] = ret_dict[str(y)][x]
                ret_dict_sync_tm[str(ret_dict['Duration'][x])] = ret_dict_sync
                ret_dict_sync = {}
        return str(ret_dict_sync_tm).replace("'", "\"")
    else:
        return str("ERROR: Unable to sync data for: " + filter + " > " + tickers).replace("'", "\"")

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

#####################################################################################################################
############################################# LOCAL DATA FETCH SERVICE ##############################################
#####################################################################################################################
@app.route('/data/get/<parent>/<subsector>/<ticker>/<type>')
def data_get(parent, subsector, ticker, type):
    filename = './data/sectors/' + str(parent) + "/" + subsector + '.json'
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
                return str("ERROR: Data not yet synced for: " + parent + " > " + subsector + " > " + ticker + " > " + type)
        return str(getData).replace("'", "\"")
    except:
        traceback.print_exc()
        return str("ERROR: Data get failed for: " + parent + " > " + subsector + " > " + ticker + " > " + type)

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
    if os.path.isfile('./data/tickers/Categories.csv'):
        get_parent = pd.read_csv('./data/tickers/Categories.csv')
    is_sub = get_parent['ParentSector'] == str(parent)
    return str(get_parent[is_sub]['Subsector'].to_list()).replace("'", "\"")

#####################################################################################################################
################################################ DATA SYNC SERVICE ##################################################
#####################################################################################################################
@app.route('/data/sync/dump/<parent>/<subsector>/<ticker>/<type>', methods=['GET', 'POST'])
def data_sync_dump(parent, subsector, ticker, type):
    filename = './data/sectors/' + str(parent) + "/" + subsector + '.json'
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
                    elif type == 'fin':
                        row[6] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'bs':
                        row[7] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'cf':
                        row[8] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'inside':
                        row[9] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'inst':
                        row[10] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'bonds':
                        row[11] = str(datetime.today().strftime('%m/%d/%Y'))
                if row:
                    writer.writerow(row)
        return str(data).replace("'", "\"")
    except:
        traceback.print_exc()
        return str("ERROR: Data sync dump failed for: " + parent + " > " + subsector + " > " + ticker + " > " + type)

@app.route('/data/sync/update/<parent>/<subsector>/<ticker>/<type>', methods=['GET', 'POST'])
def data_sync_update(parent, subsector, ticker, type):
    filename = './data/sectors/' + str(parent) + "/" + subsector + '.json'
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
                        data[count][str(ticker)][str(type)][str(i)] = addData[str(i)]
                    break
                count = count + 1
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
                    elif type == 'fin':
                        row[6] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'bs':
                        row[7] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'cf':
                        row[8] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'inside':
                        row[9] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'inst':
                        row[10] = str(datetime.today().strftime('%m/%d/%Y'))
                    elif type == 'bonds':
                        row[11] = str(datetime.today().strftime('%m/%d/%Y'))
                if row:
                    writer.writerow(row)
        return str(data).replace("'", "\"")
    except:
        traceback.print_exc()
        return str("ERROR: Data sync update failed for: " + parent + " > " + subsector + " > " + ticker + " > " + type)

#####################################################################################################################
################################################# HELPER FUNCTIONS ##################################################
#####################################################################################################################

def getMetadata(input):
    metadata = []
    if "_" in input:
        if os.path.isfile('./data/'+input[0:int(input.index("_"))] + '.csv'):
            metadata = t.ticker_details(input)
    return metadata

