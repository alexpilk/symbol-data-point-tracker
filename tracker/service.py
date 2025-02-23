from collections import defaultdict, deque


class SlidingDeque:
    def __init__(self, is_minimum):
        self.is_minimum = is_minimum
        self.deque = deque()

    @property
    def front_value(self):
        return self.deque[0][0]

    def add_new(self, value, index):
        while self.deque and (self.deque[-1][0] >= value if self.is_minimum else self.deque[-1][0] <= value):
            self.deque.pop()
        self.deque.append((value, index))

    def remove_obsolete(self, index):
        if self.deque[0][1] == index:
            self.deque.popleft()


class RollingStats:
    def __init__(self):
        self.sum = 0
        self.sum_of_squares = 0
        self.min_deque = SlidingDeque(is_minimum=True)
        self.max_deque = SlidingDeque(is_minimum=False)


def stat_map_factory(max_k) -> dict[int, RollingStats]:
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
        total_points = len(self.symbols[symbol])
        new_points = len(values)
        for k in range(1, self.MAX_K):
            window_size = 10 ** k
            stat: RollingStats = self.rolling_stats[symbol][k]

            from_ = -1 * min(window_size, new_points)
            for i, value in enumerate(self.symbols[symbol][from_:]):
                stat.sum += value
                stat.sum_of_squares += value ** 2
                stat.min_deque.add_new(value, i + total_points + from_)
                stat.max_deque.add_new(value, i + total_points + from_)

            from_ = -1 * (new_points + window_size)
            to = -1 * max(new_points, window_size)
            for i, value in enumerate(self.symbols[symbol][from_:to]):
                stat.min_deque.remove_obsolete(i + total_points + from_)
                stat.max_deque.remove_obsolete(i + total_points + from_)
                stat.sum -= value
                stat.sum_of_squares -= value ** 2

    def get_stats(self, symbol, k):
        values = self.symbols[symbol][-1 * 10 ** k:]
        stat = self.rolling_stats[symbol][k]
        avg = stat.sum / len(values)

        variance = stat.sum_of_squares / len(values) - avg ** 2
        return {
            'min': stat.min_deque.front_value,
            'max': stat.max_deque.front_value,
            'avg': avg,
            'var': variance,
            'last': values[-1]
        }


def get_tracker():
    return Tracker()
