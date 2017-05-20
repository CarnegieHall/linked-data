# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2016 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to Countries CSV
## Argument[2] is path to Instruments CSV
## Argument[3] is path to Composers CSV
## Argument[4] is path to Performers CSV -- if more CSVs needed, add as additional args

import csv
import io
import json
import rdflib
from rdflib import Graph, Literal, Namespace, OWL, RDF, URIRef, XSD
from rdflib.namespace import FOAF, OWL, RDF, RDFS, SKOS
from rdflib.plugins.serializers.nt import NTSerializer
import re
import os
import sys

class Entity(object):

	def __init__(self, names, dates):
		self.names = names
		self.dates = dates
	def create_entity_name(self):
		fullName = ' '.join(self.names).strip()
		return fullName
	def create_entity_dates(self):
		lifeDates = []
		for date in self.dates:
			if (date[0].isnumeric() and
			    date[1].isnumeric() and
			    date[2].isnumeric()):
				lifeDate = "{:04d}-{:02d}-{:02d}".format(
					    int(date[0]),int(date[1]),int(date[2]))
			elif (date[0].isnumeric() and
			      date[1].isnumeric()):
				lifeDate = "{:04d}-{:02d}".format(
					int(date[0]),int(date[1]))
			elif date[0].isnumeric():
				lifeDate = "{:04d}".format(int(date[0]))
			else:
				lifeDate = "unknown"
			lifeDates.append(lifeDate)
		return lifeDates

countryDict = {}
instrumentDict = {}
entityDict = {}

gInstruments = Graph()
gEntities = Graph()

chensembles = Namespace('http://data.carnegiehall.org/ensembles/')
chinstruments = Namespace('http://data.carnegiehall.org/instruments/')
chnames = Namespace('http://data.carnegiehall.org/names/')
chroles = Namespace('http://data.carnegiehall.org/roles/')
dbp = Namespace('http://dbpedia.org/ontology/')
gndo = Namespace('http://d-nb.info/standards/elementset/gnd#')
mbz = Namespace('https://musicbrainz.org/artist/')
mo = Namespace ('http://purl.org/ontology/mo/')
schema = Namespace('http://schema.org/')

filePath_1 = sys.argv[1]
filePath_2 = sys.argv[2]
filePath_3 = sys.argv[3]

with open(filePath_1, 'rU') as f1:
    countries = csv.reader(f1, dialect='excel', delimiter=',', quotechar='"')
    for row in countries:
        country_id = row[0]
        label = row[1]
        uri = row[2]

        countryDict[str(country_id)] = {}
        countryDict[str(country_id)]['label'] = label
        countryDict[str(country_id)]['lat'] = ''
        countryDict[str(country_id)]['long'] = ''
        countryDict[str(country_id)]['uri'] = uri

with open(filePath_2, 'rU') as f2:
    instruments = csv.reader(f2, dialect='excel', delimiter=',', quotechar='"')
    p = re.compile(r'^http://')
    for row in instruments:
        instrument_id = row[0]
        name = row[1]
        type_indicator = row[2]
        sameAs_uri = row[3]
        predicate = row[4]
        section_id = row[5]

        if type_indicator in ('ANIMAL', 'ROLE_IND'):
                instrument_uri = chroles[str(instrument_id)]
        elif type_indicator in ('ENS', 'ROLE_GRP'):
                instrument_uri = chensembles[str(instrument_id)]
                gInstruments.add( (URIRef(instrument_uri), RDF.type, schema.PerformingGroup) )
        else:
                instrument_uri = chinstruments[str(instrument_id)]
                gInstruments.add( (URIRef(instrument_uri), RDF.type, mo.Instrument) )

        gInstruments.add( (URIRef(instrument_uri), RDFS.label, Literal(name) ) )

        match = p.findall(sameAs_uri)
        if type_indicator == 'IND':
            gInstruments.add( (URIRef(instrument_uri), RDF.type, mo.Instrument) )

        instrumentDict[str(instrument_id)] = {}
        instrumentDict[str(instrument_id)]['label'] = name
        instrumentDict[str(instrument_id)]['typeIndicator'] = type_indicator
        instrumentDict[str(instrument_id)]['uri'] = instrument_uri
        instrumentDict[str(instrument_id)]['sameAs'] = sameAs_uri
        instrumentDict[str(instrument_id)]['predicate'] = predicate
        instrumentDict[str(instrument_id)]['section_id'] = section_id


