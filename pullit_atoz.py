import requests
import sys

if len(sys.argv) != 4:
    print("usage: ./pullit.py en-US allurls.txt allurls_series.txt")
    exit(0)

# for series, pulling from the A-Z collection works better than pulling from sitemap - we pull ~460 instead of ~300
# for movies, pulling from A-Z + Shorts collections seems to mostly match sitemap:
# we miss out on unreleased movies that are in the sitemap but only has a trailer, but you can't watch those anyways...

lang = sys.argv[1]

language_name, region_name = lang.split("-")
moviejsonbase = "https://disney.content.edge.bamgrid.com/svc/content/DmcVideoBundle/version/5.1/region/" + region_name + "/audience/false/maturity/1830/language/" + language_name + "/encodedFamilyId/"
seriesjsonbase = "https://disney.content.edge.bamgrid.com/svc/content/DmcSeriesBundle/version/5.1/region/" + region_name + "/audience/false/maturity/1830/language/" + language_name + "/encodedSeriesId/"

# A-Z
base_movies_collection = "https://disney.content.edge.bamgrid.com/svc/content/CuratedSet/version/5.1/region/{}/audience/k-false,l-true/maturity/1830/language/{}/setId/9f7c38e5-41c3-47b4-b99e-b5b3d2eb95d4/pageSize/30/page/"
# Shorts
base_shorts_collection = "https://disney.content.edge.bamgrid.com/svc/content/CuratedSet/version/5.1/region/{}/audience/k-false,l-true/maturity/1830/language/{}/setId/34c856af-325c-4603-8d6b-dd9dc4695a69/pageSize/30/page/"
base_series_collection = "https://disney.content.edge.bamgrid.com/svc/content/CuratedSet/version/5.1/region/{}/audience/k-false,l-true/maturity/1830/language/{}/setId/53adf843-491b-40ae-9b46-bccbceed863b/pageSize/30/page/"


def graballpages(base_url):
    page = 1
    retval = []
    while True:
        page_url = base_url + str(page)
        print(page_url)
        resp = requests.get(page_url)
        j = resp.json()
        if len(j["data"]["CuratedSet"]["items"]) == 0:
            break
        retval.append(j)
        page += 1
    return retval


def grabone(base_url, output_base_url):
    allpages = graballpages(base_url)
    allout = []
    for page in allpages:
        for item in page["data"]["CuratedSet"]["items"]:
            if "encodedSeriesId" in output_base_url:
                itemid = item["encodedSeriesId"]
            else:
                itemid = item["family"]["encodedFamilyId"]
            allout.append(output_base_url + itemid)
    return allout


urls_movies = grabone(
    base_movies_collection.format(region_name, language_name), moviejsonbase)
urls_movies += grabone(
    base_shorts_collection.format(region_name, language_name), moviejsonbase)
urls_series = grabone(
    base_series_collection.format(region_name, language_name), seriesjsonbase)
with open(sys.argv[2], "w") as outfile:
    outfile.write("\n".join(urls_movies))
with open(sys.argv[3], "w") as outfile:
    outfile.write("\n".join(urls_series))
