from collections import namedtuple
from subprocess import Popen, PIPE
from re import compile, IGNORECASE


# min/avg/max/stddev
PING_RESULTS_PATTERN = b"(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)"
compiled_ping_results_pattern = compile(PING_RESULTS_PATTERN, IGNORECASE)


class PingResults(namedtuple("PingResults", ["min", "max", "avg", "stddev"])):
    def __new__(cls, min=None, max=None, avg=None, stddev=None):
        return super(PingResults, cls).__new__(cls, min, max, avg, stddev)


class PingFailedError(RuntimeError):
    def __init__(self, host):
        super(PingFailedError, self).__init__("Failed to ping {0}.  Host possibly down.".format(host))


def ping(host, count=3):
    call_list = ["ping", "-c", str(count), host]
    process = Popen(call_list, stdout=PIPE)
    results, err = process.communicate()
    parsed = compiled_ping_results_pattern.search(results)
    if parsed is None:
        raise PingFailedError(host)
    matches = parsed.groups()
    return PingResults(min=matches[0], avg=matches[1], max=matches[2], stddev=matches[3])

