import csv
import numpy as np
import json
csv_file_path = "./outputs/output_seq9_unscl.csv"

output_file_path = "./outputs/location_seq9_unscl.json"
dicts = {'data':[]}
datas = {}
object_data = {}
with open(file=csv_file_path,mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader,None)
    for row in csv_reader:
        frame = int(row[0])
        pos = json.loads(row[1])
        tag = row[2]
        object_data = datas[frame]
        if tag in object_data:
            object_data[tag].append([pos])
        else:
            object_data[tag] = [[pos]]

        datas[frame] = object_data

dicts['data'] = [datas]

with open(output_file_path, 'w') as json_file:
    json.dump(dicts, json_file, indent=4)
