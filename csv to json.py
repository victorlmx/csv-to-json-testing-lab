#Known issues:
#There is no clear way of identifying the different wildlife entries. e.g., "Wildlife 2"
#There is no clear way of identifying the different livestock entries.

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

#REQ: Read from these queries.
general=setFromCSV('general.csv')
sites=setFromCSV('site.csv')
livestock=setFromCSV('livestock.csv')
wildlife=setFromCSV('wildlife.csv')
animal=setFromCSV('animal.csv')
observation_group_dic={}

def buildDictionary(category_name, list, sub_category_id_column=None, category=None):
    global observation_group_dic
    if (category_name == str_livestock or category_name ==str_wildlife or category_name ==str_animals):
        sub_category = {} #e.g., Wildlife 1, Wildlife 2,...
        a={} #e.g., animals observed per species 
        n = 1
        map_temp = {}  #e.g., cat=1, boar=2
    for item in list:
        #REQ: The 1st level is the Observation Group ID.
        observation_group = item["Observation Group"]
        if (observation_group not in observation_group_dic): 
            observation_group_dic[observation_group] = {}   
        #REQ: Delete already known information.
        item.pop("Observation Group")
        item.pop("Observation Category 0")

        #REQ: General info and Site Description doesn't have any nested items.
        if (category_name == str_general or category_name ==str_site):
            observation_group_dic[observation_group][category_name]=item
        
        #REQ: Livestock and Wildlife have nested items (e.g., "Wildlife 1", "Wildlife 2")
        elif (category_name == str_livestock or category_name ==str_wildlife):
            sub_category_key = ""
            sub_category_id = item[sub_category_id_column]

            #REQ: Group Wildlife and Livestock items by "Animals Observed per Species"
            animal_per_species = item["Animals Observed per Species"] #e.g., "Adult Male", "Adult Female", etc.
            item.pop("Animals Observed per Species")
            if (sub_category_id not in map_temp): 
                map_temp[sub_category_id] = n
                sub_category_key = category + " " + str(n)
                sub_category[sub_category_key] = {}
                n += 1
            else:
                sub_category_key = category + " " + str(map_temp[sub_category_id])

            a[animal_per_species + " Healthy"]= item["Number Healthy"]
            a[animal_per_species + " Sick or Injured"]= item["Number Sick or Injured"]
            a[animal_per_species + " Dead"]= item["Number Dead"]
            item["animals observed per species"]=a
            sub_category[sub_category_key]=item
        elif (category_name == str_animals):
            print("to do")
    if (category_name == str_livestock or category_name ==str_wildlife):
        
        observation_group_dic[observation_group][category_name]=sub_category
        

def deleteEmpty(key, name):
    global observation_group_dic
    if (len(observation_group_dic[key][name])==0):
        observation_group_dic[key].pop(name)

#REQ: Make a category for each query. Place them at the same level.
buildDictionary(str_general, general)
buildDictionary(str_site, sites)
buildDictionary(str_wildlife, wildlife, "Provide Species not Listed", "Wildlife")
buildDictionary(str_animals, animal, "Animal ID", "Animal")
buildDictionary(str_livestock, livestock, "Other Relevant Information", "Livestock")

#REQ: Create JSON schema.
print(json.dumps(observation_group_dic))
