# Sample Wikidata SPARQL Queries for CH LOD

## Using the sample queries

Go to [Wikidata Query Service](https://query.wikidata.org). Copy one of the sample queries below into the query window (right panel). Then hit the blue arrow on the left to run it. The results will be in the bottom half of the screen.

## Sample queries

### Timeline of compositions by composers in CH performance history data
```
#Timeline of compositions by composers in CH performance history data
#defaultView:Timeline
SELECT DISTINCT  ?item ?itemLabel ?composerLabel ?catalog_code ?publication_data
WHERE
{
	?composer wdt:P4104 ?chAgent_id.
    	?item wdt:P86 ?composer ;
          wdt:P528 ?catalog_code ;
          wdt:P577 ?publication_data .

	SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
```
### Viennese composers and their compositions by tonality
```
#Viennese composers and their compositions by tonality
#Can change place of birth/death/residence in query builder (Vienna is wd:Q1741)
#defaultView:Tree
SELECT ?composer ?composerLabel ?composerImage ?tonality ?tonalityLabel ?composition ?compositionLabel WHERE {
  ?composer wdt:P31 wd:Q5.
  ?composer wdt:P4104 ?chAgent_id.
  ?composer (wdt:P19|wdt:P20|wdt:P551) wd:Q1741.
  OPTIONAL { ?composer wdt:P18 ?composerImage. }
  ?composition wdt:P86 ?composer.
  ?composition wdt:P826 ?tonality.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],de-at,de". }
}
ORDER BY ?composerLabel ?tonalityLabel
```
### People from CH performance history that received a Grammy Award
```
#People from CH performance history that received Grammy Award
#defaultView:ImageGrid
SELECT DISTINCT ?person ?personLabel ?personImage WHERE {
  ?person (wdt:P166/wdt:P279*) wd:Q41254 ;
                               wdt:P4104 ?chAgent_id .
  OPTIONAL { ?person wdt:P18 ?personImage. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```
### Birthplaces of people named Johann (or replace this name with whatever you want!)
```
#Birthplaces of people named Johann
#Can change name in query builder (change object valeu of wdt:P735 - wd:Q11122389 is Johann)
#Map marker displays birthplace label, coordinates, person's name (and image if available)
#defaultView:Map
SELECT ?person ?personLabel ?placeLabel ?coord ?coordLabel ?personImage WHERE {
  ?person wdt:P735 wd:Q11122389.
  ?person wdt:P19 ?place.
  ?person wdt:P4104 ?chAgent_id.
  ?place wdt:P625 ?coord.
  OPTIONAL { ?person wdt:P18 ?personImage. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```
### Things/people in CH performance history with most children
```
#Things/people in CH performance history with most children
#added before 2016-10
SELECT ?parent ?parentLabel ?count
WHERE
{
  {
    SELECT ?parent (COUNT(?child) AS ?count)
    WHERE
    {
      ?parent wdt:P40 ?child.
      ?parent wdt:P4104 ?chAgent_id.
    }
    GROUP BY ?parent
    ORDER BY DESC(?count)
    LIMIT 10
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY DESC(?count)
LIMIT 10
```
### People in CH performance history Awarded Nobel Peace Prize
```
#People in CH performance history Awarded Nobel Peace Prize
#Can change award in query builder by changing object value of ?awardStat ps:P166 wd:Q35637.
#defaultView:Timeline
SELECT DISTINCT ?item ?itemLabel ?when (YEAR(?when) AS ?date) ?pic WHERE {
  ?item wdt:P4104 ?chAgent_id.
  ?item p:P166 ?awardStat.
  ?awardStat ps:P166 wd:Q35637.
  ?awardStat pq:P585 ?when.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
  OPTIONAL { ?item wdt:P18 ?pic. }
}
```
### Number of people in CH performance history per gender
```
#Number of people in CH performance history per gender
#Does not show gender label
#added before 2016-10
SELECT ?gender (count(distinct ?human) as ?number)
WHERE
{
	?human wdt:P31 wd:Q5
	; wdt:P21 ?gender
	; wdt:P4104 ?chAgent_id .
}
GROUP BY ?gender
LIMIT 10

```
### US presidents who have appeared at CH and spouses
```
#US presidents who have appeared at CH and spouses
#added before 2016-10
#TEMPLATE={"template":"Presidents of ?country and their spouses","variables":{"?country":{"query":" SELECT ?id WHERE { ?id wdt:P31 wd:Q6256 . }"} } }
#defaultView:ImageGrid
SELECT ?president ?presidentName ?presidentPicture ?spouse ?spouseName ?spousePicture WHERE {
  BIND(wd:Q30 AS ?country)
  ?country (p:P6/ps:P6) ?president.
  ?president wdt:P26 ?spouse;
     wdt:P4104 ?chAgent_id.
  OPTIONAL {
    ?president wdt:P18 ?presidentPicture.
    ?spouse wdt:P18 ?spousePicture.
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```
### Politicians that appeared at CH who died of cancer (of any type)
```
#Politicians that appeared at CH who died of cancer (of any type)
#added before 2016-10
SELECT ?politician ?cause ?politician_label ?cause_of_death_label
WHERE
{
	?politician wdt:P106 wd:Q82955 ;    # find items that have "occupation (P106): politician (Q82955)"
                wdt:P4104 ?chAgent_id.
	?politician wdt:P509 ?cause .       # with a P509 (cause of death) claim
	?cause wdt:P279* wd:Q12078 .        # ... where the cause is a subclass of (P279*) cancer (Q12078)
	# ?politician wdt:P39 wd:Q11696 .   # Uncomment this line to include only U.S. Presidents

	OPTIONAL {?politician rdfs:label ?politician_label filter (lang(?politician_label) = "en") .}
	OPTIONAL {?cause rdfs:label ?cause_of_death_label filter (lang(?cause_of_death_label) = "en").}
}
ORDER BY ASC (?politician)
```
### List of presidents who have appeared at CH with causes of death
```
#List of presidents who have appeared at CH with causes of death
#added before 2016-10
SELECT ?presidentID ?causeID ?presidentName ?causeLabel
WHERE
{
	?presidentID wdt:P39 wd:Q11696 .
	?presidentID wdt:P509 ?causeID .
    ?presidentID wdt:P4104 ?chAgent_id.
	OPTIONAL {
		?presidentID rdfs:label ?presidentName filter (lang(?presidentName) = "en") .
	}
	OPTIONAL {
		?causeID rdfs:label ?causeLabel filter (lang(?causeLabel) = "en").
	}
}
```

### List of people who have appeared at CH with causes of death
```
#List of people who have appeared at CH with causes of death
#added before 2016-10
SELECT ?personID ?causeID ?personName ?causeLabel
WHERE
{
	?personID wdt:P509 ?causeID ;
		  wdt:P4104 ?chAgent_id.
	OPTIONAL {
		?personID rdfs:label ?personName filter (lang(?personName) = "en") .
	}
	OPTIONAL {
		?causeID rdfs:label ?causeLabel filter (lang(?causeLabel) = "en").
	}
}
ORDER BY ASC (?causeLabel)
```
### List of actors who have appeared at CH with pictures with year of birth and/or death
```
#List of actors who have appeared at CH with pictures with year of birth and/or death
#Change object value wd:Q33999 in Query Helper to search other roles, e.g. conductor
#added before 2016-10
#defaultView:ImageGrid
SELECT ?human ?humanLabel ?yob ?yod ?picture
WHERE
{
	?human wdt:P31 wd:Q5;
           wdt:P106 wd:Q33999 ;
           wdt:P4104 ?chAgent_id .
	?human wdt:P18 ?picture .
	OPTIONAL { ?human wdt:P569 ?dob . ?human wdt:P570 ?dod }.
	BIND(YEAR(?dob) as ?yob) . #if available: year
	BIND(YEAR(?dod) as ?yod) .
	SERVICE wikibase:label {
		bd:serviceParam wikibase:language "en" .
	}
}
LIMIT 88
```
### Authors, writers and poets ranked by sitelink and also includes "country of citizenship"
* This works, but it is slow and maybe needs refinement.
```
#Authors, writers and poets ranked by sitelink and also includes "country of citizenship"
#added before 2016-10
SELECT distinct ?writer ?place ?linkcount
WHERE
{
  {?s wdt:P106 wd:Q36180 ; wdt:P4104 ?chAgent_id .} UNION { ?s wdt:P106 wd:Q482980 . } UNION { ?s wdt:P106 wd:Q49757 . }
  ?s wdt:P27 ?pl .
  ?s wikibase:sitelinks ?linkcount .
  OPTIONAL {
     ?s rdfs:label ?writer filter (lang(?writer) = "en").
   }
    OPTIONAL {
     ?pl rdfs:label ?place filter (lang(?place) = "en").
   }
} GROUP BY ?place ?writer ?linkcount HAVING (?linkcount > 10) ORDER BY DESC(?linkcount)
```
### Map of birthplaces of pianists with a CH Agent ID, with image (filter city by population)
```
#defaultView:Map
#view:Map{"hide": ["?location", "?population", "?layer"]}
SELECT ?person ?personLabel ?personImage ?birthDate ?deathDate ?city ?cityLabel 
(SAMPLE(?location) AS ?location) (MAX(?population) AS ?population) (SAMPLE(?layer) AS ?layer)
(IRI(CONCAT("https://www.carnegiehall.org/About/History/Performance-History-Search?q=&dex=prod_PHS&pf=", 
              (STR(ENCODE_FOR_URI(?personLabel))))) AS ?phsLink)
WHERE {
  ?person wdt:P31 wd:Q5;
          wdt:P19 ?city;
          wdt:P4104 ?chAgent_id;
          wdt:P106 wd:Q486748 .
  ?city wdt:P625 ?location;
        wdt:P1082 ?population .
  FILTER (xsd:integer(?chAgent_id) < 1000000).
  OPTIONAL { ?person wdt:P18 ?personImage }
  OPTIONAL { ?person wdt:P569 ?birthDate }
  OPTIONAL { ?person wdt:P570 ?deathDate }
  BIND(
    IF(?population < 10000, "Pop. 1k-10k",
    IF(?population < 50000, "Pop. 10k-50k",
    IF(?population < 100000, "Pop. 50k-100k",
    IF(?population < 500000, "Pop. 100k-500k", 
    IF(?population < 1000000, "Pop. 500k-1M",
    IF(?population < 10000000, "Pop. 1M-10M",
    IF(?population < 50000000, "Pop. 50M-100M",
    "Pop. >100M")))))))
    AS ?layer).

  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
GROUP BY ?person ?personLabel ?personImage ?phsLink ?birthDate ?deathDate ?city ?cityLabel
```
### Map of birthplaces of pianists with a CH Agent ID, with image (filter by sign of the Zodiac)
```
#defaultView:Map
#view:Map{"hide": "?location"}
SELECT ?personLabel ?personImage ?birthDate ?deathDate ?city ?cityLabel ?location
(SAMPLE(?layer) AS ?layer)
(IRI(CONCAT("https://www.carnegiehall.org/About/History/Performance-History-Search?q=&dex=prod_PHS&pf=", 
              (STR(ENCODE_FOR_URI(?personLabel))))) AS ?phsLink)
WHERE {
  ?person wdt:P31 wd:Q5;
          wdt:P19 ?city;
          wdt:P4104 ?chAgent_id;
          wdt:P569 ?birthDate;
          wdt:P106 wd:Q486748 .
  ?city wdt:P625 ?location.
  FILTER (xsd:integer(?chAgent_id) < 1000000).
  OPTIONAL { ?person wdt:P18 ?personImage }
  OPTIONAL { ?person wdt:P570 ?deathDate }
  BIND(
    IF(month(?birthDate) = 1 && day(?birthDate) > 19, "Aquarius",
    IF(month(?birthDate) = 1 && day(?birthDate) < 20, "Capricorn",
    IF(month(?birthDate) = 2 && day(?birthDate) > 18, "Pisces",
    IF(month(?birthDate) = 2 && day(?birthDate) < 19, "Aquarius",
    IF(month(?birthDate) = 3 && day(?birthDate) > 20, "Aries",
    IF(month(?birthDate) = 3 && day(?birthDate) < 21, "Pisces",
    IF(month(?birthDate) = 4 && day(?birthDate) > 19, "Taurus",
    IF(month(?birthDate) = 4 && day(?birthDate) < 20, "Aries",
    IF(month(?birthDate) = 5 && day(?birthDate) > 20, "Gemini",
    IF(month(?birthDate) = 5 && day(?birthDate) < 21, "Taurus",
    IF(month(?birthDate) = 6 && day(?birthDate) > 20, "Cancer",
    IF(month(?birthDate) = 6 && day(?birthDate) < 21, "Gemini",
    IF(month(?birthDate) = 7 && day(?birthDate) > 22, "Leo",
    IF(month(?birthDate) = 7 && day(?birthDate) < 23, "Cancer",
    IF(month(?birthDate) = 8 && day(?birthDate) > 22, "Virgo",
    IF(month(?birthDate) = 8 && day(?birthDate) < 23, "Leo",
    IF(month(?birthDate) = 9 && day(?birthDate) > 22, "Libra",
    IF(month(?birthDate) = 9 && day(?birthDate) < 23, "Virgo",
    IF(month(?birthDate) = 10 && day(?birthDate) > 22, "Scorpio",
    IF(month(?birthDate) = 10 && day(?birthDate) < 23, "Libra",
    IF(month(?birthDate) = 11 && day(?birthDate) > 21, "Sagittarius",
    IF(month(?birthDate) = 11 && day(?birthDate) < 22, "Scorpio",
    IF(month(?birthDate) = 12 && day(?birthDate) > 21, "Capricorn",
       "Saggitarius")))))))))))))))))))))))
    AS ?layer).

  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
GROUP BY ?personLabel ?personImage ?phsLink ?birthDate ?deathDate ?city ?cityLabel ?location
```
### Find Wikidata items with CH Agent ID
```
#Find Wikidata items with CH Agent ID
SELECT ?item ?chURL
WHERE 
{
  wd:P4104 wdt:P1630 ?formatterurl.
    ?item wdt:P4104 ?chAgentID .
  BIND(IRI(REPLACE(?chAgentID, '^(.+)$', ?formatterurl)) AS ?chURL).

}
```
### Find Wikidata items with CH Work ID
```
#Find Wikidata items with CH Work ID
#Excludes items that are instance of "single" (Q134556)
SELECT DISTINCT ?item ?chURL
WHERE 
{
  wd:P5229 wdt:P1630 ?formatterurl.
    ?item wdt:P5229 ?chWorkID ;
          (wdt:P31/wdt:P279*) wd:Q2188189 .

  OPTIONAL{wd:P5229 wdt:P1630 ?formatterurl.
           ?item wdt:P5229 ?chWorkID ;
                 (wdt:P31/wdt:P279*) wd:Q7725634 .}
  BIND(IRI(REPLACE(?chWorkID, '^(.+)$', ?formatterurl)) AS ?chURL).
}
```
### Find CH premieres of any type associated with a conductor (no limit)
```
PREFIX chnames: http://data.carnegiehall.org/names/
PREFIX dcterms: http://purl.org/dc/terms/
PREFIX rdfs: http://www.w3.org/2000/01/rdf-schema#
PREFIX event: http://purl.org/NET/c4dm/event.owl#
select ?work ?workTitle ?comment ?event ?eventTitle ?eventDate where { 
   ?work dcterms:creator chnames:1002833 ;
         rdfs:label ?workTitle .
   ?event event:product ?workPerformance ;
          rdfs:label ?eventTitle ;
          dcterms:date ?eventDate .
   ?workPerformance event:product ?work;
                    rdfs:comment ?comment .
   filter contains(?comment, "premiere")
} 
```
