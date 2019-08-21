# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2017 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Output is TSV file for Wikidata Quickstatements tool
## NB chID values need to be enclosed inside double quotes for tool to work
## Argument[0] is script to run
## Argument[1] is path to json query results from data.carnegiehall.org (IDs w/WD link)
## Argument[2] is path to csv query results from wikidata (items w/CH Agent ID)
## Argument[3] is the Wikidata property to update (Agent=P4104 | Work=P5229)
## Argument[4] is destination directory for output TSV of WD IDs and CH IDs

import csv
import json
import os
import sys
from urllib.parse import urlparse

filePath_1 = sys.argv[1]
filePath_2 = sys.argv[2]
wdProperty = sys.argv[3]
filePath_3 = sys.argv[4]

ch_WikiDict = {}
wikiDict = {}
wiki_updateDict = {}
c = 0

with open(filePath_1, newline=None) as f1:
    chData = json.load(f1)

    for result in chData["results"]["bindings"]:
        wdURI = result["wikidataLink"]["value"]
        wdID = urlparse(wdURI)[2].split('/')[2]
        chURI = result["name"]["value"]
        chID = urlparse(chURI)[2].split('/')[2]

        ch_WikiDict[str(wdID)] = chID

with open(filePath_2, newline=None, encoding='utf-8') as f2:
	wikiData = csv.reader(f2, dialect='excel', delimiter=',', quotechar='"')
	next(wikiData, None)
	for row in wikiData:
            wdURI = row[0]
            wdID = urlparse(wdURI)[2].split('/')[2]
            chURI = row[1]
            chID = urlparse(chURI)[2].split('/')[2]

            wikiDict[str(wdID)] = chID

for key in ch_WikiDict:
    chID = ch_WikiDict[str(key)]
    if key not in wikiDict:
        c += 1
        wiki_updateDict[str(key)] = chID

outputPath = ''.join([str(filePath_3), '/wikidataUpdate.tsv'])

with open(outputPath, 'w', newline='') as tsvfile:
    w = csv.writer(tsvfile, delimiter="\t", quotechar="'")
    for key, val in wiki_updateDict.items():
        w.writerow([key, wdProperty, f'"{val}"'])

print(f'There are {c} Wikidata IDs without CH Agent IDs')
print('Finished creating wikidataUpdate')
