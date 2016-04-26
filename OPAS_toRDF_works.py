# !/usr/local/bin/python3.4.2
# ----Copyright (c) 2016 Carnegie Hall | The MIT License (MIT)----
# ----For the full license terms, please visit https://github.com/CarnegieHall/quality-control/blob/master/LICENSE----

## Argument[0] is script to run
## Argument[1] is path to genres CSV
## Argument[2] is path to composers CSV
## Argument[3] is path to Works CSV

import csv
import json
import rdflib
from rdflib import Graph, Literal, Namespace, OWL, RDF, URIRef, XSD
from rdflib.namespace import DCTERMS, FOAF, OWL, RDF, RDFS, SKOS
from rdflib.plugins.serializers.nt import NTSerializer
import os
import sys

genreDict = {}
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
filePath_3 = sys.argv[3]

with open(filePath_1, 'rU') as f1:
    genres = csv.reader(f1, dialect='excel', delimiter=',', quotechar='"')
    for row in genres:
        genre_id = row[0]
        label = row[1]

        if genre_id in ('18', '52', '53', '75', '178', '181', '185'):
            genre_category = 'non-musical'
        else:
            genre_category = 'MusicalWork'

        genreDict[str(genre_id)] = {}
        genreDict[str(genre_id)]['label'] = label
        genreDict[str(genre_id)]['category'] = genre_category

composer_idList = []
work_idList = []
contributor_idList = []

## Reading composers from unified Entity dict is tricky, since if composer is also a performer,
## he/she is assigned a new ID (oldID + 1000000). Instead, re-opening Composers CSV temporarily
## to facilitate mapping a work to its composer. Since URIs are created from the ID, we just
## re-create the composer URI in this temporary dict
composers_tempDict = {}

with open(filePath_2, 'rU') as f2:
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

with open(filePath_3, 'rU') as f3:
    works = csv.reader(f3, dialect='excel', delimiter=',', quotechar='"')
    for row in works:
        work_id = row[0]
        work_uri = chworks[work_id]
        composer_id = row[1]
        composer_uri = composers_tempDict[composer_id]['uri']
        printTitle = row[2]
        dateCirca = row[3]
        if dateCirca == 'c':
            dateCirca = 'c. '
        if dateCirca == 'C':
            dateCirca = 'c. '
        if dateCirca == '?':
            dateCirca = 'c. '
        if dateCirca == '-':
            dateCirca = 'before '
        dateStart = row[4]
        dateEnd = row[5]
        if dateCirca:
            if dateEnd:
                date = ''.join([dateCirca, dateStart, '-', dateEnd])
            else:
                date = ''.join([dateCirca, dateStart])
        else:
            if dateStart:
                if dateEnd:
                    date = ''.join([dateStart, '-', dateEnd])
                else:
                    date = dateStart
            else:
                date = ''

        contributor_id = row[6]
        contributor_role = row[7]
        contributorDict = {}
        if contributor_id:
            contributorDict['id'] = contributor_id
            contributorDict['role'] = contributor_role


        if work_id not in work_idList:
            work_idList.append(work_id)

            linkCode = row[8]
            link = row[9]
            linkDict = {'dbpedia': '', 'lcnaf': '', 'mbz': ''}
            if linkCode in linkDict:
                linkDict[str(linkCode)] = link

            genre_id = row[10]

            gWorks.add( (URIRef(work_uri), RDFS.label, Literal(printTitle.encode('utf-8')) ) )

            if genre_id != '0':
                if genreDict[str(genre_id)] != 'non-musical':
                    gWorks.add( (URIRef(work_uri), RDF.type, mo.MusicalWork ) )
                    gWorks.add( (URIRef(work_uri), RDF.type, gndo.MusicalWork ) )
                    gWorks.add( (URIRef(work_uri), RDF.type, schema.MusicComposition ) )
                    gWorks.add( (URIRef(work_uri), DCTERMS.creator, URIRef(composer_uri) ) )
                else:
                    gWorks.add( (URIRef(work_uri), RDF.type, gndo.Work ) )
                    gWorks.add( (URIRef(work_uri), RDF.type, schema.CreativeWork ) )
            if date:
                if len(date) == 4:
                    gWorks.add( (URIRef(work_uri), DCTERMS.created, Literal(date, datatype=XSD.gYear) ) )
                else:
                    gWorks.add( (URIRef(work_uri), DCTERMS.created, Literal(date) ) )

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
            worksDict[str(work_id)]['title'] = printTitle
            worksDict[str(work_id)]['composer_id'] = composer_id
            worksDict[str(work_id)]['contributor'] = contributorList
            worksDict[str(work_id)]['date'] = date
            worksDict[str(work_id)]['uri'] = work_uri
            worksDict[str(work_id)]['genre_id'] = genre_id
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


genre_dict_path = os.path.join(os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'genreDict.json')
works_dict_path = os.path.join(os.path.dirname(__file__), os.pardir, 'JSON_dicts', 'worksDict.json')
works_graph_path = os.path.join(os.path.dirname(__file__), os.pardir, 'Graphs', 'worksGraph.nt')

gWorks.bind("dbpedia", dbpedia)
gWorks.bind("dcterms", DCTERMS)
gWorks.bind("foaf", FOAF)
gWorks.bind("gndo", gndo)
gWorks.bind("mo", mo)
gWorks.bind("rdf", RDF)
gWorks.bind("rdfs", RDFS)
gWorks.bind("schema", schema)

gWorks = gWorks.serialize(destination=works_graph_path, format='nt')

with open(genre_dict_path, 'w') as f1:
    json.dump(genreDict, f1)

with open(works_dict_path, 'w') as f2:
    json.dump(worksDict, f2)

print('Finished processing Works')

