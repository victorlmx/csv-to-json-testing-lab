import csv
import json

def csv_to_json():
    data_dict = {}
    with open('general.csv', encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
        for rows in csv_reader:
            key = rows['Observation Group']
            data_dict[key] = rows
    json_object=json.dumps(data_dict, indent = 4)
    print(json_object)

csv_to_json()