## Blank list to contain instruments for each entity
instrumentList = []

## Instrument is used to set rdf:type (foaf:Person or foaf:Agent)
## For non-performing composers, gender will set rdf:type
## (Group/collective composers don't have gender, therefore foaf:Agent)

for item in sys.argv[4:]:
    ## Blank list of IDs to check for repeat rows while iterating each CSV
    idList = []
    with open(item, 'rU') as csvfile:
        addressBook = csv.reader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in addressBook:
            address_id = row[0]
            performer_uri = chnames[str(address_id)]
            if address_id not in idList:
                idList.append(address_id)
                foafClass = ''
                lastName = row[1]
                firstName = row[2]
                title = row[3]
                suffix = row[4]
                birthDay = row[5]
                birthMonth = row[6]
                birthYear = row[7]
                birthCountry_id = row[8]
                deathDay = row[9]
                deathMonth = row[10]
                deathYear = row[11]

                performer = Entity([title, firstName, lastName, suffix], (
                    [birthYear, birthMonth, birthDay], [deathYear, deathMonth, deathDay]))

                fullName = performer.create_entity_name()
                birthDate = performer.create_entity_dates()[0]
                deathDate = performer.create_entity_dates()[1]

                ## Names, instruments, and rdf types/classes will be added to the graph here
                instrument_idList = []
                instrument_id = row[12]
                if instrument_id != '0':
                    instrument_name = instrumentDict[str(instrument_id)]['label']
                    instrument_predicate = instrumentDict[str(instrument_id)]['predicate']
                    instrument_uri = instrumentDict[str(instrument_id)]['uri']
                    instrument_type = instrumentDict[str(instrument_id)]['typeIndicator']
                    instrument_section = instrumentDict[str(instrument_id)]['section_id']
                    instrument_idList.append(instrument_id)

                    if instrument_section != '26':
                        if instrument_type in ('IND', 'ROLE_IND'):
                            gEntities.add(
                                (URIRef(performer_uri), RDF.type, FOAF.Person) )
                            gEntities.add(
                                (URIRef(performer_uri), FOAF.name, Literal(fullName)) )
                            gEntities.add(
                                (URIRef(performer_uri), URIRef(instrument_predicate), URIRef(instrument_uri)) )
                            foafClass = 'Person'
                        elif instrument_type == 'ROLE_GRP':
                            gEntities.add(
                                (URIRef(performer_uri), RDF.type, FOAF.Agent) )
                            gEntities.add(
                                (URIRef(performer_uri), RDFS.label, Literal(fullName)) )
                            gEntities.add(
                                (URIRef(performer_uri), URIRef(instrument_predicate), URIRef(instrument_uri)) )
                            foafClass = 'Agent'
                        elif instrument_type == 'ENS':
                            gEntities.add(
                                (URIRef(performer_uri), RDF.type, FOAF.Agent) )
                            gEntities.add(
                                (URIRef(performer_uri), RDF.type, mo.MusicArtist) )
                            gEntities.add(
                                (URIRef(performer_uri), RDFS.label, Literal(fullName)) )
                            gEntities.add(
                                (URIRef(performer_uri), URIRef(instrument_predicate), URIRef(instrument_uri)) )
                            foafClass = 'Agent'
                        elif instrument_type == 'ANIMAL':
                            gEntities.add(
                                (URIRef(performer_uri), RDF.type, dbp.animal) )
                            gEntities.add(
                                (URIRef(performer_uri), RDFS.label, Literal(fullName)) )
                            gEntities.add(
                                (URIRef(performer_uri), URIRef(instrument_predicate), URIRef(instrument_uri)) )
                            foafClass = 'Agent'

                dbpedia = row[13]
                lcnaf = row[14]
                mbz = row[15]
                geobirth = row[16]

                #make a new blank dict to put into our entityDict
                entityDict[str(address_id)] = {}

                #set the values
                entityDict[str(address_id)]['group uri'] = ''
                entityDict[str(address_id)]['first name'] = firstName
                entityDict[str(address_id)]['last name'] = lastName
                entityDict[str(address_id)]['full name'] = fullName
                entityDict[str(address_id)]['title'] = title
                entityDict[str(address_id)]['suffix'] = suffix
                entityDict[str(address_id)]['instrument'] = instrument_idList
                entityDict[str(address_id)]['birth date'] = birthDate
                entityDict[str(address_id)]['birth country id'] = birthCountry_id
                entityDict[str(address_id)]['death date'] = deathDate
                entityDict[str(address_id)]['dbpedia'] = dbpedia
                entityDict[str(address_id)]['geobirth'] = geobirth
                entityDict[str(address_id)]['lcnaf'] = lcnaf
                entityDict[str(address_id)]['mbz'] = mbz
                entityDict[str(address_id)]['uri'] = performer_uri
                entityDict[str(address_id)]['composer id'] = ''
                entityDict[str(address_id)]['foaf'] = foafClass


            else:
                instrument_id = row[12]
                instrument_name = instrumentDict[str(instrument_id)]['label']
                instrument_predicate = instrumentDict[str(instrument_id)]['predicate']
                instrument_uri = instrumentDict[str(instrument_id)]['uri']
                instrument_type = instrumentDict[str(instrument_id)]['typeIndicator']
                instrument_section = instrumentDict[str(instrument_id)]['section_id']

                if instrument_section != '26':## 26 is the section id for 'Non-performing'
                    if instrument_id not in instrument_idList:
                        instrument_idList.append(instrument_id)

                        gEntities.add(
                            (URIRef(performer_uri), URIRef(instrument_predicate), URIRef(instrument_uri)) )

                entityDict[str(address_id)]['instrument'] = instrument_idList

