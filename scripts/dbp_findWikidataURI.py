# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2017 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to json query results from data.carnegiehall.org
## Argument[2] is path to json query results from dbpedia

import json
import os
import re
import sys

from rdflib import Graph, URIRef
from rdflib.namespace import SKOS
from rdflib.plugins.serializers.nt import NTSerializer

filePath_1 = sys.argv[1]
filePath_2 = sys.argv[2]

ch_toWikiDict = {}
gWikidata = Graph()

with open(filePath_1, 'rU') as f1, open(filePath_2, 'rU') as f2:
    chData = json.load(f1)
    dbpData = json.load(f2)

    for key in chData:
        ch_dbp = chData[str(key)]["dbp"]
        ch_wikidata = chData[str(key)]["wikidata"]
        if not ch_wikidata:
            for item in dbpData["results"]["bindings"]:
                dbp = item["s"]["value"]
                wikidata = item["o"]["value"]

                if dbp == ch_dbp:
                    chData[key]["wikidata"] = wikidata
                    gWikidata.add( (URIRef(key), SKOS.exactMatch, URIRef(wikidata)) )

ch_toWikiDict_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'ch_toWikiDict.json')
wikidata_graph_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'Graphs', 'wikidataGraph_dboMusicalArtist.nt')

with open(ch_toWikiDict_path, 'w') as f1:
    json.dump(ch_toWikiDict, f1)

gWikidata.bind("skos", SKOS)

gWikidata = gWikidata.serialize(destination=wikidata_graph_path, format='nt')

print("Finished getting Wikidata URIs")
