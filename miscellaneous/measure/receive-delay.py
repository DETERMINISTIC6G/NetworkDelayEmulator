import socket
import pickle
import time
import csv

IP = "20.0.0.2"
PORT = 15000

PRINT_STEP=10_000



delays = {}


def receive_package():
    pass

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((IP, PORT))
#    sock.listen(1)
    print("Listening on %s:%s" % (IP, PORT))
#    print("Receiving %d Packages" % max_count)
    count = 0
    try:
        while True:
    #        c, addr = sock.accept()
    #       print("New Connection from: %s" % (str(addr)))
    #        try:
            data, addr  = sock.recvfrom(1024)
            if not data:
                print("Schlecht0...")
                continue

            timestamp = time.time_ns()

            try:
                data = pickle.loads(data)
            except:
                print("Schlecht1...")
                pass

#            print(data)
#            delta = (timestamp - int(data[0]))
#            delta_ms = delta * (10 ** -6)
#            id = data[1]
#            print(data)
#            delays[id] = delta_ms

            if count % PRINT_STEP == 0:
                print("Packages Received: %d" % count, end="\r")
            count+=1
#            print("Package received: ID: %d, Delay: %sms" % (id, str(delta_ms)))
#            if count >= max_count:
#                break
#            count+=1
    except:
        print("Schlecht2...")
    finally:
        sock.close()








if __name__ == "__main__":
    main()