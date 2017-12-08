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
### People from CH performance history that received Grammy Award
```
#People from CH performance history that received Grammy Award
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
#added before 2016-10
# Coordinates of the birth places of people named Antoine
#defaultView:Map
SELECT ?item ?itemLabel ?coord WHERE {
  ?item wdt:P735 wd:Q11122389.
  ?item wdt:P19 ?place.
  ?item wdt:P4104 ?chAgent_id.
  ?place wdt:P625 ?coord.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "fr". }
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
	?personID wdt:P509 ?causeID .
    ?personID wdt:P4104 ?chAgent_id.
	OPTIONAL {
		?personID rdfs:label ?personName filter (lang(?personName) = "en") .
	}
	OPTIONAL {
		?causeID rdfs:label ?causeLabel filter (lang(?causeLabel) = "en").
	}
}
```
### List of actors who have appeared at CH with pictures with year of birth and/or death
```
#List of actors who have appeared at CH with pictures with year of birth and/or death
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
