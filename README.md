# linked-data
# THIS IS A DRAFT! THIS IS A DRAFT! THIS IS A DRAFT! THIS IS A DRAFT! THIS IS A DRAFT! THIS IS A DRAFT! 

## OVERVIEW

The purpose of this repository is to share Carnegie Hall's performance history as linked open data, and resources related to its creation and maintenance. 

You can explore the Carnegie Hall (CH) performance history linked open data [here], and read more about it below.

## CONTENTS

The Carnegie Hall Archives believes in showing its work. To that goal, this repository includes:
- Link to explore the CH LOD via a SPARQL endpoint for querying, with option to download the entire dataset
- [Python scripts](/scripts/scripts-overview.md) used to transform CSV to LOD serializations
- An overview of [CH's performance history]
- Documentation about the [structure and content of the CH LOD]

## CARNEGIE HALL PERFORMANCE HISTORY AS LINKED OPEN DATA
### About the Dataset
The initial release encompasses performance history data from 1891 through the end of the 2015-16 concert season (July 15, 2016). The Carnegie Hall Archives intends to release updated datasets at semi-regular (e.g. 3-6 month) intervals.

#### What Does "Performance History" Mean at CH?

Since it opened in 1891, Carnegie Hall has been a center of cultural and political expression, holds multiple performance spaces, and we present and provide a venue for many different types of music and art. Since its transition to a not-for-profit institution in 1960, Carnegie Hall has continued to deepen its commitment to music education and community outreach and programming with concerts and events in neighborhoods throughout New York City, and the world.

The Carnegie Hall Archives maintains a database, the [Orchestra Planning and Administration System (OPAS)](http://fineartssoftware.com/), with a goal to track every event – musical and nonmusical – that has occurred in the public performance spaces of CH since 1891. Since the CH Archives was not established until 1986, there are some gaps in these records, which we continue to fill in using sources like digitized newspaper listings and reviews, or missing concert programs we buy on eBay or are donated to us. This database now covers **more than 50,000 events across nearly all musical genres, as well as theatrical, dance and spoken word events, meetings, lectures, civic rallies, and political conventions**. Our database has corresponding records for more than 100,000 artists, 20,000 composers and over 85,000 musical works.

Starting in 2013, Carnegie Hall began publishing some of these records to the [Performance History Search](https://www.carnegiehall.org/PerformanceHistorySearch/). You can now find the records for more than 45,000 events from 1891 to the present. Data cleanup efforts are ongoing, and new records are published each month. The Carnegie Hall linked data prototype uses this published data set.

### Potential Future Work

Though the CH LOD includes about 3 million triples, there is still information missing from or out of scope of the initial release. Below is a sample of excluded content and topics. See how to [get involved] if you have feedback about the list of information not currently in the dataset.

- Some past **performance records are missing**; such data will be added as it becomes available. 
- **Complete, accurate biographical data is not always available** for performers and composers. To the extent that this information has been provided to Carnegie Hall or is available from published authority sources, it has been added to the dataset. Existing Carnegie Hall URIs will remain stable, but additional or revised statements (e.g. newly acquired birth/death dates, corrected spellings, etc.) may be added at any time. 
- **Presenting organizations**, e.g. concert management and/or licensees who rented the Hall, are not included in the initial release
- **Credited non-performing roles**, e.g. choral/ensemble preparation, technical roles, etc., are not included in the initial release

### Building LOD at Carnegie Hall

## GET INVOLVED
### Provide Feedback or Report Issues
### Build Something & Share It

## USAGE AND LICENSE
### USAGE GUIDELINES
#### DATA
#### SCRIPTS
This code is provided “as is” and for you to use at your own risk. The information included in the contents of this repository is not necessarily complete. Carnegie Hall offers the scripts as-is and makes no representations or warranties of any kind.

We plan to update the scripts regularly. We welcome any [Issues](https://github.com/CarnegieHall/linked-data/issues) and other feedback. Please let us know if you have found the contents of this repository useful!

### LICENSES
#### DATA LICENSE
**Carnegie Hall is releasing this performance history dataset with a [Creative Commons CC0 1.0 Universal Public Domain data license](https://creativecommons.org/publicdomain/zero/1.0/)**.

The Carnegie Hall Performance History dataset includes data from the [GeoNames geographical database](http://www.geonames.org/), which is licensed under a [Creative Commons Attribution 3.0 License](http://creativecommons.org/licenses/by/3.0/).

#### SCRIPTS LICENSE
_The MIT License (MIT)_

_Copyright (c) 2017 Carnegie Hall_

All contents are released under the terms described in the [MIT License](https://github.com/CarnegieHall/linked-data/blob/master/LICENSE) included in this repository.
