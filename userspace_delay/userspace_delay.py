import os, time
import sys
import collections
import argparse
from io import BytesIO
from delay_distributions import *

from distributions import normal_distribution, static, user_defined_distribution

MAX_QUEUE_SIZE = 512000
MAX_DATA_SIZE = 40960

DISTRIBUTIONS = [
    ["Normal Distribution", normal_distribution.NormalDistribution],
    ["Static Delay", static.StaticDistribution],
    ["Histogram", user_defined_distribution.UserDefinedDistribution]
]

parser = argparse.ArgumentParser()
parser.add_argument("device", help="Character Device that corrosponds to the QDISC instance.")
parser.add_argument("-i", "--interval", help="Interval in seconds in which to check free space inside the QDISC", type=float, required=False, default=0.1)
parser.add_argument("-m", "--mincount",help="Minimum count of free elements in QDISC", type=int, required=False, default=10240)
args = parser.parse_args()

DEVICE = args.device
TIMEOUT = args.interval
MIN_DATA_SIZE = args.mincount
distribution = None

delay_count = 0
last_time = 0
last_free = 0
queue_empty_warning = False
past_rates = collections.deque([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], maxlen=20)


def clear_line(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)


def print_stats(free, added_count):
    global last_free
    global last_time
    global queue_empty_warning
    global distribution
    first_run = last_time == 0
    term_size = os.get_terminal_size().columns      
    free_delta = free - last_free
    if added_count > 0:
        last_free = free - added_count
    else:
        last_free = free
    time_delta = round(time.time() - last_time, 5)
    last_time = time.time()
    rate = int(free_delta/time_delta)
    past_rates.append(rate)

    lines = []
    lines.append("Distribution: %s" % distribution.print_info())
    lines.append("Max Queue Size: %d, Batch Size: %d, Interval: %1.2fs" % (MAX_QUEUE_SIZE, MAX_DATA_SIZE, TIMEOUT))
    lines.append("")
    if queue_empty_warning:
        lines.append("Warning: Queue was empty!")
    lines.append("Delays Submitted: %s, Space Available: %s, Rate ~%s Packages/s" % ("{0:,}".format(delay_count), "{0:,}".format(free), "{0:,}".format(int(sum(past_rates)/len(past_rates)))))
    clear_line(len(lines))
    for x in lines:
        print(x.center(term_size))



def generate_data(count):
    delay = distribution.generate_delays(count)
    data = bytearray()
    for x in delay:
        data.extend(abs(int(x)).to_bytes(8,"little"))
    return data




if __name__ == "__main__":

    s = ""
    for x in range(0, len(DISTRIBUTIONS)):
        s += "%d: %s\n" % (x+1, DISTRIBUTIONS[x][0])
    print(s)
    choice = 0
    choice = int(input("Select Distribution: "))

    distribution = DISTRIBUTIONS[choice-1][1]()
    distribution.init()
    dev = os.open(DEVICE, os.O_RDWR)
    added_count = 0

    while True:
        free = int.from_bytes(os.read(dev,8), "little")

        if free >= MAX_QUEUE_SIZE and last_free != 0:
            queue_empty_warning = True

        if free < MIN_DATA_SIZE:
            time.sleep(TIMEOUT)
            print_stats(free, added_count)
            added_count = 0
            continue

        elif free > MAX_DATA_SIZE:
            os.write(dev, generate_data(MAX_DATA_SIZE))
            delay_count += MAX_DATA_SIZE
            added_count += MAX_DATA_SIZE

        else:
            os.write(dev, generate_data(free))
            delay_count += free
            added_count += free
