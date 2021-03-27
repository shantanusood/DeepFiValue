import traceback
import json

def get_by_type(parent, subsector, ticker, type):
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
                return str("ERROR: Data not yet synced for: " + parent + " > " + subsector + " > " + ticker + " > " + type)
        return getData
    except:
        return str("ERROR: Data get failed for: " + parent + " > " + subsector + " > " + ticker + " > " + type)