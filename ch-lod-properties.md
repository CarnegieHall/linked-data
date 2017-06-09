# Carnegie Hall Linked Open Data - Properties

## OVERVIEW

## PROPERTIES USED
|Property|Vocabulary|CH Usage|
|:----|:---|:---|
|[name](http://xmlns.com/foaf/0.1/name)|[Friend Of A Friend (FOAF)](http://xmlns.com/foaf/0.1/)|Relates the URI of an entity (e.g. composer, performer, conductor) to a human-readable version of their name (text string)|
|[professionOrOccupation](http://d-nb.info/standards/elementset/gnd#professionOrOccupation)|[GND (German National Library) Ontology](http://d-nb.info/standards/elementset/gnd)|Relates the URI of an entity to the URI of his/her/its role (e.g. conductor, dancer, orchestra, string quartet)|
|[playedInstrument](http://d-nb.info/standards/elementset/gnd#playedInstrument)|[GND (German National Library) Ontology](http://d-nb.info/standards/elementset/gnd)|Relates the URI of an entity to the URI of his/her instrument|
|[birthPlace](http://dbpedia.org/ontology/birthPlace)|[DBPedia Ontology](http://dbpedia.org/ontology/)|Relates the URI of an entity (e.g. composer, performer, conductor) to the GeoNames URI for the birth place|
|[birthDate](http://schema.org/birthDate)|[Schema.org](http://schema.org/)|Relates the URI of an entity (e.g. composer, performer, conductor) to a date of birth|
|[deathDate](http://schema.org/deathDate)|[Schema.org](http://schema.org/)|Relates the URI of an entity (e.g. composer, performer, conductor) to a date of death|
|[containsPlace](http://schema.org/containsPlace)|[Schema.org](http://schema.org/)|Relates the URI for Carnegie Hall (the building) to its constituent venues|
|[creator](http://purl.org/dc/terms/creator)|[DCMI Metadata Terms (dcterms)]()|Relates the URI of a creative work to the URI of its creator (e.g. composer, playwright, etc.)|
|[contributor](http://purl.org/dc/terms/contributor)|[DCMI Metadata Terms (dcterms)]()|Relates the URI of a creative work to the URI of a contributor (i.e. co-composer, arranger, librettist)|
|[created](http://purl.org/dc/terms/created)|[DCMI Metadata Terms (dcterms)](http://purl.org/dc/terms/)|Relates the URI of a creative work to the date/s of its creation|
|[date](http://purl.org/dc/terms/date)|[DCMI Metadata Terms (dcterms)](http://purl.org/dc/terms/)|Relates the URI of an event to the date/time on which it occurred (ISO 8601-formatted datetime string)|
|[arr](http://id.loc.gov/vocabulary/relators/arr)|[MARC Role Relators](http://id.loc.gov/vocabulary/relators/)|Relates the URI of a musical work to the URI of an arranger|
|[aut](http://id.loc.gov/vocabulary/relators/aut)|[MARC Role Relators](http://id.loc.gov/vocabulary/relators/)|Relates the URI of a creative work to the URI of an editor|
|[edt](http://id.loc.gov/vocabulary/relators/edt)|[MARC Role Relators](http://id.loc.gov/vocabulary/relators/)|Relates the URI of a creative work to the URI of an author of the text|
|[lbt](http://id.loc.gov/vocabulary/relators/lbt)|[MARC Role Relators](http://id.loc.gov/vocabulary/relators/)|Relates the URI of a musical work to the URI of a librettist|
|[lyr](http://id.loc.gov/vocabulary/relators/lyr)|[MARC Role Relators](http://id.loc.gov/vocabulary/relators/)|Relates the URI of a musical work to the URI of a lyricist|
|[trc](http://id.loc.gov/vocabulary/relators/trc)|[MARC Role Relators](http://id.loc.gov/vocabulary/relators/)|Relates the URI of a musical work to the URI of a transcriber|
|[trl](http://id.loc.gov/vocabulary/relators/trl)|[MARC Role Relators](http://id.loc.gov/vocabulary/relators/)|Relates the URI of a creative work to the URI of a translator of the text|
|[place](http://purl.org/NET/c4dm/event.owl#place)|[Event Ontology](http://purl.org/NET/c4dm/event.owl)|Relates the URI of an event to the URI of the venue in which it took place|
|[product](http://purl.org/NET/c4dm/event.owl#product)|[Event Ontology](http://purl.org/NET/c4dm/event.owl)|Relates the URI of an event to the URI of a sub-event (i.e. work performance), or the URI of a sub-event (work performance) to the URI of the work or activity performed|
|[conductor](http://purl.org/ontology/mo/conductor)|[Music Ontology](http://purl.org/ontology/mo/)|Relates the URI of a performance to the URI of a performer, e.g. a soloist|
|[performer](http://purl.org/ontology/mo/performer)|[Music Ontology](http://purl.org/ontology/mo/)|Relates the URI of a performance to the URI of a conductor|
|[exactMatch](https://www.w3.org/2009/08/skos-reference/skos.html#exactMatch)|[SKOS Simple Knowledge Organization System](https://www.w3.org/2009/08/skos-reference/skos.html)|Relates the URI of an entity or work to the URI of an equivalent entity in another namespace, e.g. dbpedia|
|[label](http://www.w3.org/2000/01/rdf-schema)|[RDF Schema Vocabulary (RDFS)](http://www.w3.org/2000/01/rdf-schema)|Relates the URI of an event, venue, place, non-human entity, or work to a human-readable name (text string)|
|[comment](http://www.w3.org/2000/01/rdf-schema#comment)|[RDF Schema Vocabulary](http://www.w3.org/2000/01/rdf-schema)|Relates the URI of a venue to its description|
|[parentFeature](http://www.geonames.org/ontology#parentFeature)|[GeoNames Ontology](http://www.geonames.org/ontology)|Relates the URI for a venue to the GeoNames URI for Carnegie Hall (the building)|
|[historicalName](http://www.geonames.org/ontology#historicalName)|[GeoNames Ontology](http://www.geonames.org/ontology)|Relates the URI for a venue to a human-readable name (text string) by which it was previously known (e.g. Weill Recital Hall --> Carnegie Recital Hall)|
|[long](http://www.w3.org/2003/01/geo/wgs84_pos#long)|[WGS84 Geo Positioning](http://www.w3.org/2003/01/geo/wgs84_pos)|Relates the URI of a birth place to the longitude coordinate|
|[lat](http://www.w3.org/2003/01/geo/wgs84_pos#lat)|[WGS84 Geo Positioning](http://www.w3.org/2003/01/geo/wgs84_pos)|Relates the URI of a birth place to the latiitude coordinate|
