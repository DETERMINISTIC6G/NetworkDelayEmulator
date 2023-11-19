import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker  
import matplotlib.patches as mpatches
import sys

import parse_arguments

#plt.rcParams["figure.figsize"] = [17.50, 7]
#plt.rcParams["figure.autolayout"] = True

HIST_SIZE=350
PRINT_STEP = 10_000



START = 3_500_000
START = 0

plot_data = {}

arg_data = {}

arg_data["distribution"] = "Normal Distributed µ: 200us, σ: 25us\n"
arg_data["distribution_name"] = "Normal Distributed µ: 200us, σ: 25us\n"
arg_data["bandwith"] = "Mixed"
arg_data["size"] = 5_000_000
arg_data["data"] = {}

#arg_data["data"]["Reference Data"] = "data/200us_25us_normal_distributed_101Mbps_reference_data.csv"
#arg_data["data"]["Sch_Delay Reordered"] = "data/200us_25us_normal_distributed_101Mbps_sch_delay_reordered.csv"
#arg_data["data"]["NetEm"] = "data/200us_25us_normal_distributed_101Mbps_netem.csv"

arg_data["data"]["System Default (pfifo_fast)"] = "data/000_no_delay_101Mbps_system_default.csv"
arg_data["data"]["Sch Delay FIFO"] = "data/000_no_delay_101Mbps_sch_delay_fifo.csv"
arg_data["data"]["Sch Delay Reordered"] = "data/000_no_delay_101Mbps_sch_delay_reordered.csv"
arg_data["data"]["NetEm"] = "data/000_no_delay_101Mbps_netem.csv"


#arg_data["data"]["Sch Delay 101Mbps"] = "data/200us_25us_normal_distributed_101Mbps_sch_delay_reordered.csv"
#arg_data["data"]["Sch Delay 215Mbps"] = "data/200us_25us_normal_distributed_215Mbps_sch_delay_reordered.csv"
#arg_data["data"]["Sch Delay 305Mbps"] = "data/200us_25us_normal_distributed_305Mbps_sch_delay_reordered.csv"
#arg_data["data"]["Sch Delay 415Mbps"] = "data/200us_25us_normal_distributed_415Mbps_sch_delay_reordered.csv"
#arg_data["data"]["Sch Delay 503Mbps"] = "data/200us_25us_normal_distributed_503Mbps_sch_delay_reordered.csv"


#arg_data["data"]["NetEm 101Mbps"] = "data/200us_25us_normal_distributed_101Mbps_netem.csv"
#arg_data["data"]["NetEm 215Mbps"] = "data/200us_25us_normal_distributed_215Mbps_netem.csv"

#arg_data["data"]["NetEm 305Mbps"] = "data/200us_25us_normal_distributed_305Mbps_netem.csv"

#arg_data["data"]["NetEm 415Mbps"] = "data/200us_25us_normal_distributed_415Mbps_netem.csv"



SIZE = 5_000_000


#arg_data = parse_arguments.parse_arguments()

#SIZE = arg_data["size"]
    
fig, ax = plt.subplots()

bins = np.linspace(0, 50, HIST_SIZE)

#plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%d ns'))
plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%dµs'))

#ax.ticklabel_format(useOffset=False, style='plain')

for x in arg_data["data"]:
    print("Loading %s data..." % x)

    plot_data[x] = {}
    plot_data[x]["file_data"] = []
    plot_data[x]["x_data"] = []
    plot_data[x]["y_data"] = []
    with open(arg_data["data"][x]) as file:
        plot_data[x]["file_data"] = file.readlines()
    i = 0
    for line in range(0, SIZE):

        if i < START:
            i += 1
            continue

        if plot_data[x]["file_data"][line].startswith("#") or "LOSS" in plot_data[x]["file_data"][line]:
            continue
        data = plot_data[x]["file_data"][line]
        plot_data[x]["x_data"].append(int(data.split(",")[0]))

        plot_data[x]["y_data"].append(int(data.split(",")[1])/1000)

        if i % PRINT_STEP == 0:
            print("%d lines read" % i, end="\r")
        i += 1
    print("%s Data loaded" % x)

        


    ax.hist(plot_data[x]["y_data"], bins, alpha=0.3, label=x)
    print("%s Hist Done" % x)

legend = ax.legend(loc="upper right")
fig.set_figwidth(8)
fig.set_figheight(6)

#plt.title("%s Packages With a rate of ~%s,\nDistribution: %s" % ("{0:,}".format(SIZE), arg_data["bandwith"], arg_data["distribution_name"]),fontsize = 14)
plt.title("%s Packages\nDistribution: %s" % ("{0:,}".format(arg_data["size"]), arg_data["distribution_name"]),fontsize = 14)


plt.xticks(fontsize=14)
plt.yticks(fontsize=14)



# plt.xlabel("Delay in µs")
# plt.ylabel("Number of Packages")



plt.savefig('plot.png', dpi=1000)  
plt.show()
