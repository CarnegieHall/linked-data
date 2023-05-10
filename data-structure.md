# Carnegie Hall Linked Open Data Structure

## OVERVIEW

This page provides details about the creation and structure of Carnegie Hall (CH) Linked Open Data (LOD). To learn more about the project and content of the dataset, please see the CH LOD repository's [README](./README.md).

🔴 Query the data [here](http://data.carnegiehall.org/sparql/).  
🔴 Visit our Carnegie Hall Data Lab, a learning space for us to experiment with LOD and semantic technologies, [here](http://data.carnegiehall.org/datalab/).

## ADDITIONAL DOCUMENTATION

Details about the following topics are available in the dedicated pages linked below.

| Topic  |  See... |
|---|---|
| Namespaces |[ch-lod-namespaces.md](./ch-lod-namespaces.md)|
| Classes |[ch-lod-classes.md](./ch-lod-classes.md)|
|Properties|[ch-lod-properties.md](./ch-lod-properties.md)|

## DATA MODEL

To reiterate, CH performance data has two distinct layers of metadata: **event** and **work performance** (sub-event).
 
![CH LOD Data Model diagram](/CarnegieHall_LOD_DataModel_detail_20230510.png) 

You can download the CH LOD Data model diagram [here](/CarnegieHall_LOD_DataModel_detail_20230510.png). 

### Sample Event Record

Below is a CH event record (in Turtle format), followed by statements about one of the work performances and a related performer from the event. View an [HTML representation](https://www.carnegiehall.org/About/History/Performance-History-Search?q=&dex=prod_PHS&page=2&event=8195&pf=Boston%20Symphony%20Orchestra_Max%20Fiedler_) of this event on the Carnegie Hall Performance History Search.

```
@prefix schema: <http://schema.org/> .
@prefix chEvents: <http://data.carnegiehall.org/events/> .
@prefix chVenues: <http://data.carnegiehall.org/venues/> .
@prefix chNames: <http://data.carnegiehall.org/names/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

chEvents:8195 a schema:Event ;
   rdfs:label "Boston Symphony Orchestra"@en ;
   schema:location chVenues:5 ;
   schema:organizer chNames:22864 ;
   schema:subEvent <http://data.carnegiehall.org/events/8195/work_04> , <http://data.carnegiehall.org/events/8195/work_02> , <http://data.carnegiehall.org/events/8195/work_01> , <http://data.carnegiehall.org/events/8195/work_03> ;
   rdfs:comment """NEW YORK PREMIERE of Granville Bantock's PIERROT OF THE MINUTE
"""@en ;
   schema:description "symphony orchestra performance" ;
   schema:startDate "1909-11-13T14:30:00"^^<http://www.w3.org/2001/XMLSchema#dateTime> ;
   <http://data.carnegiehall.org/vocabulary/roles/conductor> chNames:47438 ;
   <http://data.carnegiehall.org/vocabulary/roles/orchestra> chNames:22864 .


<http://data.carnegiehall.org/venues/5> a schema:EventVenue ;
   rdfs:label "Main Hall"@en ;
   schema:containedInPlace <http://data.carnegiehall.org/venues/96397> ;
   rdfs:comment "Main Hall is the designation applied to the main Carnegie Hall auditorium from 1891-1997, when it was renamed Isaac Stern Auditorium in honor of violinist Isaac Stern, President of Carnegie Hall (1960-2001). In 2006 the stage was dedicated the Ronald O. Perelman Stage."@en .

<http://data.carnegiehall.org/events/8195/work_03> a <http://data.carnegiehall.org/model/WorkPerformance> ;
   rdfs:label "Piano Concerto No. 2 in C Minor, Op. 18" ;
   <http://purl.org/ontology/mo/performer> <http://data.carnegiehall.org/names/52002> ;
   schema:workPerformed <http://data.carnegiehall.org/works/18637> ;
   <http://data.carnegiehall.org/vocabulary/roles/piano> <http://data.carnegiehall.org/names/52002> .

<http://data.carnegiehall.org/works/18637> a schema:CreativeWork , schema:MusicComposition ;
   rdfs:label "Piano Concerto No. 2 in C Minor, Op. 18" ;
   <http://purl.org/dc/terms/creator> <http://data.carnegiehall.org/names/52002> ;
   schema:dateCreated "1900-1901" ;
   <http://www.w3.org/2004/02/skos/core#exactMatch> <http://dbpedia.org/resource/Piano_Concerto_No._2_(Rachmaninoff)> , <http://id.loc.gov/authorities/names/n81147588> , <https://musicbrainz.org/work/aca4167a-b927-41f5-a839-99cf9ad476cc> , <http://www.wikidata.org/entity/Q210224> .

<http://data.carnegiehall.org/names/52002> a <http://data.carnegiehall.org/model/Entity> , schema:Person ;
   rdfs:label "Sergei Rachmaninoff" ;
   <http://d-nb.info/standards/elementset/gnd#playedInstrument> <http://data.carnegiehall.org/instruments/783> ;
   schema:birthPlace <http://sws.geonames.org/515246/> ;
   schema:hasOccupation <http://data.carnegiehall.org/roles/439> , <http://id.loc.gov/vocabulary/relators/cmp> , <http://id.loc.gov/vocabulary/relators/arr> , <http://id.loc.gov/vocabulary/relators/trc> ;
   schema:birthDate "1873-04-01"^^<http://www.w3.org/2001/XMLSchema#date> ;
   schema:deathDate "1943-03-28"^^<http://www.w3.org/2001/XMLSchema#date> ;
   schema:name "Sergei Rachmaninoff" ;
   <http://www.w3.org/2004/02/skos/core#exactMatch> <http://dbpedia.org/resource/Sergei_Rachmaninoff> ,     <http://id.loc.gov/authorities/names/n50054908> , <http://musicbrainz.org/artist/44b16e44-da77-4580-b851-0d765904573e> , <http://www.wikidata.org/entity/Q131861> .
 ```

## GET INVOLVED

Something in this document unclear? Have a suggestions or comment about a topic described above? Submit your feedback via ['Issues'](https://github.com/CarnegieHall/linked-data/issues).

----------------------------
Go to: [README](/README.md) | [SPARQL ENDPOINT](http://data.carnegiehall.org)
