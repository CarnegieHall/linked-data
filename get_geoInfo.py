# !/usr/local/bin/python3.4

## Argument[0] is script to run
## Argument[1] is path to entityDict

import httplib2
import json
import lxml
import os
import re
import sys
import time
from bs4 import BeautifulSoup
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDFS
from rdflib.plugins.serializers.nt import NTSerializer

gPlaces = Graph()
gn = Namespace('http://www.geonames.org/ontology#')
wgs84_pos = Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#')

filePath_1 = sys.argv[1]

with open(filePath_1, 'rU') as f1:
    entities = json.load(f1)
    for entity in entities:
        geobirth = entities[entity]['geobirth']
        if geobirth:
            uri = ''.join([geobirth, 'about.rdf'])
            h = httplib2.Http()
            resp, rdf_doc = h.request(uri, "GET")
            time.sleep(1)
            soup = BeautifulSoup(rdf_doc, "xml")

            for tag in soup.find_all("name"):
                name = tag.text
                gPlaces.add( (URIRef(geobirth), RDFS.label, Literal(name)) )

            for tag in soup.find_all("parentCountry"):
                country = tag.attrs['rdf:resource']
                gPlaces.add( (URIRef(geobirth), gn.parentCountry, URIRef(country) ) )

            for tag in soup.find_all("lat"):
                lat = tag.text
                gPlaces.add( (URIRef(geobirth), wgs84_pos.lat, Literal(lat)) )

            for tag in soup.find_all("long"):
                long = tag.text
                gPlaces.add( (URIRef(geobirth), wgs84_pos.long, Literal(long)) )

places_graph_path = os.path.join(os.path.dirname(__file__), os.pardir, 'Graphs', 'placesGraph_test.nt')

gPlaces.bind("gn", gn)
gPlaces.bind("rdfs", RDFS)
gPlaces.bind("wgs84_pos", wgs84_pos)

gPlaces = gPlaces.serialize(destination=places_graph_path, format='nt')

print('Finished getting geo info')
