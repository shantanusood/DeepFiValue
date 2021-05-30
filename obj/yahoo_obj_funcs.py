from obj import yahoo_obj as y
import datetime as dt
import pandas as pd

def getTableData(soup, type):
    dict = {}
    n = 0
    header_val = [i.text.upper() for i in soup.select(y.table_breakdown_header())[1:]]
    l = soup.select(y.table_data())
    labels = soup.select(y.table_labels())
    data = [i.text for i in l]
    n = int(len(data)/len(labels))
    counter = 0
    try:
        dict["Duration"] = header_val
        for i in range(0, len(data), n):
            dict[str(labels[counter].text)] = data[i:i+n]
            counter = counter + 1
    except:
        pass
        #n = 4
        #for i in range(0, len(data), n):
            #dict[str(labels[counter].text)] = data[i:i+n-1]
            #counter = counter + 1
    return dict

def getTableData_ks(soup, type):
    dict = {}
    n = 0
    header_val = [i.text.upper() for i in soup.select(y.ks_table_labels())[1:]]
    header_val.insert(0, "Current")
    l = soup.select(y.ks_table_data())
    labels = soup.select(y.ks_table_breakdown_header())
    data = [i.text for i in l]
    n = int(len(data)/len(labels))
    counter = 0
    try:
        dict["Duration"] = header_val
        for i in range(0, len(data), n):
            dict[str(labels[counter].text)] = data[i:i+n]
            counter = counter + 1
    except:
        pass
        #n = 4
        #for i in range(0, len(data), n):
            #dict[str(labels[counter].text)] = data[i:i+n-1]
            #counter = counter + 1
    return dict

def getTableData_inside(soup, type):
    data = soup.select(y.inside_table())
    data = data[1:]
    header_val = [i.text.upper() for i in data[0]]
    data = data[1:]
    count = 0
    for x in data:
        data[count] = [i.text.upper() for i in x][2:]
        count = count + 1
    return pd.DataFrame(data, columns=header_val[2:])
