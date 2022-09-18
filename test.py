import csv
import json

def dictionaryFromCSV(path):
    data_dict = {}
    with open(path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
        for rows in csv_reader:
            key = rows['Observation Group'] #make this the key value.
            #rows.pop('Observation Group')
            #rows.pop('Observation Category 0')
            data_dict[key]=rows
    return data_dict

def setFromCSV(path):
    data_set = []
    with open(path, encoding = 'utf-8') as csv_file_handler:

        csv_reader = csv.DictReader(csv_file_handler)
        for row in csv_reader:
            data_set.append(row)
    return data_set


general=dictionaryFromCSV('general.csv')
sites=dictionaryFromCSV('site.csv')
livestock=setFromCSV('livestock.csv')
output = {}

#note: item is a dict
for item in livestock:
    key = item["Observation Group"]
    if (key not in output):
        output[item["Observation Group"]]=[item["Observation Category 0"],[]]
    item.pop("Observation Category 0")
    item.pop("Observation Group")
    output[key][1].append(item)

print(json.dumps(output))

#print(livestock)

#for item in general.items():


#output = {}
#dict1 = {}
#dict2 = {}

#output["a"]={}
#print(output)
#dict1["General"]={}
#dict2["Site"]={}

#output["a"]=dict1
#print(output)
#output["a"].update(dict2)

#print(output)

exit()
