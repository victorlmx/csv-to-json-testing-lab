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

def buildDictionary(name, list, idIdentifier=None, category=None):
    global dictionary_output
    if (name == str_livestock or name ==str_wildlife):
        sub_category = {}
        n = 1
        map_temp = {}
    for item in list:
        key = item["Observation Group"]
        item.pop("Observation Group")
        item.pop("Observation Category 0")

        if (name == str_livestock or name ==str_wildlife):
            sub_category_name = ""
            sub_category_id = item[idIdentifier]
            dict2_key2 = item["Animals Observed per Species"]
            item.pop("Animals Observed per Species")
            if (sub_category_id not in map_temp): 
                map_temp[sub_category_id] = n
                sub_category_name = category + " " + str(n)
                sub_category[sub_category_name] = {"Adult Male": [],"Adult Female": [],"Adult Unknown Sex": [],"Juvenile": [],"Fetus": [], "Unknown Sex and Age": []}
                n += 1
            else:
                sub_category_name = category + " " + str(map_temp[sub_category_id])

        if (key not in dictionary_output): 
            dictionary_output[key] = {str_general: [],str_site: [],str_wildlife: [],str_livestock: [],str_animals: []}
        dictionary_output[key][name].append(item)

def deleteEmpty(key, name):
    global dictionary_output
    if (len(dictionary_output[key][name])==0):
        dictionary_output[key].pop(name)

buildDictionary(str_general, general)
buildDictionary(str_site, sites)
buildDictionary(str_wildlife, wildlife, "Provide Species not Listed", "Wildlife")
buildDictionary(str_animals, animal)
buildDictionary(str_livestock, livestock, "Other Relevant Information", "Livestock")

for key in dictionary_output:
    deleteEmpty(key, str_general)
    deleteEmpty(key, str_site)
    deleteEmpty(key, str_wildlife)
    deleteEmpty(key, str_animals)
    deleteEmpty(key, str_livestock)

print(json.dumps(dictionary_output))
