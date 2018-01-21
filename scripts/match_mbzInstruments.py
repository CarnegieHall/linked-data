# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2017 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to csv of MusicBrainz IDs and labels
## Argument[2] is path to json file of instrument IDs, labels from data.carnegiehall.org

import csv
import json
import os
import pandas as pd
import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

filePath_1 = sys.argv[1]
filePath_2 = sys.argv[2]

ch_toMbzDict = {}

mbzInstruments = pd.read_csv(filePath_1)
chInstruments = pd.read_csv(filePath_2)

def fuzzy_match(x, choices, scorer, cutoff):
    return process.extractOne(
        x, choices=choices, scorer=scorer, score_cutoff=cutoff
        )

FuzzyWuzzyResults = chInstruments.loc[:, "label"].apply(
    fuzzy_match,
    args=( mbzInstruments.loc[:, "label"],
           fuzz.token_sort_ratio,
           90
           )
    )

for result in FuzzyWuzzyResults:
    if result:
        chLabel = result[0]
        matchID = mbzInstruments.iloc[result[2],0]
        matchLabel = mbzInstruments.iloc[result[2],1]
        matches = chInstruments.loc[
            chInstruments['label'] == str(matchLabel)]
        df = matches.set_index('instrument')

        if not df.empty:
            chID = df.index.values[0]

            ch_toMbzDict[str(chID)] = {}
            ch_toMbzDict[str(chID)]['label'] = chLabel
            ch_toMbzDict[str(chID)]['mbz label'] = matchLabel
            ch_toMbzDict[str(chID)]['mbz ID'] = matchID

ch_toMbzDict_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'ch_toMbzDict.json')

with open(ch_toMbzDict_path, 'w') as f1:
    json.dump(ch_toMbzDict, f1)

print("Finished finding matches to MusicBrainz instrument IDs")
