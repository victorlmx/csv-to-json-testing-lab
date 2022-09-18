import csv
import json

def dictionaryFromCSV(path):
    data_dict = {}
    with open(path, encoding = 'utf-8') as csv_file_handler:

        csv_reader = csv.DictReader(csv_file_handler)
        for rows in csv_reader:
            dic_2={}
            key = rows['Observation Group'] #make this the key value.
            for item in rows.items():
                #print(item[0])
                if (item[0] != "Observation Group" and item[0] != "Observation Category 0"):
                    dic_2[item[0]]=item[1]
            data_dict[key]=dic_2
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

for observationGroup in sites:
    if (observationGroup in general):
        general[observationGroup]["Site Description"]= sites[observationGroup]
    else:
        print("XXXXXXX")

print(general)
exit()

livestock=setFromCSV('livestock.csv')
