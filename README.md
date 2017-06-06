# linked-data

## OVERVIEW
Carnegie Hall Archives maintains a series of scripts to transform its historical performance history data from its source in a SQL database into the Resource Description Framework (RDF) for publication as linked open data.

These scripts have benefitted immensely from a wide community of archiving, preservation, and programming experts who share their code and troubleshooting techniques online. We are excited by the opportunity to participate in this community and have our methods improve through open collaboration and mutual exchange.

### PERFORMANCE HISTORY DATABASE: OPAS
The Carnegie Hall Archives maintains a database, the [Orchestra Planning and Administration System (OPAS)](http://fineartssoftware.com/), with a goal to track every event – musical and nonmusical – that has occurred in the public performance spaces of Carnegie Hall since 1891. (Since the CH Archives was not established until 1986, there are some gaps in these records, which we continue to fill in using sources like digitized newspaper listings and reviews, or missing concert programs we buy on eBay.) This database now covers more than 50,000 events across nearly all musical genres, as well as dance and spoken word performances, meetings, lectures, civic rallies, and political conventions. Our database has corresponding records for more than 100,000 artists, 20,000 composers and over 85,000 musical works. Starting in 2013, Carnegie Hall began publishing some of these records to the [Performance History Search](http://www.carnegiehall.org/PerformanceHistorySearch/) on its website, where you can now find the records for more than 45,000 events from 1891 to the present.  Data cleanup efforts are ongoing, and new records are published each month.  The Carnegie Hall linked data prototype uses this published data set.

## CONTENTS

| Script Name         | Purpose           |
| ------------- |-------------|
| **[OPAS_toRDF_entities.py](https://github.com/CarnegieHall/linked-data/blob/master/OPAS_toRDF_entities.py)**     | Transforms OPAS data (Entities, i.e. performers, composers, etc.) from SQL into RDF data model |
|**[OPAS_toRDF_works.py](https://github.com/CarnegieHall/linked-data/blob/master/OPAS_toRDF_events.py)**      | Transforms OPAS data (Creative works, i.e. musical compositions, dramatic works, etc.) from SQL into RDF data model |
|**[OPAS_toRDF_events.py](https://github.com/CarnegieHall/linked-data/blob/master/OPAS_toRDF_works.py)** | Transforms OPAS data (Events, i.e. performances, lectures, etc.) from SQL into RDF data model |


## USAGE AND LICENSE
### USAGE GUIDELINES
This code is provided “as is” and for you to use at your own risk. The information included in the contents of this repository is not necessarily complete. Carnegie Hall offers the scripts as-is and makes no representations or warranties of any kind.

We plan to update the scripts regularly. We welcome any [Issues](https://github.com/CarnegieHall/linked-data/issues) and other feedback. Please let us know if you have found the contents of this repository useful!

### LICENSE
_The MIT License (MIT)_

_Copyright (c) 2016 Carnegie Hall_

All contents are released under the terms described in the [MIT License](https://github.com/CarnegieHall/linked-data/blob/master/LICENSE) included in this repository.
