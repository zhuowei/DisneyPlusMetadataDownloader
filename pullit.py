#!/usr/bin/env python3
import sys
import re

lang = sys.argv[1]

# usage: ./pullit.py en-US allurls.txt allurls_series.txt d-sitemap-1.xml d-sitemap-2.xml
moviesregex = re.compile(
    r"https://www\.disneyplus\.com/(\w*-\w*/)?movies/[^<]*")
seriesregex = re.compile(
    r"https://www\.disneyplus\.com/(\w*-\w*/)?series/[^<]*")

language_name, region_name = lang.split("-")
moviejsonbase = "https://disney.content.edge.bamgrid.com/svc/content/DmcVideoBundle/version/5.1/region/" + region_name + "/audience/false/maturity/1450/language/" + language_name + "/encodedFamilyId/"
seriesjsonbase = "https://disney.content.edge.bamgrid.com/svc/content/DmcSeriesBundle/version/5.1/region/" + region_name + "/audience/false/maturity/1450/language/" + language_name + "/encodedSeriesId/"

urls_movies = []
ids_movies = set()
urls_series = []
ids_series = set()
for filename in sys.argv[4:]:
    with open(filename, "r") as infile:
        indata = infile.read()
    for m in moviesregex.finditer(indata):
        url = m.group(0)
        id = url[url.rfind("/") + 1:]
        if id in ids_movies:
            continue
        ids_movies.add(id)
        urls_movies.append(moviejsonbase + id)
    for m in seriesregex.finditer(indata):
        url = m.group(0)
        id = url[url.rfind("/") + 1:]
        if id in ids_series:
            continue
        ids_series.add(id)
        urls_series.append(seriesjsonbase + id)
with open(sys.argv[2], "w") as outfile:
    outfile.write("\n".join(urls_movies))
with open(sys.argv[3], "w") as outfile:
    outfile.write("\n".join(urls_series))
