# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2016 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/linked-data/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to composers CSV
## Argument[2] is path to Works CSV

import csv
import json
import rdflib
from rdflib import Graph, Literal, Namespace, OWL, RDF, URIRef, XSD
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS
from rdflib.plugins.serializers.nt import NTSerializer
import os
import sys

class Work(object):

    def __init__(self, title, dates):
        self.title = title
        self.dates = dates
    def create_work_dates(self):
        dateCirca = self.dates[0]
        if dateCirca == 'c':
            dateCirca = 'c. '
        if dateCirca == 'C':
            dateCirca = 'c. '
        if dateCirca == '?':
            dateCirca = 'c. '
        if dateCirca == '-':
            dateCirca = 'before '

        dateStart = self.dates[1]
        dateEnd = self.dates[2]
        if dateCirca:
            if dateEnd:
                workDate = ''.join([dateCirca, dateStart, '-', dateEnd])
            else:
                workDate = ''.join([dateCirca, dateStart])
        else:
            if dateStart:
                if dateEnd:
                    workDate = ''.join([dateStart, '-', dateEnd])
                else:
                    workDate = dateStart
            else:
                workDate = ''
        return workDate

groupsDict = {}
worksDict = {}
contributorList = []

gWorks = Graph()

chnames = Namespace('http://data.carnegiehall.org/names/')
chworks = Namespace('http://data.carnegiehall.org/works/')
dbpedia = Namespace('http://dbpedia.org/resource/')
gndo = Namespace('http://d-nb.info/standards/elementset/gnd#')
mbz = Namespace('https://musicbrainz.org/artist/')
mo = Namespace ('http://purl.org/ontology/mo/')
schema = Namespace('http://schema.org/')

filePath_1 = sys.argv[1]
filePath_2 = sys.argv[2]

composer_idList = []
work_idList = []
contributor_idList = []

## Reading composers from unified Entity dict is tricky, since if composer is also a performer,
## he/she is assigned a new ID (oldID + 1000000). Instead, re-opening Composers CSV temporarily
## to facilitate mapping a work to its composer. Since URIs are created from the ID, we just
## re-create the composer URI in this temporary dict
composers_tempDict = {}

with open(filePath_1, 'rU') as f2:
    composers = csv.reader(f2, dialect='excel', delimiter=',', quotechar='"')
    for row in composers:
        composer_id = row[0]
        ## Create new entity ID for stand-alone (non-performer) composers, e.g. Beethoven
        entity_id = str(int(composer_id) + 1000000)
        addressLink = row[1]
        groupURI = row[2]
        if addressLink != '0':
            composer_uri = chnames[addressLink]
        else:
            composer_uri = chnames[entity_id]

        if composer_id not in composer_idList:
            composers_tempDict[str(composer_id)] = {}
            composers_tempDict[str(composer_id)]['uri'] = composer_uri
            if groupURI:
                composers_tempDict[str(composer_id)]['group uri'] = groupURI
            else:
                groupURI = 'http://id.loc.gov/vocabulary/relators/cmp'
                composers_tempDict[str(composer_id)]['group uri'] = groupURI

