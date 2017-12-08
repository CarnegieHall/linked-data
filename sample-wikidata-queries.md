#Timeline of compositions by composers in CH performance history data
#defaultView:Timeline
SELECT DISTINCT  ?item ?itemLabel ?composerLabel ?catalog_code ?publication_data
WHERE
{
	?composer wdt:P4104 ?chAgent_id.
  ?item wdt:P86 ?composer ;
          wdt:P528 ?catolog_code ;
          wdt:P577 ?publication_data .

	SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
