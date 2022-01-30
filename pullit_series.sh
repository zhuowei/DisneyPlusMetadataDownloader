#!/bin/sh
allvideos="$(grep -h -o -E "https://www\.disneyplus\.com/series/[^<]*" d-sitemap-1.xml d-sitemap-2.xml)"
for i in $allvideos
do
   part="$(basename "$i")"
   echo "https://disney.content.edge.bamgrid.com/svc/content/DmcSeriesBundle/version/5.1/region/US/audience/false/maturity/1450/language/en/encodedSeriesId/$part"
done
