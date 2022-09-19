import csv
import json

def setFromCSV(path):
    data_set = []
    with open(path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
        for row in csv_reader:
            data_set.append(row)
    return data_set


str_animals= "Animal and Samples"
str_livestock = "Livestock - Domestic Species"
str_wildlife = "Wildlife"
str_site = "Site Description"
str_general = "General Information"

general=setFromCSV('general.csv')
sites=setFromCSV('site.csv')
livestock=setFromCSV('livestock.csv')
wildlife=setFromCSV('wildlife.csv')
animal=setFromCSV('animal.csv')
output={}


def buildDic(name, list):
    global output
    for item in list:
        key = item["Observation Group"]
        item.pop("Observation Group")
        item.pop("Observation Category 0")
        if (key not in output): 
            output[key] = {str_general: [],str_site: [],str_wildlife: [],str_livestock: [],str_animals: []}
        output[key][name].append(item)

def deleteEmpty(key, name):
    if (len(output[key][name])==0):
        output[key].pop(name)

buildDic(str_general, general)
buildDic(str_site, sites)
buildDic(str_wildlife, wildlife)
buildDic(str_animals, animal)
buildDic(str_livestock, livestock)

for key in output:
    deleteEmpty(key, str_general)
    deleteEmpty(key, str_site)
    deleteEmpty(key, str_wildlife)
    deleteEmpty(key, str_animals)
    deleteEmpty(key, str_livestock)

print(json.dumps(output))
