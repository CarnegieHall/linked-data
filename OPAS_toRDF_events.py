# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2016 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to Venues CSV
## Argument[2] is path to entityDict
## Argument[3] is path to worksDict
## Argument[4] is path to 1st Events CSV
## Argument[5] is path to 2nd Events CSV
## Argument[6] is path to 3rd Events CSV, etc. - can continue adding CSV files as needed

import csv
import json
##from datetime import datetime
import datetime as dt
from pytz import timezone
import pytz
import rdflib
from rdflib import Graph, Literal, Namespace, OWL, RDF, URIRef, XSD
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS
from rdflib.plugins.serializers.nt import NTSerializer
import re
import os
import sys

utc = pytz.timezone("UTC")
eastern = timezone('US/Eastern')

class Event(object):

	def __init__(self, date, time):
		self.date = date
		self.time = time
	def create_event_dateTime(self):
		dateTimeString = ' '.join([date, time])
		isoDateTime = eastern.localize(
                    dt.datetime.strptime(dateTimeString,'%m/%d/%Y %I:%M %p')).isoformat()
		return isoDateTime

venueDict = {}
eventDict = {}

gEvents = Graph()
gVenues = Graph()

chvenues = Namespace('http://data.carnegiehall.org/venues/')
chevents = Namespace('http://data.carnegiehall.org/events/')
geonames = Namespace('http://www.geonames.org/ontology#')
event = Namespace('http://purl.org/NET/c4dm/event.owl#')
mo = Namespace ('http://purl.org/ontology/mo/')
schema = Namespace('http://schema.org/')

ch = chvenues['96397']
geonamesCH = URIRef('http://sws.geonames.org/5111573/')
geonames_chCinema = URIRef('http://sws.geonames.org/7255414/')

gVenues.add( (ch, OWL.sameAs, geonamesCH))
gVenues.add( (ch, RDFS.label, Literal('Carnegie Hall', lang='en') ) )

filePath_1 = sys.argv[1]
filePath_2 = sys.argv[2]
filePath_3 = sys.argv[3]

with open(filePath_1, 'rU') as f1:
    venues = csv.reader(f1, dialect='excel', delimiter=',', quotechar='"')
    for row in venues:
        venue_id = row[0]
        venue_uri = chvenues[str(venue_id)]
        venue_code = row[1]
        venue_name = row[2]
        venue_notes = row[3]

        gVenues.add( (URIRef(venue_uri), RDFS.label, Literal(venue_name, lang='en') ) )
        gVenues.add( (URIRef(venue_uri), geonames.parentFeature, URIRef(ch) ) )

        if venue_notes:
            gVenues.add( (URIRef(venue_uri), RDFS.comment, Literal(venue_notes, lang='en') ) )

        if venue_code == 'ISA':
            oldName = 'Main Hall'
            gVenues.add( (URIRef(venue_uri), geonames.historicalName, Literal(oldName, lang='en') ) )

        if venue_code == 'ZH':
            oldName = 'Carnegie Hall Cinema'
            gVenues.add( (URIRef(venue_uri), geonames.historicalName, Literal(oldName, lang='en') ) )

        if venue_code == 'CHPL':
            oldName = 'Carnegie Lyceum'
            gVenues.add( (URIRef(venue_uri), geonames.historicalName, Literal(oldName, lang='en') ) )

        if venue_code == 'CL':
            oldName = 'Recital Hall'
            gVenues.add( (URIRef(venue_uri), geonames.historicalName, Literal(oldName, lang='en') ) )

        if venue_code == 'WRH':
            oldName = 'Carnegie Recital Hall'
            gVenues.add( (URIRef(venue_uri), geonames.historicalName, Literal(oldName, lang='en') ) )

        if venue_code == 'CRH':
            oldName = 'Chamber Music Hall'
            gVenues.add( (URIRef(venue_uri), geonames.historicalName, Literal(oldName, lang='en') ) )

        if venue_code == 'CIN':
            gVenues.add( (URIRef(venue_uri), OWL.sameAs, geonames_chCinema))
            gVenues.add( (URIRef(venue_uri), geonames.parentFeature, ch ) )
            gVenues.add( (URIRef(venue_uri), geonames.historicalName, Literal('Carnegie Hall Playhouse', lang='en') ) )

        venueDict[str(venue_id)] = venue_uri