with open(filePath_2, 'rU') as f3:
    works = csv.reader(f3, dialect='excel', delimiter=',', quotechar='"')
    for row in works:
        work_id = row[0]
        work_uri = chworks[work_id]
        composer_id = row[1]
        composer_uri = composers_tempDict[composer_id]['uri']
        title = row[2]
        dateCirca = row[3]
        dateStart = row[4]
        dateEnd = row[5]
        contributor_id = row[6]
        contributor_role = row[7]
        contributorDict = {}
        if contributor_id:
            contributorDict['id'] = contributor_id
            contributorDict['role'] = contributor_role

        work = Work(title, [dateCirca, dateStart, dateEnd])
        work_date = work.create_work_dates()

        if work_id not in work_idList:
            work_idList.append(work_id)

            linkCode = row[8]
            link = row[9]
            linkDict = {'dbpedia': '', 'lcnaf': '', 'mbz': ''}
            if linkCode in linkDict:
                linkDict[str(linkCode)] = link

            genre_code = row[10]

            gWorks.add( (URIRef(work_uri), RDFS.label, Literal(work.title.encode('utf-8')) ) )

            if genre_code != 'non-musical':
                gWorks.add( (URIRef(work_uri), RDF.type, mo.MusicalWork ) )
                gWorks.add( (URIRef(work_uri), RDF.type, gndo.MusicalWork ) )
                gWorks.add( (URIRef(work_uri), RDF.type, schema.MusicComposition ) )
                gWorks.add( (URIRef(work_uri), DCTERMS.creator, URIRef(composer_uri) ) )
            else:
                gWorks.add( (URIRef(work_uri), RDF.type, gndo.Work ) )
                gWorks.add( (URIRef(work_uri), RDF.type, schema.CreativeWork ) )
            if work_date:
                if len(work_date) == 4:
                    gWorks.add(
                        (URIRef(work_uri), DCTERMS.created, Literal(work_date, datatype=XSD.gYear) ) )
                else:
                    gWorks.add( (URIRef(work_uri), DCTERMS.created, Literal(work_date) ) )

            if contributor_id != '0':
                contributor_idList = []
                contributor_idList.append(contributor_id)
                contributorList = [contributorDict]
                contributor_uri = composers_tempDict[str(contributor_id)]['uri']

                gWorks.add( (URIRef(work_uri), URIRef(contributor_role), URIRef(contributor_uri) ) )
                gWorks.add( (URIRef(work_uri), DCTERMS.contributor, URIRef(contributor_uri) ) )
            else:
                contributorList = ''


            worksDict[str(work_id)] = {}
            worksDict[str(work_id)]['title'] = work.title
            worksDict[str(work_id)]['composer_id'] = composer_id
            worksDict[str(work_id)]['contributor'] = contributorList
            worksDict[str(work_id)]['date'] = work_date
            worksDict[str(work_id)]['uri'] = work_uri
            worksDict[str(work_id)]['genre_code'] = genre_code
            for link in linkDict:
                worksDict[str(work_id)][link] = linkDict[link]
        else:
            if contributor_id != '0':
                if contributor_id not in contributor_idList:
                    contributor_idList.append(contributor_id)
                    contributorList.append(contributorDict)
                    worksDict[str(work_id)]['contributor'] = contributorList
                    contributor_uri = composers_tempDict[str(contributor_id)]['uri']

                    gWorks.add( (URIRef(work_uri), URIRef(contributor_role), URIRef(contributor_uri) ) )

            linkCode = row[8]
            link = row[9]
            if linkCode in linkDict:
                worksDict[str(work_id)][str(linkCode)] = link

for key in worksDict:
    work_uri = worksDict[key]['uri']
    dbpedia_link = worksDict[key]['dbpedia']
    lcnaf_link = worksDict[key]['lcnaf']
    mbz_link = worksDict[key]['mbz']

    if dbpedia_link:
        gWorks.add( (URIRef(work_uri), OWL.sameAs, URIRef(dbpedia_link)) )
    if lcnaf_link:
        gWorks.add( (URIRef(work_uri), OWL.sameAs, URIRef(lcnaf_link)) )
    if mbz_link:
        gWorks.add( (URIRef(work_uri), OWL.sameAs, URIRef(mbz_link)) )


works_dict_path = os.path.join(os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'worksDict.json')
works_graph_path = os.path.join(os.path.dirname(__file__), os.pardir, 'Graphs', 'worksGraph.nt')

gWorks.bind("dbpedia", dbpedia)
gWorks.bind("dcterms", DCTERMS)
gWorks.bind("gndo", gndo)
gWorks.bind("mo", mo)
gWorks.bind("rdf", RDF)
gWorks.bind("rdfs", RDFS)
gWorks.bind("schema", schema)

gWorks = gWorks.serialize(destination=works_graph_path, format='nt')

with open(works_dict_path, 'w') as f2:
    json.dump(worksDict, f2)

print('Finished processing Works')

