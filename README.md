# linked-data

## OVERVIEW

The purpose of this repository is to share Carnegie Hall's performance history as linked open data, and resources related to its creation and maintenance. 

🔴 Explore Carnegie Hall's linked open data [here](http://data.carnegiehall.org), and read more about it below.

## CONTENTS

The Carnegie Hall Archives believes in showing its work. To that goal, this repository includes:
- [Link](http://data.carnegiehall.org) to explore the CH LOD via a SPARQL endpoint for querying
- [Python scripts](/scripts/scripts-overview.md) used to transform CSV to LOD serializations
- An overview of [Carnegie Hall's performance history](#carnegie-hall-performance-history-as-linked-open-data)
- Documentation about the [structure and content of the Carnegie Hall linked open data](/data-structure.md)

## CARNEGIE HALL PERFORMANCE HISTORY AS LINKED OPEN DATA

### About the Data Set
The initial release encompasses performance history data from 1891 through the end of the 2015-16 concert season (July 15, 2016). The Carnegie Hall Archives intends to release updated data sets at semi-regular (e.g. 3-6 month) intervals.

#### What Does "Performance History" Mean at CH?

Since it opened in 1891, Carnegie Hall has been a center of cultural and political expression, presenting and providing a venue for many different types of music and culture across multiple performance spaces. Since its transition to a not-for-profit institution in 1960, Carnegie Hall has continued to deepen its commitment to music education and community outreach by presenting concerts and events in neighborhoods throughout New York City, across the United States, and worldwide.

The Carnegie Hall Archives maintains a database, the [Orchestra Planning and Administration System (OPAS)](http://fineartssoftware.com/), with a goal to track every event – musical and nonmusical – that has occurred in the public performance spaces of CH since 1891. Since our archives were not established until 1986, there are some gaps in these records, which we continue to fill using sources like digitized newspaper listings and reviews; many missing pieces – concert programs, posters, etc. – are donated to us, or we buy them on eBay. This database now covers **more than 50,000 events across nearly all musical genres, as well as theatrical, dance and spoken word events, meetings, lectures, civic rallies, and political conventions**. It also includes corresponding records for more than 100,000 artists, 20,000 composers and over 85,000 musical works.

Starting in 2013, Carnegie Hall began publishing some of these records to our online [Performance History Search](https://www.carnegiehall.org/PerformanceHistorySearch/). The Performance History Search has records for more than 45,000 events from 1891 to the present. Data cleanup efforts are ongoing, and new records are published each month to that HMTL presentation. The Carnegie Hall linked data prototype uses this published data set.

#### Data Structure

How is the Carnegie Hall (CH) performance history represented as linked open data? Characteristics about CH performance events fall into two categories:
1. **Information that applies to the entire event**.
2. **Information that applies to each presentation of a work** during an event (a *work performance*). 

The separation of a work performance from the event enables us to provide specificity. Statements link performers to a particular work performance, rather than generically to an entire event. Let's explore the event data structure further: 

1. Each event has its own Uniform Resource Indentifier (URI) and includes metadata related to: 
      - *Date/Time* (ISO 8601 date/time string) 
      - *Venue* 
      - *Title* (who performed or what took place) 
      - *Entities who participate in the entirety of the program*, like a conductor and/or an orchestra.

2. Components of an event, e.g. each work performed, is a sub-event with its own URI. Work performance metadata includes:
      - *Works* (musical and non-musical)
      - *Performers* 

Interested in the **CH LOD data model, namespaces, URI schemas, vocabularies, and ontologies**? Check out CH's in-depth [data structure and schema documentation](/data-structure.md) in this repository.

### Potential Future Work

Although the CH LOD includes about 3 million triples, there is still information missing from or out of scope of this initial release. Below is a sample of excluded content and topics. See how to [get involved](#get-involved) if you have feedback about the list of information not currently in the dataset.

- Some past **performance records are missing**; such data will be added as it becomes available. 
- **Complete, accurate biographical data is not always available** for performers and composers. To the extent that this information has been provided to Carnegie Hall or is available from published authority sources, it has been added to the dataset. Existing Carnegie Hall URIs will remain stable, but additional or revised statements (e.g. newly acquired birth/death dates, corrected spellings, etc.) may be added at any time.
- **Additional external authority IDs** - we plan to add more external authority IDs for entities and creative works, and to expand the scope to include Wikidata IDs
- **Presenting organizations**, e.g. concert management and/or licensees who rented the Hall, are not included in the initial release
- **Roles and instruments on a specific Work Performance** for an entity. We are working on a way to describe which instrument/role a certain artist played an during a work performance.
- **Credited non-performing roles**, e.g. choral/ensemble preparation, technical roles, etc., are not included in the initial release
- **Building LOD at Carnegie Hall** - How did the Carnegie Hall Archives get from an internal database to 3 million triples containing open data from a dozen ontologies and vocabularies? 

## GET INVOLVED
### Provide Feedback or Report Issues

Want to help Carnegie Hall improve the performance history data? Use the [Issues](https://github.com/CarnegieHall/linked-data/issues) page to share:
- **Feedback** - What was useful about the data or the resources in this repository? 
- **Recommendations** - Have a great idea for the content, structure, or resources we describe you'd like to share with us?
- **Sample Queries** - Did you write an interesting SPARQL query others might find useful? 
- **Issues or Inaccuracies** - Notice something out of place or incorrect? 

### Build Something & Share It

Did you use the CH LOD to build an interesting visualization, or port it into a new project? We'd love to see it! [Submit](https://github.com/CarnegieHall/linked-data/issues) a link and a description of how you utilized the data set.

## USAGE AND LICENSE
### USAGE GUIDELINES
#### DATA
Carnegie Hall offers the CH Performance History as Linked Open Data dataset as-is and makes no representations or warranties of any kind concerning the contents. Please see the data license statement below.

If you have questions about the dataset or its usage, please submit a new ['Issue'](https://github.com/CarnegieHall/linked-data/issues) or email *archives at carnegiehall dot org*. 

#### SCRIPTS
This code is provided “as is” and for you to use at your own risk. The information included in the contents of this repository is not necessarily complete. Carnegie Hall offers the scripts as-is and makes no representations or warranties of any kind.

We plan to update the scripts regularly. We welcome any [feedback](https://github.com/CarnegieHall/linked-data/issues). Please let us know if you have found the contents of this repository useful!

### LICENSES
#### DATA LICENSE
**Carnegie Hall is releasing this performance history dataset with a [Creative Commons CC0 1.0 Universal Public Domain data license](https://creativecommons.org/publicdomain/zero/1.0/)**.

The Carnegie Hall Performance History dataset includes data from the [GeoNames geographical database](http://www.geonames.org/), which is licensed under a [Creative Commons Attribution 3.0 License](http://creativecommons.org/licenses/by/3.0/).

#### REPOSTIORY AND SCRIPTS LICENSE
_The MIT License (MIT)_

_Copyright (c) 2017 Carnegie Hall_

All contents are released under the terms described in the [MIT License](https://github.com/CarnegieHall/linked-data/blob/master/LICENSE) included in this repository.

## ACKNOWLEDGEMENTS 
Thank you to [Matt Miller](https://github.com/thisismattmiller) for his contributions to this project. 

Thank you to the following organizations for inspiration and commitment to the open data community:
- [Linked Jazz](https://linkedjazz.org/)
- [New York Philharmonic Archives](https://github.com/nyphilarchive/PerformanceHistory)
- [The Museum of Modern Art (MoMA)](https://github.com/MuseumofModernArt/collection)
