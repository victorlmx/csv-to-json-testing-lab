#Known issues:
#There is no clear way of identifying the different wildlife entries. e.g., "Wildlife 2"
#There is no clear way of identifying the different livestock entries.

#note try &includeuuids=true

import csv
import json
from collections import defaultdict

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

def buildJSON(category_name, list, sub_category_id_column=None):
    print("Building json for ", category_name, ":")
    global observation_group_dic
    if (category_name == str_livestock or category_name ==str_wildlife or category_name ==str_animals):
        sub_category = {} #e.g., Wildlife 1, Wildlife 2,...
        sub_category_items = {}
        n = 1
        map_categories = {}  #e.g., cat=1, boar=2
    for item in list:
        #REQ: The 1st level is the Observation Group ID.
        observation_group = item["Observation Group"]
        if (observation_group not in observation_group_dic): 
            observation_group_dic[observation_group] = {}   
        item.pop("Observation Group")
        item.pop("Observation Category 0")

        #REQ: General info and Site Description items doesn't need any particular nesting.
        if (category_name == str_general or category_name ==str_site):
            print("-- processing observation", observation_group, ", waypoint", item["Waypoint ID"])
            observation_group_dic[observation_group][category_name]=item
        
        #REQ: Livestock and Wildlife have nested items (e.g., "Wildlife 1", "Wildlife 2")
        if (category_name == str_livestock or category_name ==str_wildlife or category_name == str_animals):
            print("-- processing observation", observation_group, ", ID:", item[sub_category_id_column])
            animals_observed_per_species={}
            sub_category_key = ""
            sub_category_id = item[sub_category_id_column]

            if (sub_category_id not in map_categories): 
                map_categories[sub_category_id] = n
                sub_category_key = item[sub_category_id_column]
                sub_category[sub_category_key] = {}
                n += 1
            else:
                sub_category_key = item[sub_category_id_column]

        if (category_name == str_animals):
            sub_category[sub_category_key]=item
            observation_group_dic[observation_group][category_name]=sub_category

        if (category_name == str_livestock or category_name ==str_wildlife):
            #REQ: Group Wildlife and Livestock items by "Animals Observed per Species"
            #Generate something like 
            #{
            #    "Adult Female Healthy":"5.0",
            #    "Adult Female Sick or Injured":"0.0",
            #    "Adult Female Dead":"1.0"
            #},
            animal_per_species = item["Animals Observed per Species"] #e.g., "Adult Male", "Adult Female", etc.
            item.pop("Animals Observed per Species")
            animals_observed_per_species[animal_per_species + " Healthy"]= item["Number Healthy"]
            animals_observed_per_species[animal_per_species + " Sick or Injured"]= item["Number Sick or Injured"]
            animals_observed_per_species[animal_per_species + " Dead"]= item["Number Dead"]
            item.pop("Number Dead")
            item.pop("Number Healthy")
            item.pop("Number Sick or Injured")

            #append animals_observed_per_species to the list that will ultimately be assigned to the subcategory (e.g., "Widlife 1" or "Wildlife 2") outside of the for loop.
            if map_categories[sub_category_id] in sub_category_items:
                sub_category_items[map_categories[sub_category_id]]["animals observed per species"].append(animals_observed_per_species)
            else:
                sub_category_items[map_categories[sub_category_id]]={"animals observed per species":[]}
                sub_category_items[map_categories[sub_category_id]]["animals observed per species"].append(animals_observed_per_species)
            
            sub_category[sub_category_key]=item

        #elif (category_name == str_animals):

    #add the multiple animals_observed_per_species to the subcategory.
    if (category_name == str_livestock or category_name ==str_wildlife):
        n=1
        for value in sub_category.values():
            value["animals observed per species"]=sub_category_items[n]["animals observed per species"]
            n += 1
        observation_group_dic[observation_group][category_name]=sub_category

#REQ: Make a category for each query. Place them at the same level.
buildJSON(str_general, general)
buildJSON(str_site, sites)
buildJSON(str_wildlife, wildlife, "Provide Species not Listed")
buildJSON(str_animals, animal, "Animal ID")
buildJSON(str_livestock, livestock, "Species")

#REQ: Create JSON schema.
print("==================Complete JSON Below==================")
print(json.dumps(observation_group_dic))
