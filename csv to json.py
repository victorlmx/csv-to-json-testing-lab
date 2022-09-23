#Known issues:
#There is no clear way of identifying the different wildlife entries. e.g., "Wildlife 2"
#There is no clear way of identifying the different livestock entries.

#note try &includeuuids=true






#TO-DO: Generate Animal Sample Records






import csv
import json
from collections import defaultdict


str_animals= "Animal and Samples"
str_livestock = "Livestock - Domestic Species"
str_wildlife = "Wildlife"
str_site = "Site Description"
str_general = "General Information"

general=[]
sites=[]
livestock=[]
wildlife=[]
animal=[]

observations={}
animals_observed_per_species={}

def readCSVs():
    global general, sites, livestock, wildlife, animal
    general=createListFromCSV('general.csv')
    sites=createListFromCSV('site.csv')
    livestock=createListFromCSV('livestock.csv')
    wildlife=createListFromCSV('wildlife.csv')
    animal=createListFromCSV('animal.csv')

def buildStructure():
    buildCategoryStructure(str_general, general)
    buildCategoryStructure(str_site, sites)
    buildCategoryStructure(str_wildlife, wildlife, "Provide Species not Listed")
    buildCategoryStructure(str_animals, animal, "Animal ID")
    buildCategoryStructure(str_livestock, livestock, "Species")

def createListFromCSV(path):
    data_set = []
    with open(path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
        for row in csv_reader:
            data_set.append(row)
    return data_set

def observationGroup(list):
    id = list["Observation Group"]
    if (id not in observations): 
        observations[id] = {}
    return id

def removeKnownInfo(list):
    list.pop("Observation Group")
    list.pop("Observation Category 0")

def addCategoryInfo(id, category_name, list):
    print("-- processing observation", id, ", waypoint", list["Waypoint ID"])
    observations[id][category_name]=list

def buildCategoryStructure(category_name, list, sub_category_id_column=None):
    print("Building json for ", category_name, ":")
    sub_category = {} #e.g., Wildlife 1, Wildlife 2,...
    sub_category_items = {}
    listCategories = {}  #e.g., cat=1, boar=2

    for item in list:
        observation_group = observationGroup(item)
        if (category_name == str_general or category_name ==str_site):
            addCategoryInfo(observation_group,category_name, item)
        
        if (category_name == str_livestock or category_name ==str_wildlife or category_name == str_animals):
            print("-- processing observation", observation_group, ", ID:", item[sub_category_id_column])
            
            sub_category_id = item[sub_category_id_column]

            if (sub_category_id not in listCategories): 
                listCategories[sub_category_id] = len(listCategories)+1
                sub_category[sub_category_id] = {}

        if (category_name == str_animals):
            sub_category[sub_category_id]=item
            observations[observation_group][category_name]=sub_category

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
            if listCategories[sub_category_id] in sub_category_items:
                sub_category_items[listCategories[sub_category_id]]["Animals Observed Per Species"].append(animals_observed_per_species)
            else:
                sub_category_items[listCategories[sub_category_id]]={"Animals Observed Per Species":[]}
                sub_category_items[listCategories[sub_category_id]]["Animals Observed Per Species"].append(animals_observed_per_species)
            
            sub_category[sub_category_id]=item

    #add the multiple animals_observed_per_species to the subcategory.
    if (category_name == str_livestock or category_name ==str_wildlife):
        for idx, value in enumerate(sub_category.values()):
            value["Animals Observed Per Species"]=sub_category_items[idx+1]["Animals Observed Per Species"]
        observations[observation_group][category_name]=sub_category

readCSVs()
buildStructure()
print("==================Complete JSON Below==================")
print(json.dumps(observations))
