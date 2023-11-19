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
plot_data = {}

arg_data = parse_arguments.parse_arguments()

SIZE = arg_data["size"]
    
fig, ax = plt.subplots()

bins = np.linspace(100, 350, HIST_SIZE)

#plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%d ns'))
plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%dµs'))

#ax.ticklabel_format(useOffset=False, style='plain')

for x in arg_data["data"]:
    plot_data[x] = {}
    plot_data[x]["file_data"] = []
    plot_data[x]["x_data"] = []
    plot_data[x]["y_data"] = []
    with open(arg_data["data"][x]) as file:
        plot_data[x]["file_data"] = file.readlines()
    
    for line in range(0, SIZE):
        if plot_data[x]["file_data"][line].startswith("#"):
            continue
        data = plot_data[x]["file_data"][line]
        plot_data[x]["x_data"].append(int(data.split(",")[0]))
        plot_data[x]["y_data"].append(int(data.split(",")[1])/1000)
    print("%s Data loaded" % x)
    ax.hist(plot_data[x]["y_data"], bins, alpha=0.3, label=x)
    print("%s Hist Done" % x)

legend = ax.legend(loc="upper right")
fig.set_figwidth(8)
fig.set_figheight(6)

plt.title("%s Packages With a rate of ~%s,\nDistribution: %s" % ("{0:,}".format(SIZE), arg_data["bandwith"], arg_data["distribution_name"]),fontsize = 14)


plt.xticks(fontsize=14)
plt.yticks(fontsize=14)



# plt.xlabel("Delay in µs")
# plt.ylabel("Number of Packages")



plt.savefig('plot.png', dpi=1000)  
plt.show()
