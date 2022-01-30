#bigfiles="$(grep "26f92b06ea07e32d487c58faa81de51a" /tmp/dp_md5|cut -d " " -f 3)"
bigfiles="$(grep "992d453ab2832f6b25f02c5856f27541" /tmp/dp_md5_series|cut -d " " -f 3)"
for i in $bigfiles
do
	rm $i
done