with open(filePath_2, 'rU') as f2:
    entities = json.load(f2)
    for item in sys.argv[4:]:
        ## Blank lists of various IDs to check for repeat rows while iterating each CSV
        idList = []
        work_idList = []
        soloist_idList = []
        programList = []
        work_perfDict = {}

        with open(item, 'rU') as csvfile:
            events = csv.reader(csvfile, dialect='excel', delimiter=',', quotechar='"')
            for row in events:
                event_id = row[0]
                date = row[1].lstrip('0')
                time = row[2]
                venue_id = row[3]
                venue_uri = venueDict[str(venue_id)]
                event_uri = chevents[str(event_id)]
                event_title = row[4]

                orchestra_id = row[5]
                orchestra_uri = ''
                if orchestra_id != '0':
                    orchestra_uri = entities[str(orchestra_id)]['uri']

                conductor_id = row[6]
                conductor_uri = ''
                if conductor_id != '0':
                    conductor_uri = entities[str(conductor_id)]['uri']

                work_id = row[7]
                soloist_id = row[8]
                work_order = row[9]

                new_event = Event(date, time)
                isoDateTime = new_event.create_event_dateTime()

                if event_id not in idList:
                    idList.append(event_id)

                    gEvents.add( (URIRef(event_uri), RDF.type, event.Event) )
                    gEvents.add( (URIRef(event_uri), RDFS.label, Literal(event_title, lang='en') ) )
                    gEvents.add( (URIRef(event_uri), DCTERMS.date, Literal(isoDateTime, datatype=XSD.dateTime) ) )
                    gEvents.add( (URIRef(event_uri), event.place, URIRef(venue_uri)) )

                    if conductor_uri:
                        gEvents.add( (URIRef(event_uri), mo.conductor, URIRef(conductor_uri)) )

                    if orchestra_uri:
                        gEvents.add( (URIRef(event_uri), mo.performer, URIRef(orchestra_uri)) )

                    work_idList = []
                    work_idList.append(work_id)

                    soloist_idList = []
                    soloist_idList.append(soloist_id)

                    work_perfDict = {}
                    work_perfDict['soloists'] = soloist_idList
                    work_perfDict['order'] = work_order


                    eventDict[str(event_id)] = {}
                    eventDict[str(event_id)]['isoDateTime'] = isoDateTime
                    eventDict[str(event_id)]['venue id'] = venue_id
                    eventDict[str(event_id)]['title'] = event_title
                    eventDict[str(event_id)]['orchestra id'] = orchestra_id
                    eventDict[str(event_id)]['conductor id'] = conductor_id
                    eventDict[str(event_id)][str(work_id)] = work_perfDict
                    eventDict[str(event_id)]['uri'] = event_uri
                else:
                    if work_id not in work_idList:
                        work_idList.append(work_id)
                        soloist_idList = []
                        soloist_idList.append(soloist_id)
                        
                        work_perfDict = {}
                        work_perfDict['soloists'] = soloist_idList
                        work_perfDict['order'] = work_order
                        
                        eventDict[str(event_id)][str(work_id)] = work_perfDict
                    else:
                        eventDict[str(event_id)][str(work_id)]['soloists'].append(soloist_id)

# Each work on an event is represented by a subdict containing its program order and list of soloists
# These workDicts are in turn represented by a key (key=work_id) in the subdict for that event
# Works are related via the work_performance URI>event.Product>work URI
# Solists are related via work_performance URI>mo.performer>entity URI

# Create list of work IDs for 'No program' and 'Soloists not assigned'
placeHolders = ['3319', '10862']

with open(filePath_3, 'rU') as f3:
    works = json.load(f3)
    for key in eventDict:
        event_uri = eventDict[key]['uri']
        for item in eventDict[key].keys():
            if item.isdigit():
                programOrder = eventDict[key][str(item)]['order']
                work_performance = URIRef(value=''.join([event_uri, '/work_', str(programOrder).zfill(2)]))
                soloists = eventDict[key][str(item)]['soloists']
                work_uri = works[str(item)]['uri']

                if item not in placeHolders:
                    gEvents.add( (URIRef(event_uri), event.product, URIRef(work_performance)) )
                    gEvents.add( (work_performance, RDF.type, event.Product) )
                    gEvents.add( (work_performance, event.product, URIRef(work_uri)) )

                    if '0' not in soloists:
                        for soloist in soloists:
                            soloist_uri = entities[str(soloist)]['uri']
                            gEvents.add( (work_performance, mo.performer, URIRef(soloist_uri)) )
                else:
                    if '0' not in soloists:
                        for soloist in soloists:
                            soloist_uri = entities[str(soloist)]['uri']
                            gEvents.add( (URIRef(event_uri), mo.performer, URIRef(soloist_uri)) )

event_dict_path = os.path.join(os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'eventDict.json')
event_graph_path = os.path.join(os.path.dirname(__file__), os.pardir, 'Graphs', 'eventGraph.nt')
venue_dict_path = os.path.join(os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'venueDict.json')
venue_graph_path = os.path.join(os.path.dirname(__file__), os.pardir, 'Graphs', 'venueGraph.nt')

gVenues.bind("geonames", geonames)
gVenues.bind("owl", OWL)
gVenues.bind("rdfs", RDFS)

gEvents.bind("chevents", chevents)
gEvents.bind("chvenues", chvenues)
gEvents.bind("dcterms", DCTERMS)
gEvents.bind("event", event)
gEvents.bind("mo", mo)
gEvents.bind("rdf", RDF)
gEvents.bind("rdfs", RDFS)

gVenues = gVenues.serialize(destination=venue_graph_path, format='nt')
gEvents = gEvents.serialize(destination=event_graph_path, format='nt')

with open(venue_dict_path, 'w') as f5:
    json.dump(venueDict, f5)

with open(event_dict_path, 'w') as f6:
    json.dump(eventDict, f6)

print("Finished with Venues and Events")
