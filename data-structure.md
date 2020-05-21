# Carnegie Hall Linked Open Data Structure

## OVERVIEW

This page provides details about the creation and structure of Carnegie Hall (CH) Linked Open Data (LOD). To learn more about the project and content of the dataset, please see the CH LOD repository's [README](./README.md).

🔴 Query the data [here](http://data.carnegiehall.org).  
🔴 Visit our Carnegie Hall Data Lab, a learning space for us to experiment with LOD and semantic technologies, [here](https://carnegiehall.github.io/datalab/).

## ADDITIONAL DOCUMENTATION

Details about the following topics are available in the dedicated pages linked below.

| Topic  |  See... |
|---|---|
| Namespaces |[ch-lod-namespaces.md](./ch-lod-namespaces.md)|
| Classes |[ch-lod-classes.md](./ch-lod-classes.md)|
|Properties|[ch-lod-properties.md](./ch-lod-properties.md)|

## DATA MODEL

To reiterate, CH performance data has two distinct layers of metadata: **event** and **work performance** (sub-event).
 
![CH LOD Data Model diagram](/CarnegieHall_LOD_DataModel_detail_20200219.png) 

You can download the CH LOD Data model diagram [here](/CarnegieHall_LOD_DataModel_detail_20200219.png). If you'd prefer to view/download the [data model in XML](https://drive.google.com/file/d/1yyfv2da8N1JioahI5LqDdLUck84CmNs-/view?usp=sharing) you can use Draw.io. 

### Sample Event Record

Below is a CH event record (in Turtle format), followed by statements about one of the work performances and a related performer from the event. View an [HTML representation](https://www.carnegiehall.org/About/History/Performance-History-Search?q=&dex=prod_PHS&page=2&event=8195&pf=Boston%20Symphony%20Orchestra_Max%20Fiedler_) of this event on the Carnegie Hall Performance History Search.

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

Something in this document unclear? Have a suggestions or comment about a topic described above? Submit your feedback via ['Issues'](https://github.com/CarnegieHall/linked-data/issues).

----------------------------
Go to: [README](/README.md) | [SPARQL ENDPOINT](http://data.carnegiehall.org)
