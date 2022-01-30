import gencsv

rows = gencsv.doall("disneyplus_20220130")
counts = {}
for i in rows:
    subtitles = i[3].split("|")
    for s in subtitles:
        if not s.endswith("[CC]"):
            continue
        oldcount = counts[s] if s in counts else 0
        counts[s] = oldcount + 1
for i in sorted(counts.keys()):
    print(i + ":", counts[i])
