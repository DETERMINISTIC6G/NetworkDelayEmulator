DELAY=1

cd /home/grohmalz/scripts
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
if [ "$#" -ne 3]; then
    read -p "Number of Preocesses: " pcount
    read -p "Number of Packages per Process: " count
    read -p "Delay between packages: " delay
else
pcount=$1
count=$2
delay=$3
fi

echo Staring $pcount Processes with $count Packages each
sleep 1

for (( x=0; x<$pcount; x++)); do
    sudo nice -n -15 python3 send-delay.py --count $count --delay $delay &
done

wait
exit 0