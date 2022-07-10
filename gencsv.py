import json
import os
import csv
import sys


def doone(filename, nameid):
    with open(filename, "r") as infile:
        indata = json.load(infile)
    if "DmcSeriesBundle" in indata["data"]:
        videos = indata["data"]["DmcSeriesBundle"]["episodes"]["videos"]
        if len(videos) == 0:
            return None
        video = videos[0]
        textbundle = indata["data"]["DmcSeriesBundle"]["series"]["text"]
        texttype = "series"
    else:
        video = indata["data"]["DmcVideoBundle"]["video"]
        textbundle = video["text"]
        texttype = "program"
    media_metadata = video["mediaMetadata"]

    def nameTrack(i):
        if i["renditionName"]:
            return i["renditionName"]
        return i["language"] + "-" + i["trackType"]

    tracks_text = "|".join(
        sorted([nameTrack(i) for i in media_metadata["audioTracks"]]))
    subtitles_text = "|".join(
        sorted([
            nameTrack(i) for i in media_metadata["captions"]
            if i["trackType"] != "FORCED"
        ]))
    video_title = textbundle["title"]["full"][texttype]["default"]["content"]
    return [video_title, nameid, tracks_text, subtitles_text]


def doall(foldername):
    rows = []
    for subfolder in ["disneyplus_movies", "disneyplus_series"]:
        for filename in os.listdir(foldername + "/" + subfolder):
            row = doone(foldername + "/" + subfolder + "/" + filename,
                        filename)
            if row is None:
                continue
            rows.append(row)
    return rows


def main():
    rows = doall(sys.argv[1])
    rows.sort(key=lambda a: a[0])
    with open(sys.argv[2], "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "ID", "Audio", "Subtitles"])
        writer.writerows(rows)


if __name__ == "__main__":
    main()
