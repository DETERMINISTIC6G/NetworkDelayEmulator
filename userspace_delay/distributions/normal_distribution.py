import numpy as np

class NormalDistribution:
    def __init__(self):
        self.sigma = 0
        self.mu = 0

    def init(self):
        self.mu = int(input("Please specify the desired mean: "))
        self.sigma = int(input("Please specify the standard deviation : "))


    def generate_delays(self, count):
        data = np.random.normal(self.mu, self.sigma, count).tolist()
        return data

    def print_info(self):
        return "Normal Distributed µ: %dns, σ: %dns" % (self.mu, self.sigma)

    def help(self):
        # TODO
        pass