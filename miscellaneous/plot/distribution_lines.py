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

soll_delay_x =[]
soll_delay_y = []
mess_delay_x = []
mess_delay_y = []

#SIZE=20_000


def mean_confidence_interval(data, confidence=0.99):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


plot_data = {}

arg_data = parse_arguments.parse_arguments()
    
SIZE = arg_data["size"]


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
    
    for line in range(0, SIZE):
        if plot_data[x]["file_data"][line].startswith("#") or "LOSS" in plot_data[x]["file_data"][line]:
            continue
        data = plot_data[x]["file_data"][line]
        plot_data[x]["x_data"].append(int(data.split(",")[0]))
        plot_data[x]["y_data"].append(int(data.split(",")[1])/1000)
    plot_data[x]["y_mean_data"] = [np.mean(plot_data[x]["y_data"])/1000]*len(plot_data[x]["x_data"])


    print("%s Data loaded" % x)
    ax.plot(plot_data[x]["x_data"],plot_data[x]["y_data"], label=x)
    print("%s Line added" % x)
    ax.plot(plot_data[x]["x_data"],plot_data[x]["y_mean_data"], label="%s Mean: %fus" %(x, plot_data[x]["y_mean_data"][0]))
    print("%s Mean Line added" % x)



legend = ax.legend(loc="upper right", fontsize="6")
fig.set_figwidth(18)
fig.set_figheight(6)

plt.savefig('plot.png', dpi=1000)  
plt.show()
