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

normal_x =[]
normal_y = []
delay_hc_x = []
delay_hc_y = []
delay_user_x = []
delay_user_y = []
delay_netem_x = []
delay_netem_y = []

#START=2_000_000
START=0

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


boxplots = []
labels = []

for x in arg_data["data"]:
    plot_data[x] = {}
    plot_data[x]["file_data"] = []
    plot_data[x]["x_data"] = []
    plot_data[x]["y_data"] = []
    plot_data[x]["y_mean_data"] = []
    with open(arg_data["data"][x]) as file:
        plot_data[x]["file_data"] = file.readlines()
    
    i=0
    for line in range(0, SIZE):
        if plot_data[x]["file_data"][line].startswith("#"):
            continue        
        data = plot_data[x]["file_data"][line]
        if i > START:
            plot_data[x]["x_data"].append(int(data.split(",")[0]))
            plot_data[x]["y_data"].append(int(data.split(",")[1])/1000)
        i+=1



    plot_data[x]["y_mean_data"] = [np.mean(plot_data[x]["y_mean_data"])]*len(plot_data[x]["x_data"])
    print("%s Data loaded" % x)

    boxplots.append(plot_data[x]["y_data"])
    labels.append(x)

print(labels)
bp = ax.boxplot(boxplots, labels=labels, notch=True, widths=0.4)
for line in bp["medians"]:
    x, y = line.get_xydata()[1] # top of median line
    ax.text(x+len(bp["medians"])/18, y-2, '%.2fµs' % y, horizontalalignment='center', fontsize="large") # draw above, centered

#for line in bp["boxes"]:
#    print(line.get_xydata())
#    x, y = line.get_xydata()[1] # bottom of left line
#    ax.text(x+len(bp["medians"])/10,y, '%.1f' % y,
#         horizontalalignment='center', # centered
#         verticalalignment='top')      # below
 
#    x, y = line.get_xydata()[2] # bottom of right line
#    ax.text(x+0.0,y-y/10, '%.1f' % y,
#         horizontalalignment='center', # centered
#             verticalalignment='top')      # below

#    x, y = line.get_xydata()[3] # bottom of right line
#    ax.text(x+0.04,y, '%.1f' % y,
#         horizontalalignment='center', # centered
#             verticalalignment='top')      # below

#    x, y = line.get_xydata()[4] # bottom of right line
#    ax.text(x+0.0,y+y/10, '%.1f' % y,
#         horizontalalignment='center', # centered
#             verticalalignment='top')      # below

#    x, y = line.get_xydata()[5] # bottom of right line
#    ax.text(x+len(bp["medians"])/10,y, '%.1f' % y,
#         horizontalalignment='center', # centered
#             verticalalignment='top')      # below


plt.title("%s Packages With a rate of ~%s,\nDistribution: %s" % ("{0:,}".format(SIZE), arg_data["bandwith"], arg_data["distribution_name"]),fontsize = 14)


plt.xticks(fontsize=14)
plt.yticks(fontsize=14)


#plt.xlabel("Delaying Entity")
#plt.ylabel("Delay in µs")


plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%dµs'))

fig.set_figwidth(16)
fig.set_figheight(6)
plt.savefig('plot.png', dpi=1000)  
#plt.show()

sys.exit(1)

















#    ax.hist(plot_data[x]["y_data"], bins, alpha=0.3, label=x)
#    print("%s Hist Done" % x)

legend = ax.legend(loc="upper right")

labels = ["Without Delay", "With Hardcoded Delay (0.10ms)", "With NetEm Delay (0.10ms)", "With Userspace Delay (0.10ms)"]
plot_data = [normal_y, delay_hc_y, delay_netem_y, delay_user_y]
colors = ['red', 'orange', 'yellow', "green"]
bp = ax.boxplot(plot_data, labels=labels)
bp_data = {}
i=1

for i in range(0,len(labels)):
    dict1 = {}
    dict1['lower_whisker'] = bp['whiskers'][i*2].get_ydata()[1]
    dict1['lower_quartile'] = bp['boxes'][i].get_ydata()[1]
    dict1['median'] = bp['medians'][i].get_ydata()[1]
    dict1['upper_quartile'] = bp['boxes'][i].get_ydata()[2]
    dict1['upper_whisker'] = bp['whiskers'][(i*2)+1].get_ydata()[1]
    mean, lc, uc = mean_confidence_interval(plot_data[i])
    dict1["lower_confidence_interval"] = lc
    dict1["mean"] = mean
    dict1["upeer_confidence_interval"] = uc
    bp_data[labels[i]] = dict1


for x in bp_data:
    print(x)
    for y in bp_data[x]:
        print("%s: %s" % (y, bp_data[x][y]))
    print("\n")


print("Normal Range: %f" % (bp_data["Without Delay"]["upeer_confidence_interval"] - bp_data["Without Delay"]["lower_confidence_interval"]))
print("HC Range: %f" % (bp_data["With Hardcoded Delay (0.10ms)"]["upeer_confidence_interval"] - bp_data["With Hardcoded Delay (0.10ms)"]["lower_confidence_interval"]))
print("User Range: %f" % (bp_data["With Userspace Delay (0.10ms)"]["upeer_confidence_interval"] - bp_data["With Userspace Delay (0.10ms)"]["lower_confidence_interval"]))
print("User Range: %f" % (bp_data["With NetEm Delay (0.10ms)"]["upeer_confidence_interval"] - bp_data["With NetEm Delay (0.10ms)"]["lower_confidence_interval"]))

#normal_boxplot = ax.boxplot(normal_y, vert=1, notch=True)
#delay_hc_boxplot = ax.boxplot(delay_hc_y, vert=1, notch=True)
#delay_user_boxplot = ax.boxplot(delay_user_y, vert=1, notch=True)

custom_legends=[]

i=0
for x in labels:
    median = bp_data[x]["median"]
    mean = bp_data[x]["mean"]
    lq = bp_data[x]["lower_quartile"]
    uq = bp_data[x]["upper_quartile"]
    lc = bp_data[x]["lower_confidence_interval"]
    uc = bp_data[x]["upeer_confidence_interval"]

    custom_legends.append(mpatches.Patch(color=colors[i], label="%s:\n Median %d, Mean: %d\nLower Quartiele: %d, Upper Quartiele: %d\nLower Confidence I: %d, Upper Confidence I: %d" % (x, median, mean, lq, uq, lc, uc)))
    i+=1


#legend = ax.legend(loc="upper right")
plt.legend(loc="upper left", handles=custom_legends)
#µs
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%d ns'))
plt.title("%d Packages With a rate of 5.3 MB/s" % SIZE)

plt.show()