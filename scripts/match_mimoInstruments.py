# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2017 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to csv of Wikidata query results w/MIMO and MBZ IDs
## Argument[2] is path to csv file of CH instrument IDs, labels, MBZ links
## from CH-LOD

import csv
import json
import os
import sys
##from fuzzywuzzy import fuzz
##from fuzzywuzzy import process
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import FOAF, RDF, RDFS, SKOS, XSD
from rdflib.plugins.serializers.nt import NTSerializer

filePath_1 = sys.argv[1]
filePath_2 = sys.argv[2]

wikidataInstr_dict = {}
chInstr_dict = {}
ch_toMIMO_Dict = {}

g = Graph()

##def fuzzy_match(x, choices, scorer, cutoff):
##    return process.extractOne(
##        x, choices=choices, scorer=scorer, score_cutoff=cutoff
##        )

with open(filePath_1, 'rU') as f1:
    wikidataInstr = csv.reader(f1, dialect='excel', delimiter=',', quotechar='"')
    next(wikidataInstr, None)
    for row in wikidataInstr:
        wikidataID = row[0]
        wikidataLabel = row[1]
        mbzID = row[2]
        mimoID = row[3]

        wikidataInstr_dict[str(mbzID)] = {}
        wikidataInstr_dict[str(mbzID)]['label'] = wikidataLabel
        wikidataInstr_dict[str(mbzID)]['wikidataID'] = wikidataID
        wikidataInstr_dict[str(mbzID)]['mimo'] = mimoID

with open(filePath_2, 'rU') as f2:
    chInstruments = csv.reader(f2, dialect='excel', delimiter=',', quotechar='"')
    next(chInstruments, None)
    for row in chInstruments:
        chID = row[0]
        chLabel = row[1]
        mbzID = row[2]

        if mbzID in wikidataInstr_dict.keys():
            wikidataLabel = wikidataInstr_dict[str(mbzID)]['label']
            wikidataID = wikidataInstr_dict[str(mbzID)]['wikidataID']
            mimoID = wikidataInstr_dict[str(mbzID)]['mimo']
            
            ch_toMIMO_Dict[str(chID)] = {}
            ch_toMIMO_Dict[str(chID)]['chLabel'] = chLabel
            ch_toMIMO_Dict[str(chID)]['wikidataLabel'] = wikidataLabel
            ch_toMIMO_Dict[str(chID)]['wikidataID'] = wikidataID
            ch_toMIMO_Dict[str(chID)]['mimoID'] = mimoID

            g.add( (URIRef(chID), SKOS.exactMatch, URIRef(mimoID)) )
            g.add( (URIRef(chID), SKOS.exactMatch, URIRef(wikidataID)) )

ch_toMIMO_Dict_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'ch_toMIMO_Dict.json')

ch_toMIMO_Graph_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'graphs', 'ch_toMIMO_Graph.nt')

g.bind("skos", SKOS)
g = g.serialize(destination=ch_toMIMO_Graph_path, format='nt')

with open(ch_toMIMO_Dict_path, 'w') as f1:
    json.dump(ch_toMIMO_Dict, f1)

print(json.dumps(ch_toMIMO_Dict, indent=4))
print("Finished finding matches to MIMO instrument IDs")
