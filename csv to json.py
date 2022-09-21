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
dictionary_output={}


def buildDic(name, list):
    global dictionary_output
    for item in list:
        key = item["Observation Group"]
        item.pop("Observation Group")
        item.pop("Observation Category 0")
        if (key not in dictionary_output): 
            dictionary_output[key] = {str_general: [],str_site: [],str_wildlife: [],str_livestock: [],str_animals: []}
        dictionary_output[key][name].append(item)

def buildWildDic(name, list):
    global dictionary_output
    dict2 = {}
    n = 1
    dict3_temp = {}
    for item in list:
        key = item["Observation Group"]
        dict2_key = ""
        item.pop("Observation Group")
        item.pop("Observation Category 0")
        if (key not in dictionary_output): 
            dictionary_output[key] = {str_general: [],str_site: [],str_wildlife: [],str_livestock: [],str_animals: []}
        widlifeID = item["Provide Species not Listed"]
        dict2_key2 = item["Animals Observed per Species"]
        item.pop("Animals Observed per Species")
        if (widlifeID not in dict3_temp): 
            dict3_temp[widlifeID] = n
            dict2_key = "Wildlife " + str(n)
            dict2[dict2_key] = {"Adult Male": [],"Adult Female": [],"Adult Unknown Sex": [],"Juvenile": [],"Fetus": [], "Unknown Sex and Age": []}
            n += 1
        else:
            dict2_key = "Wildlife " + str(dict3_temp[widlifeID])
        dict2[dict2_key][dict2_key2].append(item)
    dictionary_output[key][name].append(dict2)

def deleteEmpty(key, name):
    global dictionary_output
    if (len(dictionary_output[key][name])==0):
        dictionary_output[key].pop(name)

buildDic(str_general, general)
buildDic(str_site, sites)
buildWildDic(str_wildlife, wildlife)
buildDic(str_animals, animal)
buildDic(str_livestock, livestock)

for key in dictionary_output:
    deleteEmpty(key, str_general)
    deleteEmpty(key, str_site)
    deleteEmpty(key, str_wildlife)
    deleteEmpty(key, str_animals)
    deleteEmpty(key, str_livestock)

print(json.dumps(dictionary_output))
