# Copyright 2024 The NetworkDelayEmulator authors as listed in file AUTHORS.
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

class NormalDistribution:
    def __init__(self):
        self.sigma = 0
        self.mu = 0

    def init(self):
        self.mu = int(input("Mean [nanoseconds]: "))
        self.sigma = int(input("Standard deviation [nanoseconds]: "))


    def generate_delays(self, count):
        data = np.random.normal(self.mu, self.sigma, count).tolist()
        return data

    def print_info(self):
        return "Normal Distribution µ: %dns, σ: %dns" % (self.mu, self.sigma)

    def help(self):
        # TODO
        pass
