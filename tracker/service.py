from collections import defaultdict


class Tracker:
    def __init__(self):
        self.symbols = defaultdict(list)

    def add(self, symbol, values):
        self.symbols[symbol] += (values)

    def get_stats(self, symbol, k):
        values = self.symbols[symbol][-1 * 10 ** k:]
        avg = sum(values) / len(values)
        variance = sum([(point - avg) ** 2 for point in values]) / len(values)
        return {
            'min': min(values),
            'max': max(values),
            'avg': avg,
            'var': variance,
            'last': values[-1]
        }

    def reset(self):
        self.symbols = defaultdict(list)


tracker = Tracker()
