import sys
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description="Plottet...")

parser.add_argument("--distribution", help="Distribution", required=True)
parser.add_argument("--bandwidth", help="Bandwidth", required=True)
parser.add_argument("--qdisc", help="Qdisc", required=True)
parser.add_argument("--file1", help="File1", required=True)
parser.add_argument("--file2", help="File2", required=True)

args = parser.parse_args()


DIST = args.distribution
SPEED = args.bandwidth
QDISC = args.qdisc
FILE1 = args.file1
FILE2 = args.file2
PRINT_STEP = 10000


#FILE1 = "/home/grohmalz/cap1.data"
#FILE2 = "/home/grohmalz/cap2.data"

#SPEED="101Mbps"
#DIST="100us_static"
#QDISC="sch_delay_fifo"



DEST_FILE="/home/grohmalz/%s_%s_%s.csv" % (DIST, SPEED, QDISC)


#MAX_SEARCH_DIST = 5_000

#print(DEST_FILE)
#c = input("continue? y/N ")
#if c != "Y" and c != "y":
#    sys.exit(0)


order = []
hashlist = {}
delays=[]
loss_count = 0

def write_header(file):
    now = datetime.now()
    text = "##########\n"
    text += "# Date: %s\n" % now.strftime("%d/%m/%Y %H:%M:%S")
    text += "# %d Matches, %3.4f%% Packet loss" % (len(order) - loss_count, float(loss_count/len(order)))
    text += "# Distribution: %s\n" % DIST
    text += "# Speed: %s\n" % SPEED
    text += "# QDISC: %s\n" % QDISC
    text += "##########\n"
    file.write(text)


def read_files(file1, file2):
    global order
    global hashlist
    print("Loading File Data...")
    with open(file1, "r") as file:
        lines = file.readlines()
    count = 0
    for line_data in lines:
        line = line_data.split(",")
        id = line[0]
        timestamp = int(line[1].replace(".",""))
        src = line[2]
        dst = line[3]
        data = line[4]  
        if src == "10.0.0.1" and dst == "20.0.0.2":
            order.append(data)
            hashlist[data] = [timestamp, None]
        if count % PRINT_STEP == 0:
            print("File1: %d lines processed" % count, end='\r')
        count += 1
    print("\nFile1 complete.")

    with open(file2, "r") as file:
        lines = file.readlines()
    count = 0
    for line_data in lines:
        line = line_data.split(",")
        id = line[0]
        timestamp = int(line[1].replace(".",""))
        src = line[2]
        dst = line[3]
        data = line[4]  
        if count % PRINT_STEP == 0:
            print("File2: %d lines processed" % count, end='\r')
        count += 1
        try:
            hashlist[data][1] = timestamp
        except:
            pass

    print("\nFile2 complete.")

def calc_delay():
    print("Calculating Delays")
    global order
    global hashlist
    global delays
    global loss_count
    print(len(order))
    count = 0
    for i in range(len(order)):
        x = order[i]
        time_in = hashlist[x][0]
        time_out = hashlist[x][1]
        if time_out == None:
            delays.append("LOSS")
            loss_count += 1
        else:
            delays.append(time_out-time_in)
        if i % PRINT_STEP == 0:
            print("%d Delays processd" % count, end='\r')
        count += 1
        
    print("\nDelays Done")


def write_file():
    print("Writing output File")
    with open(DEST_FILE,'w') as file:
        pass

    with open(DEST_FILE, "a") as file:
        write_header(file)
        for x in range(0,len(delays)):
            file.write("%d,%s\n" % (x, delays[x]))
            if x % PRINT_STEP == 0:
                print("%d lines written" % x, end='\r')

read_files(FILE1, FILE2)
calc_delay()
write_file()



sys.exit(0)

with open(FILE1, "r") as file1:
    lines1 = file1.readlines()

with open(FILE2, "r") as file2:
    lines2 = file2.readlines()


for x in lines1:
    count2 = 0


    line1 = x.split(",")
    id1 = line1[0]
    timestamp1 = int(line1[1].replace(".",""))
    src1 = line1[2]
    dst1 = line1[3]
    data1 = line1[4]


    if src1 != "10.0.0.1" or dst1 != "20.0.0.2":
        continue

    for y in range(len(delays), len(delays)+MAX_SEARCH_DIST):
        count2 += 1
        line2 = lines2[y].split(",")
        data2 = line2[4]
        if data1 == data2:
            timestamp2 = int(line2[1].replace(".",""))
            delta = timestamp2 - timestamp1
            delays.append(delta)
            #print(count2)
            break
    if count % 10000 == 0:
        print(str(count) + " " + str(len(delays)))
    count += 1
#    print("Schlecht")

print("Found %d Matches!" % len(delays))

with open(DEST_FILE,'w') as file:
    pass

with open(DEST_FILE, "a") as file:
    write_header(file)
    for x in range(0,len(delays)):
        file.write("%d,%lu\n" % (x, delays[x]))