## Reset idList to check for repeat composer IDs during iteration
## Additional Group (e.g. composer, arranger, etc., represented here with a URI), additional links (e.g. dbpedia, lcnaf)
## cause repetition in CSV
idList = []
groupList = []

## Since links stored in repeatable name field in Composer, you don't know which link (if any) you'll get
## on each iteration; list provides variables to use for assigning correct links


with open(filePath_3, 'rU') as f3:
    composers = csv.reader(f3, dialect='excel', delimiter=',', quotechar='"')
    for row in composers:
        composer_id = row[0]
        ## Create new entity ID for stand-alone (non-performer) composers, e.g. Beethoven
        entity_id = str(int(composer_id) + 1000000)
        addressLink = row[1]
        if addressLink != '0':
            composer_uri = entityDict[str(addressLink)]['uri']
            foafClass = entityDict[str(addressLink)]['foaf']
        else:
            composer_uri = chnames[entity_id]

        groupURI = row[2]
        lastName = row[3]
        firstName = row[4]
        birthDay = row[5]
        birthMonth = row[6]
        birthYear = row[7]
        birthCountry_id = row[8]
        deathDay = row[9]
        deathMonth = row[10]
        deathYear = row[11]
        gender = row[12]

        composer = Entity([firstName, lastName], (
            [birthYear, birthMonth, birthDay], [deathYear, deathMonth, deathDay]))

        fullName = composer.create_entity_name()
        birthDate = composer.create_entity_dates()[0]
        deathDate = composer.create_entity_dates()[1]

        if composer_id not in idList:
            groupList = []
            idList.append(composer_id)
            if groupURI:
                groupList.append(groupURI)
                if groupURI not in ('reference', 'subject'):
                    gEntities.add(
                        (URIRef(composer_uri), gndo.professionOrOccupation, URIRef(groupURI)) )
            else:
                groupURI = 'http://id.loc.gov/vocabulary/relators/cmp'
                groupList.append(groupURI)
                gEntities.add(
                    (URIRef(composer_uri), gndo.professionOrOccupation, URIRef(groupURI)) )

            ## This section deals with external URI references
            linkCode = row[13]
            link = row[14]
            linkDict = {'dbpedia': '', 'lcnaf': '', 'mbz': '', 'geobirth': ''}
            if linkCode in linkDict:
                linkDict[str(linkCode)] = link

            if addressLink == '0':
                ## If there is no addressLink it means this is a new entity
                ## Index uses new ID that has been padded to 1 million
                ## We still store the original composer ID so we can link to works records

                if groupURI not in ('reference', 'subject'):
                        if gender:
                                foafClass = 'Person'
                                gEntities.add (
                                        (URIRef(composer_uri), RDF.type, FOAF.Person) )
                                gEntities.add(
                                        (URIRef(composer_uri), FOAF.name, Literal(fullName)) )
                        else:
                                foafClass = 'Agent'
                                gEntities.add (
                                        (URIRef(composer_uri), RDF.type, FOAF.Agent) )
                                gEntities.add(
                                        (URIRef(composer_uri), RDFS.label, Literal(fullName)) )
                elif groupURI != 'reference':
                        gEntities.add(
                                (URIRef(composer_uri), RDFS.label, Literal(fullName)) )
                
                entityDict[str(entity_id)] = {}
                entityDict[str(entity_id)]['composer id'] = composer_id
                entityDict[str(entity_id)]['uri'] = composer_uri
                entityDict[str(entity_id)]['group uri'] = groupList
                entityDict[str(entity_id)]['first name'] = firstName
                entityDict[str(entity_id)]['last name'] = lastName
                entityDict[str(entity_id)]['full name'] = fullName
                entityDict[str(entity_id)]['instrument'] = []
                entityDict[str(entity_id)]['birth date'] = birthDate
                entityDict[str(entity_id)]['birth country id'] = birthCountry_id
                entityDict[str(entity_id)]['death date'] = deathDate
                entityDict[str(entity_id)]['foaf'] = foafClass
                entityDict[str(entity_id)]['address book link'] = ''
                for link in linkDict:
                    entityDict[str(entity_id)][str(link)] = linkDict[link]

            else:
                ## If there IS an addressLink, entity exists, and we update the entityDict
                ## Original entity name (from Address Book) does not need to change
                ## Birth/death dates, external links might NOT be in address book, so we add/replace them

                if not foafClass:#Composer was not a performer, but was in Address Book as Licensee
                        if gender:
                                foafClass = 'Person'
                                gEntities.add (
                                        (URIRef(composer_uri), RDF.type, FOAF.Person) )
                                gEntities.add(
                                        (URIRef(composer_uri), FOAF.name, Literal(fullName)) )
                        else:
                                foafClass = 'Agent'
                                gEntities.add (
                                        (URIRef(composer_uri), RDF.type, FOAF.Agent) )
                                gEntities.add(
                                        (URIRef(composer_uri), RDFS.label, Literal(fullName)) )

                        entityDict[str(addressLink)]['foaf'] = foafClass
                
                entityDict[str(addressLink)]['composer id'] = composer_id
                entityDict[str(addressLink)]['group uri'] = groupList
                entityDict[str(addressLink)]['birth date'] = birthDate
                entityDict[str(addressLink)]['death date'] = deathDate
                entityDict[str(addressLink)]['address book link'] = addressLink
                if linkCode in linkDict:
                    entityDict[str(addressLink)][str(linkCode)] = link

        else:
            linkCode = row[13]
            link = row[14]

            if groupURI:
                if groupURI not in groupList:
                    groupList.append(groupURI)
                    if groupURI not in ('reference', 'subject'):
                        gEntities.add(
                            (URIRef(composer_uri), gndo.professionOrOccupation, URIRef(groupURI)) )
            else:
                groupURI = 'http://id.loc.gov/vocabulary/relators/cmp'
                if groupURI not in groupList:
                    groupList.append(groupURI)
                    gEntities.add(
                        (URIRef(composer_uri), gndo.professionOrOccupation, URIRef(groupURI)) )


            if addressLink == '0':
                if linkCode in linkDict:
                    entityDict[str(entity_id)][str(linkCode)] = link
            else:
                if linkCode in linkDict:
                    entityDict[str(addressLink)][str(linkCode)] = link

