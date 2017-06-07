# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2017 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to places csv

import csv
import httplib2
import lxml
import os
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
    geoURIs = csv.reader(f1, dialect='excel', delimiter=',', quotechar='"')
    for item in geoURIs:
        geoURI = item[0]
        uri = ''.join([geoURI, 'about.rdf'])
        h = httplib2.Http()
        resp, rdf_doc = h.request(uri, "GET")
        time.sleep(1)
        soup = BeautifulSoup(rdf_doc, "xml")

        for tag in soup.find_all("name"):
            name = tag.text
            gPlaces.add( (URIRef(geoURI), RDFS.label, Literal(name)) )

        for tag in soup.find_all("parentCountry"):
            country = tag.attrs['rdf:resource']
            gPlaces.add( (URIRef(geoURI), gn.parentCountry, URIRef(country) ) )

        for tag in soup.find_all("lat"):
            lat = tag.text
            gPlaces.add( (URIRef(geoURI), wgs84_pos.lat, Literal(lat)) )

        for tag in soup.find_all("long"):
            long = tag.text
            gPlaces.add( (URIRef(geoURI), wgs84_pos.long, Literal(long)) )

places_graph_path = os.path.join(
    os.path.dirname(__file__), os.pardir, 'Graphs', 'placesGraph.nt')

gPlaces.bind("gn", gn)
gPlaces.bind("rdfs", RDFS)
gPlaces.bind("wgs84_pos", wgs84_pos)

gPlaces = gPlaces.serialize(destination=places_graph_path, format='nt')

print('Finished getting geo info')
