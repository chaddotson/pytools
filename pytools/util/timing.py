from collections import namedtuple
from functools import reduce
from time import time


class TimeItResults(namedtuple("TimeItResults", ["min_time", "max_time", "avg_time"])):
    def __new__(cls, min_time=0, max_time=0, avg_time=0):
        return super(TimeItResults, cls).__new__(cls, min_time=min_time, max_time=max_time, avg_time=avg_time)


def time_function(func, args=None, kwargs=None, times_to_run=1):
    args = () if args is None else args
    kwargs = {} if kwargs is None else kwargs

    results = []

    for i in range(0, times_to_run):
        start = time()
        func(*args, **kwargs)
        results.append(time()-start)

    return TimeItResults(min_time=min(results), max_time=max(results), avg_time=reduce(lambda x, y: x + y, results) / len(results))