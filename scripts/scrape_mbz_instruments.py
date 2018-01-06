# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2017 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

##needs further refinement to eliminate non-instrument link results

## Argument[0] is script to run

import csv
import httplib2
import json
import os
import sys
from bs4 import BeautifulSoup

mbz_instDict = {}

h = httplib2.Http()
link = 'https://musicbrainz.org/instruments'
uri_root = 'https://musicbrainz.org'
resp, html_doc = h.request(link, "GET")
soup = BeautifulSoup(html_doc, "lxml")

for result in soup.body.select(
    'a[href^"/instrument/"]'):
    label = result.contents[0].string
    uri = ''.join([uri_root, result.get('href')])

    mbz_instDict[str(uri)] = label

mbz_instDict_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'source-files', 'mbz_instDict.json')

mbz_instList_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'source-files', 'mbz_instList.csv')

with open(mbz_instDict_path, 'w') as f1:
    json.dump(mbz_instDict, f1)

with open(mbz_instList_path, 'w', newline='') as csvfile:
    w = csv.writer(csvfile, dialect='excel', delimiter=',')
    for k,v in mbz_instDict.items():
        w.writerow([k,v])

print("Finished gathering MusicBrainz instrument URIs and labels")

