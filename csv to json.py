#Known issues:
#There is no clear way of identifying the different wildlife entries. e.g., "Wildlife 2"
#There is no clear way of identifying the different livestock entries.
#note try &includeuuids=true

import csv
import json

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

def addCategoryInfo(id, category_name, list):
    list.pop("Observation Group")
    observations[id][category_name]=list

def buildCategoryStructure(category_name, list, sub_category_id_column=None):
    sub_categories = {} #subcategories, names and items.
    listCategoryNames = {} #names only, e.g., Species wildlife 1 event 1
    animals_observed_per_species = {} #information about juvenile healthy, sick, dead, etc.
    boolWildlifeOrLivestock = category_name == str_livestock or category_name ==str_wildlife 

    def buildListCategories(id):
        if (id not in listCategoryNames): 
            listCategoryNames[id] = len(listCategoryNames)+1
            sub_categories[id] = {}  

    def addSubCategoryInfo():
        if (category_name == str_animals):
            if (len(item["Sample ID"]) > 0):
                sampleRecord = getSampleRecord()
                if (len(sub_categories[sub_category_id]) == 0):
                    item["Records"]=[sampleRecord]
                    sub_categories[sub_category_id]=item
                else:
                    sub_categories[sub_category_id]["Records"].append(sampleRecord)
            else:
                sub_categories[sub_category_id]=item
            item.pop("Sample Type")
            item.pop("Collected from Environment")
            item.pop("Notes")
            item.pop("Sample ID")

        if (boolWildlifeOrLivestock):
            animals_observed_per_species_item={}
            animal_per_species = item["Animals Observed per Species"] #e.g., "Adult Male", "Adult Female", etc.
            item.pop("Animals Observed per Species")
            animals_observed_per_species_item[animal_per_species + " Healthy"]= item["Number Healthy"]
            animals_observed_per_species_item[animal_per_species + " Sick or Injured"]= item["Number Sick or Injured"]
            animals_observed_per_species_item[animal_per_species + " Dead"]= item["Number Dead"]
            item.pop("Number Dead")
            item.pop("Number Healthy")
            item.pop("Number Sick or Injured")
            if listCategoryNames[sub_category_id] in animals_observed_per_species:
                animals_observed_per_species[listCategoryNames[sub_category_id]]["Animals Observed Per Species"].append(animals_observed_per_species_item)
            else:
                animals_observed_per_species[listCategoryNames[sub_category_id]]={"Animals Observed Per Species":[]}
                animals_observed_per_species[listCategoryNames[sub_category_id]]["Animals Observed Per Species"].append(animals_observed_per_species_item)
            sub_categories[sub_category_id]=item

    def getSampleRecord():
        record = {}
        record = {"Sample ID": item["Sample ID"], "Sample Type" : item["Sample Type"], "Collected from Environment" : item["Collected from Environment"], "Notes" : item["Notes"]}
        return record
    
    def addSubCategoryToObservation(observationGroup, subCategory, sub_category_id):
        if (category_name in observations[observationGroup]):
            observations[observationGroup][category_name][sub_category_id]=subCategory
        else: 
            observations[observationGroup][category_name] = {sub_category_id: subCategory}      

    def addSubCategoryToObservations():
        if (boolWildlifeOrLivestock or category_name == str_animals):    
            n = 0    
            for idx, sub_category in sub_categories.items():
                n += 1
                if (boolWildlifeOrLivestock):
                    sub_category["Animals Observed Per Species"]=animals_observed_per_species[n]["Animals Observed Per Species"]
                groupId = sub_category["Observation Group"]
                sub_category.pop("Observation Group")
                addSubCategoryToObservation(groupId, sub_category, idx)

    for item in list:
        observation_group = observationGroup(item)
        item.pop("Observation Category 0")
        
        if (category_name == str_general or category_name ==str_site):
            addCategoryInfo(observation_group,category_name, item)

        if (boolWildlifeOrLivestock or category_name == str_animals):
            sub_category_id = item[sub_category_id_column]
            buildListCategories(sub_category_id)
            addSubCategoryInfo()
    
    addSubCategoryToObservations()
    
readCSVs()
buildStructure()
print(json.dumps(observations))
