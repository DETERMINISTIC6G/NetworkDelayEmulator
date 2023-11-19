export LD_LIBRARY_PATH=/opt/napatech3/lib

FILE=/home/grohmalz/cap2.cap

sudo rm $FILE

sudo LD_LIBRARY_PATH=/opt/napatech3/lib /opt/napatech3/bin//ntpcap_capture -i napa1 -n -f $FILE

