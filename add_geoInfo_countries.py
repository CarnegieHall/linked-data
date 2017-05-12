# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2016 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to graph

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
fileName = fetch_name(filePath_1)

g = Graph()

g.parse(filePath_1, format='nt')

for place in countryDict:
    uri = place
    name = countryDict[place]['label']
    lat = countryDict[place]['lat']
    long = countryDict[place]['long']

    gPlaces.add( (URIRef(uri), RDFS.label, Literal(name)) )
    gPlaces.add( (URIRef(uri), wgs84_pos.lat, Literal(lat)) )
    gPlaces.add( (URIRef(uri), wgs84_pos.long, Literal(long)) )

graph_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'Graphs', (fileName + '.nt'))

g.bind("geonames", geonames)
gPlaces.bind("wgs84_pos", wgs84_pos)
g.bind("rdfs", RDFS)

g.serialize(destination=graph_path,format='nt')

print('Finished adding country labels to graph')
