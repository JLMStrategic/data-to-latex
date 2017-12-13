import json
from pprint import pprint

JSON_DIR = './json'

with open(JSON_DIR + '/' + 'Angie_Yuan.json') as json_file:
    data = json.load(json_file)

# pprint(data)
print(data)