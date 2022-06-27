#!/bin/bash
# usage: ./runscrape.sh scrapedir
set -e
langs="en-US fr-CA fr-FR de-DE nl-NL es-CL"
basedir="$PWD"

function cleanit() {
	bigfiles="$(grep -e "992d453ab2832f6b25f02c5856f27541" -e "26f92b06ea07e32d487c58faa81de51a" $1|cut -d " " -f 3)"
	for i in $bigfiles
	do
        	rm $i
	done
}

mkdir "$1"
cd "$1"

wget https://cde-lumiere-disneyplus.bamgrid.com/d-sitemap-1.xml
wget https://cde-lumiere-disneyplus.bamgrid.com/d-sitemap-2.xml

for langname in $langs
do
	mkdir "$langname"
	cd "$langname"
	python3 "$basedir/pullit.py" "$langname" allurls.txt allurls_series.txt ../*.xml
	mkdir disneyplus_movies
	mkdir disneyplus_series
	cd disneyplus_movies
	wget -i ../allurls.txt
	md5sum * >../md5_movies.txt
	cleanit ../md5_movies.txt
	cd ../disneyplus_series
	wget -i ../allurls_series.txt
	md5sum * >../md5_series.txt
	cleanit ../md5_series.txt
	cd ../../
done
