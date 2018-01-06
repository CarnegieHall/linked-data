# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2017 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to csv of MusicBrainz IDs and labels
## Argument[2] is path to json file of instrument IDs, labels from data.carnegiehall.org

import csv
import json
import os
import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

filePath_1 = sys.argv[1]
filePath_2 = sys.argv[2]

ch_toMbzDict = {}
mbzDict = {}

with open(filePath_1, 'rU') as f1:
    mbzInstruments = csv.reader(f1, dialect='excel', delimiter=',')
    for row in mbzInstruments:
        mbz_id = row[0]
        mbz_label = row[1]

        mbzDict[str(mbz_id)] = mbz_label

with open(filePath_2, 'rU') as f2:
    chData = json.load(f2)

    for result in chData["results"]["bindings"]:
        chURI = result["instrument"]["value"]
        chLabel = result["label"]["value"]

        for key in mbzDict:
            mbz_label = mbzDict[key]
##            match_pct = fuzz.token_set_ratio(mbz_label, chLabel)
            match_pct = fuzz.partial_ratio(mbz_label, chLabel)
##            match_pct = fuzz.token_sort_ratio(mbz_label, chLabel)
            if match_pct > 75:
##                print(key, '\t', mbz_label, '\t', chLabel)

                ch_toMbzDict[str(chURI)] = {}
                ch_toMbzDict[str(chURI)]["label"] = chLabel
                ch_toMbzDict[str(chURI)]["matches"] = {}
                ch_toMbzDict[str(chURI)]["matches"][str(key)] = mbz_label

print(len(ch_toMbzDict))
##print (json.dumps(ch_toMbzDict, indent=4))

##ch_toMbzDict_path = os.path.join(
##    os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'ch_toMbzDict.json')
##
##with open(ch_toMbzDict_path, 'w') as f1:
##    json.dump(ch_toMbzDict, f1)
##
##print("Finished finding matches to MusicBrainz instrument IDs")
