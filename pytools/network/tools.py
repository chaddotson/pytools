from collections import namedtuple
from subprocess import Popen, PIPE
from re import compile, IGNORECASE


# min/avg/max/stddev
PING_RESULTS_PATTERN = b"(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)"
PACKET_LOSS_PATTERN = b"(\d+\.?\d+)%"
compiled_ping_results_pattern = compile(PING_RESULTS_PATTERN, IGNORECASE)
compiled_packet_loss_pattern = compile(PACKET_LOSS_PATTERN, IGNORECASE)


class PingResults(namedtuple("PingResults", ["min", "max", "avg", "stddev", "percent_packet_loss"])):
    def __new__(cls, min=None, max=None, avg=None, stddev=None, percent_packet_loss=None):
        return super(PingResults, cls).__new__(cls, min, max, avg, stddev, percent_packet_loss)


class PingFailedError(RuntimeError):
    def __init__(self, host):
        super(PingFailedError, self).__init__("Failed to ping {0}.  Host possibly down.".format(host))


def ping(host, count=3):
    call_list = ["ping", "-c", str(count), host]
    process = Popen(call_list, stdout=PIPE)
    results, err = process.communicate()
    time_results = compiled_ping_results_pattern.search(results)
    packet_loss_results = compiled_packet_loss_pattern.search(results)
    if time_results is None:
        raise PingFailedError(host)
    time_result_matches = time_results.groups()
    packet_loss_matches = packet_loss_results.groups()
    return PingResults(min=float(time_result_matches[0]),
                       avg=float(time_result_matches[1]),
                       max=float(time_result_matches[2]),
                       stddev=float(time_result_matches[3]),
                       percent_packet_loss=float(packet_loss_matches[0]))

