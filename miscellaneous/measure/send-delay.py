import socket
import pickle
import time
import argparse
import random
import string 
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--count", required=False)
parser.add_argument("--delay", required=False)

args = parser.parse_args()
print(args.count)

print(time.perf_counter())

def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()

IP = "10.0.0.1"
TARGET_IP= "20.0.0.2"
PORT = 14000
TARGET_PORT = 15000
PACKAGE_COUNT = 1_000_000 + 5_000
SEND_DELAY=0.000005

if args.count == None:
    count = PACKAGE_COUNT
else:
    count = int(args.count)

if args.delay == None:
    delay=SEND_DELAY
else:
    delay = float(args.delay)


alphabet = string.ascii_lowercase + string.digits
UUID = ''.join(random.choices(alphabet, k=8))

#SEND_DELAY=0.25

def send_package(socket, id):
    data = pickle.dumps([time.time_ns(), id, UUID])
    socket.send(data)

def main():
    print("Sending %d Packages" % count)
    print("Delay: %f" % delay)
    time.sleep(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((IP, 0))
    sock.connect((TARGET_IP, TARGET_PORT))
    id = 0
    while True:
        send_package(sock, id)
        if id % 10_000 == 0:
            print(id, "\r")
        if id >= count:
            print("done")
            break
        id+=1
        
        sleep(delay)




if __name__ == "__main__":
    main()