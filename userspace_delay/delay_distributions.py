# Copyright 2024 Lorenz Grohmann (st161568@stud.uni-stuttgart.de)
#
# This file is part of NetworkDelayEmulator.
#
# NetworkDelayEmulator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# NetworkDelayEmulator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with NetworkDelayEmulator. If not, see <http://www.gnu.org/licenses/>.

import numpy as np


def normal_distributed(count):
    mu = 200_000
    sigma = 25_000
    data = np.random.normal(mu, sigma, count).tolist()
    return data

def normal_distributed2(count):
    mu = 100_000
    sigma = 25_000
    data = np.random.normal(mu, sigma, count).tolist()
    return data



def multimodel_distributed(count):
    mu1 = 300_000
    sigma1 = 25_000
    mu2 = 400_000
    sigma2 = 50_000
    mu3 = 600_000
    sigma3 = 100_000
    return np.concatenate([np.random.normal(mu1, sigma1, int(count/3)), np.random.normal(mu2, sigma2, int(count/3)), np.random.normal(mu3, sigma3, int(count/3))])





def static(count):
    delay = 100_000
    data = []
    for x in range(0, count):
        data.append(delay)
    return data


def static_zero(count):
    delay = 1
    data = []
    for x in range(0, count):
        data.append(delay)
    return data


def old(count):
    global C
    global size
    data = bytearray()
    for x in range(0, count):
        #data.extend(random.randint(0, 18_446_744_073_709_551_615).to_bytes(8,"little"))
        data.extend(int(size).to_bytes(8,"little"))
        #continue
#        if C < 100:
#            data.extend(int(0).to_bytes(8,"little"))
#        elif C < 200:
#            data.extend(int(1000000).to_bytes(8,"little"))
#        elif C < 300:
#            data.extend(int(2000000).to_bytes(8,"little"))
#        elif C < 400:
#            data.extend(int(3000000).to_bytes(8,"little"))
#        elif C < 500:
#            data.extend(int(4000000).to_bytes(8,"little"))
#        elif C < 600:
#            data.extend(int(5000000).to_bytes(8,"little"))
#        elif C < 700:
#            data.extend(int(4000000).to_bytes(8,"little"))
#        elif C < 800:
#            data.extend(int(3000000).to_bytes(8,"little"))
#        elif C < 900:
#            data.extend(int(2000000).to_bytes(8,"little"))
#        elif C < 1000:
#            data.extend(int(1000000).to_bytes(8,"little"))
#        else:
#            C = 0
#            continue

        
        C+=1
    print(len(data))
    return data

def pareto_normal(alpha, mu, size=1):
    # Generate Pareto-distributed values
    pareto_values = pareto.rvs(alpha, size=size)

    # Generate normally-distributed values
    normal_values = norm.rvs(loc=mu, scale=1, size=size)

    # Combine the two distributions
    pareto_normal_values = pareto_values * normal_values

    return pareto_normal_values
