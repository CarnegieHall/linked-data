# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2017 Carnegie Hall | The MIT License (MIT)----
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

chnames = Namespace('http://data.carnegiehall.org/names/')
chvenues = Namespace('http://data.carnegiehall.org/venues/')
chinstruments = Namespace('http://data.carnegiehall.org/instruments/')
chworks = Namespace('http://data.carnegiehall.org/works/')
event = Namespace('http://purl.org/NET/c4dm/event.owl#')
gndo = Namespace('http://d-nb.info/standards/elementset/gnd#')
mo = Namespace ('http://purl.org/ontology/mo/')
schema = Namespace('http://schema.org/')
dbp = Namespace('http://dbpedia.org/ontology/')
dbpedia = Namespace('http://dbpedia.org/resource/')
gn = Namespace('http://www.geonames.org/ontology#')
mbz = Namespace('http://musicbrainz.org/artist/')
lcnaf = Namespace('http://id.loc.gov/authorities/names/')
lcMarcRel = Namespace('http://id.loc.gov/vocabulary/relators/')
wgs84_pos = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')

filePath_1 = sys.argv[1]
fileName = fetch_name(filePath_1)

turtle = 'turtle'
ttl = 'ttl'
newSerialization = input('Enter new serialization: ')
newExtension = input('Enter new file extension: ')
print('The new serialization will be', newSerialization, 'with extension', newExtension)

g = Graph()

g.parse(filePath_1, format=str(newSerialization))

graph_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'Graphs', (fileName + '.' + newExtension))

g.bind("chinstruments", chinstruments)
g.bind("chnames", chnames)
g.bind("chworks", chworks)
g.bind("dbpedia-owl", dbp)
g.bind("dbpedia", dbpedia)
g.bind("dcterms", DCTERMS)
g.bind("event", event)
g.bind("foaf", FOAF)
g.bind("gn", gn)
g.bind("gndo", gndo)
g.bind("lcnaf", lcnaf)
g.bind("lcMarRel", lcMarcRel)
g.bind("mbz", mbz)
g.bind("mo", mo)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("skos", SKOS)
g.bind("schema", schema)
g.bind("wgs84_pos", wgs84_pos)

g.serialize(destination=graph_path,format=str(newSerialization))

print('Finished converting', fileName, 'to', newSerialization)
