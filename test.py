import csv
import json

def setFromCSV(path):
    data_set = []
    with open(path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
        for row in csv_reader:
            data_set.append(row)
    return data_set

general=setFromCSV('general.csv')
sites=setFromCSV('site.csv')
livestock=setFromCSV('livestock.csv')
wildlife=setFromCSV('wildlife.csv')
animal=setFromCSV('animal.csv')
output={}

for item in livestock:
    key = item["Observation Group"]
    if (key not in output): #what if the key exists, but not this category?
        output[key] = {'General': [],'Site': [],'Wildlife': [],'Livestock': [],'Animals': []}
    output[key]["Livestock"].append(item)

for item in animal:
    key = item["Observation Group"]
    if (key not in output): #what if the key exists, but not this category?
        output[key] = {'General': [],'Site': [],'Wildlife': [],'Livestock': [],'Animals': []}
    output[key]["Animals"].append(item)

for item in general:
    key = item["Observation Group"]
    if (key not in output): #what if the key exists, but not this category?
        output[key] = {'General': [],'Site': [],'Wildlife': [],'Livestock': [],'Animals': []}
    output[key]["General"].append(item)

for item in sites:
    key = item["Observation Group"]
    if (key not in output): #what if the key exists, but not this category?
        output[key] = {'General': [],'Site': [],'Wildlife': [],'Livestock': [],'Animals': []}
    output[key]["Site"].append(item)

for item in wildlife:
    key = item["Observation Group"]
    if (key not in output): #what if the key exists, but not this category?
        output[key] = {'General': [],'Site': [],'Wildlife': [],'Livestock': [],'Animals': []}
    output[key]["Wildlife"].append(item)



print(json.dumps(output))



exit()
