import csv
import json

def dictionaryFromCSV(path):
    data_dict = {}
    with open(path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
        for rows in csv_reader:
            key = rows['Observation Group'] #make this the key value.
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
animal=setFromCSV('animal.csv')
output={}

for item in livestock:
    key = item["Observation Group"]
    if (key not in output): #what if the key exists, but not this category?
        output[key] = {'General': [],'Site': [],'Wildlife': [],'Livestock': [],'Animals': []}
    output[key]["Livestock"].append(item)




exit()
