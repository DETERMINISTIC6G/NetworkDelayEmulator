#%%
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker  
import matplotlib.patches as mpatches
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

SIZE = 1_000



def mean_confidence_interval(data, confidence=0.99):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


with open("100us_delay_hardcoded.csv", "r") as file:
    normal_data = file.readlines()

with open("100us_delay_hardcoded.csv", "r") as file:
    delay_hc_data = file.readlines()

with open("100us_delay_userspace.csv", "r") as file:
    delay_user_data = file.readlines()

with open("100us_netem.csv", "r") as file:
    delay_netem_data = file.readlines()

for x in range(0,SIZE):
    data = normal_data[x]
    normal_x.append(int(data.split(",")[0]))
    normal_y.append(int(data.split(",")[1]))
normal_y_mean = [np.mean(normal_y)]*len(normal_x)

for x in range(0,SIZE):
    data = delay_hc_data[x]
    delay_hc_x.append(int(data.split(",")[0]))
    delay_hc_y.append(int(data.split(",")[1]))

delay_hc_y_mean = [np.mean(delay_hc_y)]*len(delay_hc_x)

for x in range(0,SIZE):
    data = delay_user_data[x]
    delay_user_x.append(int(data.split(",")[0]))
    delay_user_y.append(int(data.split(",")[1]))

delay_user_y = [x+100_000 for x in delay_user_y]
delay_user_y_mean = [np.mean(delay_user_y)]*len(delay_user_x)


for x in range(0,SIZE):
    data = delay_netem_data[x]
    delay_netem_x.append(int(data.split(",")[0]))
    delay_netem_y.append(int(data.split(",")[1]))

delay_netem_y = [x+200_000 for x in delay_netem_y]

delay_netem_y_mean = [np.mean(delay_netem_y)]*len(delay_netem_x)


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

normal_line = ax.plot(normal_x,normal_y, label='Without Delay')
normal_mean_line = ax.plot(normal_x,normal_y_mean, label='Without Delay Mean: %d' % normal_y_mean[0])

delay_hc_line = ax.plot(delay_hc_x,delay_hc_y, label='With Hardcoded Delay (0.10ms)')
delay_hc_mean_line = ax.plot(delay_hc_x,delay_hc_y_mean, label='Hardcoded Delay Mean: %d' % delay_hc_y_mean[0])

delay_user_line = ax.plot(delay_user_x,delay_user_y, label='With Userspace Delay (0.10ms)')
delay_user_mean_line = ax.plot(delay_user_x,delay_user_y_mean, label='Userspace Delay Mean: %d' % delay_user_y_mean[0])

delay_netem_line = ax.plot(delay_netem_x,delay_netem_y, label='With NetEm Delay (0.10ms)')
delay_netem_mean_line = ax.plot(delay_netem_x,delay_netem_y_mean, label='NetEm Delay Mean: %d' % delay_netem_y_mean[0])

#normal_boxplot = ax.boxplot(normal_y, vert=1, notch=True)
#delay_hc_boxplot = ax.boxplot(delay_hc_y, vert=1, notch=True)
#delay_user_boxplot = ax.boxplot(delay_user_y, vert=1, notch=True)




legend = ax.legend(loc="upper right")
#plt.legend(loc="upper left")
#µs
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%d ns'))
plt.title("%d Packages With a rate of 5.3 MB/s" % SIZE)

plt.show()
plt.savefig('line_plot.pdf')  
# %%
