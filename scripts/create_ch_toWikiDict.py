# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2017 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to json query results from data.carnegiehall.org

import json
import os
import sys

filePath_1 = sys.argv[1]

ch_toWikiDict = {}

with open(filePath_1, 'rU') as f1:
    chData = json.load(f1)

    for result in chData["results"]["bindings"]:
        chURI = result["s"]["value"]
        ch_dbp = result["o"]["value"]

        ch_toWikiDict[str(chURI)] = {}
        ch_toWikiDict[str(chURI)]["dbp"] = ch_dbp
        ch_toWikiDict[str(chURI)]["wikidata"] = ""

ch_toWikiDict_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'ch_toWikiDict.json')

with open(ch_toWikiDict_path, 'w') as f1:
    json.dump(ch_toWikiDict, f1)

print("Finished creating ch_toWikiDict")
