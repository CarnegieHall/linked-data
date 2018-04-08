# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2017 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to csv of MusicBrainz IDs and labels
## Argument[2] is path to csv file of CH instrument IDs, labels from OPAS

import csv
import json
import os
import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.plugins.serializers.nt import NTSerializer

filePath_1 = sys.argv[1]
filePath_2 = sys.argv[2]

mbzInstr_dict = {}
chInstr_dict = {}
ch_toMbzDict = {}

g = Graph()

def fuzzy_match(x, choices, scorer, cutoff):
    return process.extractOne(
        x, choices=choices, scorer=scorer, score_cutoff=cutoff
        )

with open(filePath_1, 'rU') as f1:
    mbzInstruments = csv.reader(f1, dialect='excel', delimiter=',', quotechar='"')
    next(mbzInstruments, None)
    for row in mbzInstruments:
        mbzID = row[0]
        mbzLabel = row[1]
        mbzInstr_dict[str(mbzID)] = mbzLabel

with open(filePath_2, 'rU') as f2:
    chInstruments = csv.reader(f2, dialect='excel', delimiter=',', quotechar='"')
    next(chInstruments, None)
    for row in chInstruments:
        chID = row[0]
        chLabel = row[1]
        chInstr_dict[str(chID)] = chLabel       

for mbzID in mbzInstr_dict:
    mbzLabel = mbzInstr_dict[mbzID]
    for chID in chInstr_dict:
        chLabel = chInstr_dict[chID]
        matchRatio = fuzz.token_sort_ratio(mbzLabel, chLabel)
        if matchRatio > 94:
            
            ch_toMbzDict[str(chID)] = {}
            ch_toMbzDict[str(chID)]['label'] = chLabel
            ch_toMbzDict[str(chID)]['mbz label'] = mbzLabel
            ch_toMbzDict[str(chID)]['mbz ID'] = mbzID
    
for item in ch_toMbzDict:
    chID = item
    mbzID = ch_toMbzDict[str(item)]['mbz ID']

    g.add( (URIRef(chID), SKOS.exactMatch, URIRef(mbzID)) )

ch_toMbzDict_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'ch_toMbzDict.json')

ch_toMbzGraph_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'graphs', 'ch_toMbzGraph.nt')

g.bind("skos", SKOS)
g = g.serialize(destination=ch_toMbzGraph_path, format='nt')

with open(ch_toMbzDict_path, 'w') as f1:
    json.dump(ch_toMbzDict, f1)

print(json.dumps(ch_toMbzDict, indent=4))
print("Finished finding matches to MusicBrainz instrument IDs")