## Since dates, birthplace URI and sameAs links may/may not agree between Address Book and Composers
## for linked entities, these are not added to graph until full entityDict has been created
for key in entityDict:
    entityURI = entityDict[str(key)]['uri']
    composer_id = entityDict[str(key)]['composer id']
    instrument = entityDict[str(key)]['instrument']
    groupList = entityDict[str(key)]['group uri']
    birthDate = entityDict[str(key)]['birth date']
    deathDate = entityDict[str(key)]['death date']

    if (not composer_id and not instrument):
            if int(key) < 1000000:
                    continue
    else:
        if birthDate != 'unknown':
                if len(birthDate) == 10:
                        gEntities.add(
                                (URIRef(entityURI), schema.birthDate, Literal(birthDate, datatype=XSD.date)) )
                elif len(birthDate) == 7:
                        gEntities.add(
                                (URIRef(entityURI), schema.birthDate, Literal(birthDate, datatype=XSD.gYearMonth)) )
                elif len(birthDate) == 4:
                        gEntities.add(
                                (URIRef(entityURI), schema.birthDate, Literal(birthDate, datatype=XSD.gYear)) )
        if deathDate != 'unknown':
                if len(deathDate) == 10:
                        gEntities.add(
                                (URIRef(entityURI), schema.deathDate, Literal(deathDate, datatype=XSD.date)) )
                elif len(deathDate) == 7:
                        gEntities.add(
                                (URIRef(entityURI), schema.deathDate, Literal(deathDate, datatype=XSD.gYearMonth)) )
                elif len(deathDate) == 4:
                        gEntities.add(
                                (URIRef(entityURI), schema.deathDate, Literal(deathDate, datatype=XSD.gYear)) )

        dbpedia = entityDict[str(key)]['dbpedia']
        if dbpedia:
                if 'subject' in groupList:
                                gEntities.add( (URIRef(entityURI), SKOS.closeMatch, URIRef(dbpedia)) )
                else:
                                gEntities.add( (URIRef(entityURI), OWL.sameAs, URIRef(dbpedia)) )

        lcnaf = entityDict[str(key)]['lcnaf']
        if lcnaf:
                if 'subject' in groupList:
                                gEntities.add( (URIRef(entityURI), SKOS.closeMatch, URIRef(lcnaf)) )
                else:
                                gEntities.add( (URIRef(entityURI), OWL.sameAs, URIRef(lcnaf)) )

        mbz = entityDict[str(key)]['mbz']
        if mbz:
                gEntities.add( (URIRef(entityURI), OWL.sameAs, URIRef(mbz)) )

        geobirth = entityDict[str(key)]['geobirth']
        birthCountry_id = entityDict[str(key)]['birth country id']
        if geobirth:
                gEntities.add( (URIRef(entityURI), dbp.birthPlace, URIRef(geobirth)) )
        else:
                if birthCountry_id != '0':
                        geobirth = countryDict[str(birthCountry_id)]['uri']
                        entityDict[str(key)]['geobirth'] = geobirth
                        gEntities.add( (URIRef(entityURI), dbp.birthPlace, URIRef(geobirth)) )

