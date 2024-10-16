# Carnegie Hall Linked Open Data - Classes

## OVERVIEW

Below are classes used in the Carnegie Hall (CH) data set. The table also includes a brief usage note per class and the vocabulary from which the class is sourced. 

## CLASSES USED
|Class|CH Usage|Vocabulary|
|:----|:---|:----------|
|[Event](http://schema.org/Event)|Used in CH dataset to classify Events|[Schema.org](http://schema.org/)|
|[workPerformance](http://data.carnegiehall.org/model/WorkPerformance)|Used in CH dataset to classify work performances, i.e., sub-events|[data.carnegiehall.org](http://data.carnegiehall.org/)|
|[MusicComposition](http://schema.org/MusicComposition)|Used in CH dataset to classify musical works; a sub-class of CreativeWork|[Schema.org](http://schema.org/)|
|[CreativeWork](http://schema.org/CreativeWork)|Used in CH dataset to classify non-musical creative works, e.g. plays|[Schema.org](http://schema.org/)|
|[Person](https://schema.org/Person)|Used in CH dataset to classify people|[Schema.org](http://schema.org/)|
|[Entity](http://data.carnegiehall.org/model/Entity)|The base type of all people, organizations, or animals taking part in Carnegie Hall events or serving creative roles in works performed|[data.carnegiehall.org](http://data.carnegiehall.org/)|
|[PerformingGroup](http://schema.org/PerformingGroup)|Use in CH dataset to classify performing ensembles|[Schema.org](http://schema.org/)|
|[Organization](http://schema.org/Organization)|An organization such as a school, NGO, corporation, club, etc., added when entity can be reasonably assumed to be an organization based on information available|[Schema.org](http://schema.org/)|
|[Instrument](http://purl.org/ontology/mo/Instrument)|Used in CH dataset to classify musical instruments|[Music Ontology](http://purl.org/ontology/mo/)|
|[Role](http://schema.org/Role) |Use in CH dataset to classify roles, e.g. actor, conductor, magician, etc.|[Schema.org](http://schema.org/)|
|[EventVenue](http://schema.org/EventVenue)|Used in CH dataset to classify the Carnegie Hall building, as well as each constituent venue|[Schema.org](http://schema.org/)|
|[LandmarksOrHistoricalBuildings](http://schema.org/LandmarksOrHistoricalBuildings)|Used in CH dataset to classify the Carnegie Hall building|[Schema.org](http://schema.org/)|
|[Place](http://schema.org/Place)|Entities that have a somewhat fixed, physical extension; in the context of the CH model, currently used to represent birthplaces of Entities and provide a node type suitable for attaching geocoding information|[Schema.org](http://schema.org/)|

----------------------------
Go to: [DATA STRUCTURE](/data-structure.md) | [README](/README.md) | [SPARQL ENDPOINT](http://data.carnegiehall.org/sparql/)
