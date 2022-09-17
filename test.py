

import csv
import json

with open('general.csv', newline='', mode="r") as csvFile:
    csv_reader = csv.reader(csvFile, delimiter=',', quotechar='"', lineterminator="\n")
    header = next(csv_reader)
    #"Waypoint ID","Waypoint Date","Waypoint Time","X","Y","Comment","Last Modified","Last Modified By","Observation Category 0","Affiliation","Name Protected Area","Patrol Leader or Focal Point","Observation Group"
    #print(header)
    general = {}
    for row in csv_reader:
        observationGroup  = row[12]
        #print(observationGroup)
        if(observationGroup not in general.keys()):
            general[observationGroup] = []
        general[observationGroup].append([row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]])
        #print(general)
        json_dump=json.dumps(general[observationGroup])
        print(json_dump)
