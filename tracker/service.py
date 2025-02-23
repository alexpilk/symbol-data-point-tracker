from collections import defaultdict


class RollingStats:
    def __init__(self):
        self.sum = 0
        self.sum_of_squares = 0


def stat_map_factory(max_k):
    return {
        k: RollingStats() for k in range(1, max_k)
    }


class Tracker:
    MAX_K = 8

    def __init__(self):
        self.symbols = {}
        self.rolling_stats = {}
        self.reset()

    def reset(self):
        self.symbols = defaultdict(list)
        self.rolling_stats = defaultdict(lambda: stat_map_factory(self.MAX_K))

    def add(self, symbol, values):
        self.symbols[symbol] += values
        new_points = len(values)
        for k in range(1, self.MAX_K):
            window_size = 10 ** k

            from_ = -1 * min(window_size, new_points)
            for value in values[from_:]:
                self.rolling_stats[symbol][k].sum += value
                self.rolling_stats[symbol][k].sum_of_squares += value ** 2

            from_ = -1 * (new_points + window_size)
            to = -1 * max(new_points, window_size)
            for value in self.symbols[symbol][from_:to]:
                self.rolling_stats[symbol][k].sum -= value
                self.rolling_stats[symbol][k].sum_of_squares -= value ** 2

    def get_stats(self, symbol, k):
        values = self.symbols[symbol][-1 * 10 ** k:]
        avg = self.rolling_stats[symbol][k].sum / len(values)

        variance = self.rolling_stats[symbol][k].sum_of_squares / len(values) - avg ** 2
        return {
            'min': min(values),
            'max': max(values),
            'avg': avg,
            'var': variance,
            'last': values[-1]
        }


def get_tracker():
    return Tracker()
