# !/usr/local/bin/python3.4

## Argument[0] is script to run
## Argument[1] is path to countryDict

import httplib2
import json
import lxml
import os
import sys
import time
from bs4 import BeautifulSoup

filePath_1 = sys.argv[1]

with open(filePath_1, 'rU') as f1:
    countries = json.load(f1)
    for country in countries:
        uri = countries[country]['uri']
        rdfFile = ''.join([uri, 'about.rdf'])
        h = httplib2.Http()
        resp, rdf_doc = h.request(rdfFile, "GET")
        time.sleep(1)
        soup = BeautifulSoup(rdf_doc, "xml")

        for tag in soup.find_all("lat"):
            lat = tag.text
            countries[country]['lat'] = lat

        for tag in soup.find_all("long"):
            long = tag.text
            countries[country]['long'] = long

country_dict_path = os.path.join(os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'countryDict.json')

with open(country_dict_path, 'w') as f2:
    json.dump(countryDict, f2)

print('Finished getting country info')
