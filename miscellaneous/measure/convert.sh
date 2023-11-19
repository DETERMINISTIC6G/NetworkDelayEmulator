echo "QIDSC:"
read qdisc
echo "Dist:"
read dist
echo "Bandwidth:"
read bandwidth

echo DIST: $dist
echo Bandwidth: $bandwidth
echo QDISC: $qdisc

read -p "Contiue? y/N " yn
case $yn in
    [Yy]* ) echo OK;;
    [Nn]* ) exit 0;;
    * ) exit 1;;
esac

FILE1="$dist-$bandwidth-$qdisc-1"
FILE2="$dist-$bandwidth-$qdisc-2"

mv cap1.cap $FILE1.cap
mv cap2.cap $FILE2.cap

echo "Starting tshark conversion"

tshark -r $FILE1.cap -t a -T fields -E separator=, -e frame.number -e frame.time_epoch -e ip.src -e ip.dst -e data > $FILE1.data &
tshark -r $FILE2.cap -t a -T fields -E separator=, -e frame.number -e frame.time_epoch -e ip.src -e ip.dst -e data > $FILE2.data &

wait

echo "Tshark done"

echo "Starting delay calculation"

python3 scripts/calc_delta.py --distribution $dist --bandwidth $bandwidth --qdisc $qdisc --file1 $FILE1.data --file2 $FILE2.data




