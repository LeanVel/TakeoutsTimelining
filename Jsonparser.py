import json

data = json.load(open("output/output.json",'r'))

for tuple in data :
    for field in tuple:
        print (field)