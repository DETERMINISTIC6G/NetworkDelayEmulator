
import matplotlib.pyplot as plt
import scipy.special as sps
import numpy as np

shift = 50000


shape, scale = 3, 15_000.  # mean=4, std=2*sqrt(2)
s = np.random.gamma(shape, scale, 100_000)
#np.moveaxis(s, 0, 1)
s+=shift

count, bins, ignored = plt.hist(s, 50, density=True)
print(len(bins))

y = bins**(shape-1)*(np.exp(-bins/scale) / (sps.gamma(shape)*scale**shape))

plt.plot(bins, y)
plt.show()




