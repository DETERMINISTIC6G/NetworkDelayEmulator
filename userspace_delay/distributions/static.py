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

class StaticDistribution:
    def __init__(self):
        self.delay = 0

    def init(self):
        self.delay = int(input("Please specify the desired delay in nanoseconds: "))

    def generate_delays(self, count):
        data = []
        for x in range(0, count):
            data.append(self.delay)
        return data

    def print_info(self):
        return "Static Delay %dns" % self.delay

    def help(self):
        # TODO
        pass
