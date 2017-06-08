# Carnegie Hall Linked Open Data Structure

## OVERVIEW

This page provides details about the creation and structure of Carnegie Hall (CH) Linked Open Data (LOD). To learn more about the project and content of the dataset, please see the CH LOD repository's README. (link)

Query the data here.[link]

## ADDITIONAL DOCUMENTS
| Topic  |  See... |
|---|---|
| Namespaces used or created ||
| Schemas and vocabularies ||
|Properties||

## DATA MODEL

[intro]

View CH LOD Data Model here(link). You can also download it in XML.

### Sample Event Record

Below is a CH event record (in Turtle format), followed by statements about one of the work performances and a related performer from the event.
```
<http://data.carnegiehall.org/events/8195> a <http://erlangen-crm.org/160714/E7_Activity>, 
        event:Event ; 
    rdfs:label "Boston Symphony Orchestra"@en ; 
    event:place <http://data.carnegiehall.org/venues/5> ; 
    event:product <http://data.carnegiehall.org/events/8195/work_01>, 
        <http://data.carnegiehall.org/events/8195/work_02>, 
        <http://data.carnegiehall.org/events/8195/work_03>, 
        <http://data.carnegiehall.org/events/8195/work_04> ; 
    dcterms:date "1909-11-13T14:30:00-05:00"^^xsd:dateTime ; 
    mo:conductor <http://data.carnegiehall.org/names/47438> ; 
    mo:performer <http://data.carnegiehall.org/names/22864> . 
<http://data.carnegiehall.org/events/8195/work_03> a event:Product ; 
    event:product <http://data.carnegiehall.org/works/18637> ; 
    mo:performer <http://data.carnegiehall.org/names/52002> . 
<http://data.carnegiehall.org/works/18637> a gndo:MusicalWork, 
        mo:MusicalWork, 
        schema:MusicComposition ; 
    rdfs:label "Piano Concerto No. 2 in C Minor, Op. 18" ; 
    dcterms:created "1900-1901" ; 
    dcterms:creator <http://data.carnegiehall.org/names/52002> ; 
    skos:exactMatch <http://dbpedia.org/resource/Piano_Concerto_No._2_(Rachmaninoff)>, 
        lcnaf:n81147588, 
        <https://musicbrainz.org/work/aca4167a-b927-41f5-a839-99cf9ad476cc> . 
<http://data.carnegiehall.org/names/52002> a foaf:Person ; 
    gndo:playedInstrument <http://data.carnegiehall.org/instruments/783> ; 
    gndo:professionOrOccupation <http://data.carnegiehall.org/roles/439>, 
        lcMarRel:arr, 
        lcMarRel:cmp, 
        lcMarRel:trc ; 
    dbpedia-owl:birthPlace <http://sws.geonames.org/515246/> ; 
    schema:birthDate "1873-04-01"^^xsd:date ; 
    schema:deathDate "1943-03-28"^^xsd:date ; 
    skos:exactMatch dbpedia:Sergei_Rachmaninoff, 
        lcnaf:n50054908, 
        <http://musicbrainz.org/artist/44b16e44-da77-4580-b851-0d765904573e> ; 
    foaf:name "Sergei Rachmaninoff" .
 ```

## GET INVOLVED

Something in this document unclear? Have a suggestions or comment about a topic described above? Submit your feedback via ['Issues']().
