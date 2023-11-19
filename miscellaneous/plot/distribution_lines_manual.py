import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker  
import matplotlib.patches as mpatches
import sys
import matplotlib as mpl
import parse_arguments

#plt.rcParams["figure.figsize"] = [17.50, 7]
#plt.rcParams["figure.autolayout"] = True

soll_delay_x =[]
soll_delay_y = []
mess_delay_x = []
mess_delay_y = []

#SIZE=20_000
PRINT_STEP = 10_000
arg_data = {}

arg_data["distribution"] = "Normal Distributed µ: 200us, σ: 25us\n"
arg_data["distribution_name"] = "Normal Distributed µ: 200us, σ: 25us\n"
arg_data["bandwith"] = "Mixed"
arg_data["size"] = 5_000_000
arg_data["data"] = {}

#arg_data["data"]["Reference Data"] = "data/200us_25us_normal_distributed_101Mbps_reference_data.csv"
#arg_data["data"]["Sch_Delay Reordered"] = "data/200us_25us_normal_distributed_101Mbps_sch_delay_reordered.csv"
#arg_data["data"]["NetEm"] = "data/200us_25us_normal_distributed_101Mbps_netem.csv"


#arg_data["data"]["sch_delay\nNoDelay"] = "data/000_no_delay_101Mbps_sch_delay_fifo.csv"
#arg_data["data"]["sch_delay\n100us"] = "data/test_101Mbps_sch_delay_reordered.csv"
arg_data["data"]["412Mbps"] = "data/100us_static_412Mbps_sch_delay_reordered.csv"
#arg_data["data"]["sch_delay\n1ms"] = "data/99_1ms_static_101Mbps_sch_delay_fifo.csv"

SIZE = 9_990_000

mpl.rcParams['agg.path.chunksize'] = 30000

def mean_confidence_interval(data, confidence=0.99):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


plot_data = {}

#arg_data = parse_arguments.parse_arguments()
    
#SIZE = arg_data["size"]


fig, ax = plt.subplots()

#bins = np.linspace(200_000, 1_200_000, 500)

plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%d us'))

plt.title("%s Packages With a rate of ~%s,\nDistribution: %s" % ("{0:,}".format(SIZE), arg_data["bandwith"], arg_data["distribution_name"]))
#ax.ticklabel_format(useOffset=False, style='plain')

for x in arg_data["data"]:
    plot_data[x] = {}
    plot_data[x]["file_data"] = []
    plot_data[x]["x_data"] = []
    plot_data[x]["y_data"] = []
    with open(arg_data["data"][x]) as file:
        plot_data[x]["file_data"] = file.readlines()
    i=0
    for line in range(0, SIZE):
        if plot_data[x]["file_data"][line].startswith("#") or "LOSS" in plot_data[x]["file_data"][line]:
            i+=1
            continue
        data = plot_data[x]["file_data"][line]
        plot_data[x]["x_data"].append(int(data.split(",")[0]))
        plot_data[x]["y_data"].append(int(data.split(",")[1])/1000)
        if i % PRINT_STEP == 0:
            print("%d lines read" % i, end="\r")
        i += 1
    plot_data[x]["y_mean_data"] = [np.mean(plot_data[x]["y_data"])/1000]*len(plot_data[x]["x_data"])


    print("%s Data loaded" % x)
    ax.plot(plot_data[x]["x_data"],plot_data[x]["y_data"], label=x, alpha=0.5)
    print("%s Line added" % x)
#    ax.plot(plot_data[x]["x_data"],plot_data[x]["y_mean_data"], label="%s Mean: %fus" %(x, plot_data[x]["y_mean_data"][0]))
#    print("%s Mean Line added" % x)



legend = ax.legend(loc="upper right", fontsize="6")
fig.set_figwidth(18)
fig.set_figheight(6)

plt.savefig('plot.png', dpi=1000)  
plt.show()




sys.exit(0)



with open("700us_normal_userspace_delay.csv", "r") as file:
    normal_data = file.readlines()

with open("700us_normal_distributed_delay_userspace.csv", "r") as file:
    delay_hc_data = file.readlines()

for x in range(0,SIZE):
    data = normal_data[x]
    soll_delay_x.append(int(data.split(",")[0]))
    soll_delay_y.append(int(data.split(",")[1]))

soll_delay_y_mean = [np.mean(soll_delay_y)]*len(soll_delay_x)


for x in range(0,SIZE):
    data = delay_hc_data[x]
    mess_delay_x.append(int(data.split(",")[0]))
    mess_delay_y.append(int(data.split(",")[1]))

mess_delay_y = [x+100_000 for x in mess_delay_y]

mess_delay_y_mean = [np.mean(mess_delay_y)]*len(mess_delay_x)

diff_x = []
diff_y = []
i = 0
for x ,y in zip(mess_delay_y, soll_delay_y):
    diff_x.append(i)
    diff_y.append(x - y)
    i += 1

#normal_y = [x/1000 for x in normal_y]
#delay_hc_y = [x/1000 for x in delay_hc_y]
#delay_user_y = [x/1000 for x in delay_user_y]


#delay_user_y_mean = [np.mean(delay_user_y)]*len(delay_user_x)

#delay_hc_x = delay_hc_x[:int(len(delay_hc_x)/2)]
#delay_hc_y = delay_hc_y[:int(len(delay_hc_y)/2)]
#delay_hc_y_mean = delay_hc_y_mean[:int(len(delay_hc_y_mean)/2)]
#
#delay_user_x = delay_user_x[int(len(delay_user_x)/2):]
#delay_user_y = delay_user_y[int(len(delay_user_y)/2):]
#delay_user_y_mean = delay_user_y_mean[int(len(delay_user_y_mean)/2):]



fig, ax = plt.subplots()

normal_line = ax.plot(soll_delay_x,soll_delay_y, label='Soll Delay')
normal_mean_line = ax.plot(soll_delay_x,soll_delay_y_mean, label='Soll Delay Mean: %d' % soll_delay_y_mean[0])

delay_hc_line = ax.plot(mess_delay_x,mess_delay_y, label='Gemessener Delay')
delay_hc_mean_line = ax.plot(mess_delay_x,mess_delay_y_mean, label='Gemessener Delay Mean: %d' % mess_delay_y_mean[0])

#diff_line = ax.plot(diff_x, diff_y, label="Unterschied")




legend = ax.legend(loc="upper right")
#plt.legend(loc="upper left")
#µs
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%d ns'))
plt.title("%d Packages With a rate of 5.3 MB/s" % SIZE)

plt.show()