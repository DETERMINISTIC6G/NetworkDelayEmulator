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