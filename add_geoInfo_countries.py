# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2016 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to countryDict
## Argument[2] is path to placesGraph

import json
import os
import rdflib
from rdflib import Graph
from rdflib import Graph, Literal, Namespace, OWL, RDF, URIRef, XSD
from rdflib.namespace import DCTERMS, FOAF, OWL, RDF, RDFS, SKOS
from rdflib.plugins.serializers.nt import NTSerializer
from rdflib.plugins.serializers.turtle import TurtleSerializer
import sys

def fetch_name(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

geonames = Namespace('http://sws.geonames.org/')
wgs84_pos = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')

filePath_1 = sys.argv[1]
filePath_2 = sys.argv[2]
fileName = fetch_name(filePath_2)

g = Graph()

g.parse(filePath_2, format='nt')

with open(filePath_1, 'rU') as f1:
    countries = json.load(f1)
    for country in countries:
        uri = countries[country]['uri']
        name = countries[country]['label']

        g.add( (URIRef(uri), RDFS.label, Literal(name)) )

graph_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'Graphs', (fileName + '.nt'))

g.bind("geonames", geonames)
g.bind("wgs84_pos", wgs84_pos)
g.bind("rdfs", RDFS)

g.serialize(destination=graph_path,format='nt')

print('Finished adding country info to placesGraph')
