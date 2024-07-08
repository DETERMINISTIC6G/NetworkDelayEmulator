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

import os
import numpy as np
import pandas as pd
import random


class UserDefinedDistribution:
    def __init__(self):
        self.delay_path = ""
        self.hist = None
        self.bin_edges_r = None
        self.bin_edges_l = None
        self.rng = np.random.default_rng(seed=42)
        
        

    def init(self):
        self.delay_path = self.get_valid_file_path()
        _, extension = os.path.splitext(self.delay_path)
        if extension.lower() == '.json':
            pkt_delays = pd.read_json(self.delay_path)
            self.hist, self.bin_edges_l, self.bin_edges_r = pkt_delays['count'], pkt_delays['lower_bound'], pkt_delays['upper_bound']
        elif extension.lower() == '.csv':
            pkt_delays = pd.read_csv(self.delay_path, names=['bounds', 'count', 'unit'])
            self.hist, self.bin_edges_l = pkt_delays['count'], pkt_delays['bounds']
        
    

    def generate_delays(self, count):
        data = []
        index_list = np.arange(0, len(self.hist))
        hist_sum = sum(self.hist)
        frequency = [x/hist_sum for x in self.hist]
        if self.bin_edges_r is None :
            for i in range(count) :
                #i_selected = random.choices(index_list, weights=self.hist, k=1)[0]
                i_selected = self.rng.choice(index_list, p=frequency)
                data.append(self.rng.integers(self.bin_edges_l[i_selected], self.bin_edges_l[i_selected + 1] + 1))
        else :
            for i in range(count) :
                #i_selected = random.choices(index_list, weights=self.hist, k=1)[0]
                i_selected = self.rng.choice(index_list, p=frequency)
                data.append(self.rng.integers(self.bin_edges_l[i_selected], self.bin_edges_r[i_selected] + 1))     
        return data



    def print_info(self):
        return "User-defined Distribution from %s" % (self.delay_path)

    def help(self):
        # TODO
        pass


    def get_valid_file_path(self):
        while True:
            tmp_path = input("Create delays from a histogram. Enter the file path:\n ")
            if os.path.exists(tmp_path) and os.path.isfile(tmp_path):
                return tmp_path
            else:
                print("Invalid path or the file does not exist.Please try again.")

        
        