country_dict_path = os.path.join(os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'countryDict.json')
instrument_dict_path = os.path.join(os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'instrumentDict.json')
entity_dict_path = os.path.join(os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'entityDict.json')
instruments_graph_path = os.path.join(os.path.dirname(__file__), os.pardir, 'Graphs', 'instrumentGraph.nt')
entity_graph_path = os.path.join(os.path.dirname(__file__), os.pardir, 'Graphs', 'entityGraph.nt')

gInstruments.bind("rdfs", RDFS)
gInstruments.bind("rdf", RDF)
gInstruments.bind("owl", OWL)
gEntities.bind("dbpedia-owl", dbp)
gEntities.bind("foaf", FOAF)
gEntities.bind("gndo", gndo)
gEntities.bind("mo", mo)
gEntities.bind("rdf", RDF)
gEntities.bind("rdfs", RDFS)
gEntities.bind("schema", schema)
gEntities.bind("skos", SKOS)

gInstruments = gInstruments.serialize(destination=instruments_graph_path, format='nt')
gEntities = gEntities.serialize(destination=entity_graph_path, format='nt')

with open(country_dict_path, 'w') as f1:
    json.dump(countryDict, f1)

with open(instrument_dict_path, 'w') as f2:
    json.dump(instrumentDict, f2)

with open(entity_dict_path, 'w') as f3:
    json.dump(entityDict, f3)

print("Finished processing Entities")
